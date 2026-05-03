"""
Model Training and Inference Module for Fraud Detection System
"""

import logging
from pathlib import Path
from typing import Dict, Any, Tuple, List

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
import xgboost as xgb
import lightgbm as lgb

import config
from src.utils import setup_logging, save_model, load_model


class ModelTrainer:
    """Train and manage multiple machine learning models."""
    
    def __init__(self):
        """Initialize the model trainer."""
        self.logger = setup_logging(__name__)
        self.models = {}
        self.trained_models = {}
        self.model_metrics = {}
    
    def build_logistic_regression(self) -> LogisticRegression:
        """Build Logistic Regression model."""
        self.logger.info("Building Logistic Regression model...")
        params = config.HYPERPARAMETERS.get("logistic_regression", {})
        return LogisticRegression(**params)
    
    def build_decision_tree(self) -> DecisionTreeClassifier:
        """Build Decision Tree model."""
        self.logger.info("Building Decision Tree model...")
        params = config.HYPERPARAMETERS.get("decision_tree", {})
        return DecisionTreeClassifier(**params)
    
    def build_random_forest(self) -> RandomForestClassifier:
        """Build Random Forest model."""
        self.logger.info("Building Random Forest model...")
        params = config.HYPERPARAMETERS.get("random_forest", {})
        return RandomForestClassifier(**params)
    
    def build_gradient_boosting(self) -> GradientBoostingClassifier:
        """Build Gradient Boosting model."""
        self.logger.info("Building Gradient Boosting model...")
        params = config.HYPERPARAMETERS.get("gradient_boosting", {})
        return GradientBoostingClassifier(**params)
    
    def build_xgboost(self) -> xgb.XGBClassifier:
        """Build XGBoost model."""
        self.logger.info("Building XGBoost model...")
        params = config.HYPERPARAMETERS.get("xgboost", {})
        params['scale_pos_weight'] = (1 - 0.001) / 0.001  # Adjust for class imbalance
        return xgb.XGBClassifier(**params)
    
    def build_lightgbm(self) -> lgb.LGBMClassifier:
        """Build LightGBM model."""
        self.logger.info("Building LightGBM model...")
        params = config.HYPERPARAMETERS.get("lightgbm", {})
        params['is_unbalance'] = True  # Handle class imbalance
        return lgb.LGBMClassifier(**params)
    
    def build_neural_network(self, input_dim: int) -> MLPClassifier:
        """Build Neural Network model."""
        self.logger.info("Building Neural Network model...")
        params = config.HYPERPARAMETERS.get("neural_network", {})
        
        hidden_layers = params.pop("hidden_layers", [128, 64, 32])
        hidden_layer_sizes = tuple(hidden_layers)
        
        return MLPClassifier(
            hidden_layer_sizes=hidden_layer_sizes,
            activation=params.get("activation", "relu"),
            learning_rate_init=params.get("learning_rate", 0.001),
            max_iter=params.get("epochs", 50),
            random_state=config.RANDOM_STATE,
            early_stopping=True,
            validation_fraction=0.2,
            n_iter_no_change=10,
        )
    
    def train_model(self, model: Any, X_train: np.ndarray, y_train: np.ndarray, 
                   model_name: str = "model") -> Any:
        """
        Train a single model.
        
        Args:
            model: Model instance
            X_train: Training features
            y_train: Training labels
            model_name: Name of the model
            
        Returns:
            Trained model
        """
        self.logger.info(f"Training {model_name}...")
        
        model.fit(X_train, y_train)
        
        # Store model metrics (training accuracy)
        train_accuracy = model.score(X_train, y_train)
        self.logger.info(f"{model_name} - Training Accuracy: {train_accuracy:.4f}")
        
        self.trained_models[model_name] = model
        return model
    
    def train_all_models(self, X_train: np.ndarray, y_train: np.ndarray) -> Dict[str, Any]:
        """
        Train all configured models.
        
        Args:
            X_train: Training features
            y_train: Training labels
            
        Returns:
            Dictionary of trained models
        """
        self.logger.info("Starting training of all models...")
        
        # Get input dimension for neural network
        input_dim = X_train.shape[1]
        
        models_to_build = {
            "logistic_regression": self.build_logistic_regression,
            "decision_tree": self.build_decision_tree,
            "random_forest": self.build_random_forest,
            "gradient_boosting": self.build_gradient_boosting,
            "xgboost": self.build_xgboost,
            "lightgbm": self.build_lightgbm,
            "neural_network": lambda: self.build_neural_network(input_dim),
        }
        
        for model_name in config.MODELS_TO_TRAIN:
            if model_name not in models_to_build:
                self.logger.warning(f"Model {model_name} not found. Skipping...")
                continue
            
            try:
                model = models_to_build[model_name]()
                self.train_model(model, X_train, y_train, model_name)
            except Exception as e:
                self.logger.error(f"Error training {model_name}: {str(e)}")
        
        self.logger.info(f"Trained {len(self.trained_models)} models")
        return self.trained_models
    
    def predict(self, model_name: str, X: np.ndarray) -> np.ndarray:
        """
        Make predictions with a trained model.
        
        Args:
            model_name: Name of trained model
            X: Features
            
        Returns:
            Predictions
        """
        if model_name not in self.trained_models:
            raise ValueError(f"Model {model_name} not found in trained models")
        
        model = self.trained_models[model_name]
        return model.predict(X)
    
    def predict_proba(self, model_name: str, X: np.ndarray) -> np.ndarray:
        """
        Get prediction probabilities.
        
        Args:
            model_name: Name of trained model
            X: Features
            
        Returns:
            Prediction probabilities
        """
        if model_name not in self.trained_models:
            raise ValueError(f"Model {model_name} not found in trained models")
        
        model = self.trained_models[model_name]
        
        if not hasattr(model, 'predict_proba'):
            self.logger.warning(f"{model_name} does not support predict_proba. Using decision_function.")
            if hasattr(model, 'decision_function'):
                scores = model.decision_function(X)
                # Normalize to [0, 1]
                proba = 1 / (1 + np.exp(-scores))
                return proba
            else:
                raise ValueError(f"{model_name} does not support probability predictions")
        
        return model.predict_proba(X)
    
    def save_trained_models(self, save_dir: Path = None) -> None:
        """
        Save all trained models.
        
        Args:
            save_dir: Directory to save models
        """
        if save_dir is None:
            save_dir = config.MODELS_DIR
        
        save_dir.mkdir(parents=True, exist_ok=True)
        
        for model_name, model in self.trained_models.items():
            filepath = save_dir / f"{model_name}.pkl"
            save_model(model, filepath)
        
        self.logger.info(f"Saved {len(self.trained_models)} models to {save_dir}")
    
    def load_trained_models(self, load_dir: Path = None, model_names: List[str] = None) -> None:
        """
        Load trained models from disk.
        
        Args:
            load_dir: Directory containing models
            model_names: List of model names to load (if None, load all)
        """
        if load_dir is None:
            load_dir = config.MODELS_DIR
        
        if model_names is None:
            model_names = [f.stem for f in load_dir.glob("*.pkl")]
        
        for model_name in model_names:
            filepath = load_dir / f"{model_name}.pkl"
            if filepath.exists():
                model = load_model(filepath)
                self.trained_models[model_name] = model
                self.logger.info(f"Loaded model: {model_name}")
            else:
                self.logger.warning(f"Model file not found: {filepath}")
        
        self.logger.info(f"Loaded {len(self.trained_models)} models from {load_dir}")
    
    def get_feature_importance(self, model_name: str, feature_names: List[str] = None, 
                              top_n: int = 20) -> pd.DataFrame:
        """
        Get feature importance from a model.
        
        Args:
            model_name: Name of trained model
            feature_names: List of feature names
            top_n: Number of top features to return
            
        Returns:
            Dataframe with feature importance
        """
        if model_name not in self.trained_models:
            raise ValueError(f"Model {model_name} not found in trained models")
        
        model = self.trained_models[model_name]
        
        if not hasattr(model, 'feature_importances_'):
            self.logger.warning(f"{model_name} does not have feature_importances_ attribute")
            return None
        
        importances = model.feature_importances_
        
        if feature_names is None:
            feature_names = [f"Feature_{i}" for i in range(len(importances))]
        
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importances
        }).sort_values('Importance', ascending=False).head(top_n)
        
        self.logger.info(f"\nTop {top_n} Features for {model_name}:")
        self.logger.info(importance_df.to_string())
        
        return importance_df
    
    def get_trained_models_list(self) -> List[str]:
        """Get list of trained model names."""
        return list(self.trained_models.keys())


class AnomalyDetector:
    """Anomaly detection using Isolation Forest and LOF."""
    
    def __init__(self):
        """Initialize the anomaly detector."""
        self.logger = setup_logging(__name__)
        self.isolation_forest = None
        self.lof = None
    
    def train_isolation_forest(self, X_train: np.ndarray) -> None:
        """
        Train Isolation Forest model.
        
        Args:
            X_train: Training features
        """
        from sklearn.ensemble import IsolationForest
        
        self.logger.info("Training Isolation Forest...")
        params = config.HYPERPARAMETERS.get("isolation_forest", {})
        
        self.isolation_forest = IsolationForest(**params)
        self.isolation_forest.fit(X_train)
        
        self.logger.info("Isolation Forest trained")
    
    def train_lof(self, X_train: np.ndarray) -> None:
        """
        Train Local Outlier Factor model.
        
        Args:
            X_train: Training features
        """
        from sklearn.neighbors import LocalOutlierFactor
        
        self.logger.info("Training Local Outlier Factor...")
        params = config.HYPERPARAMETERS.get("local_outlier_factor", {})
        
        self.lof = LocalOutlierFactor(**params)
        self.lof.fit(X_train)
        
        self.logger.info("LOF trained")
    
    def detect_anomalies_if(self, X: np.ndarray) -> np.ndarray:
        """
        Detect anomalies using Isolation Forest.
        
        Args:
            X: Features
            
        Returns:
            Anomaly predictions (-1: anomaly, 1: normal)
        """
        if self.isolation_forest is None:
            raise ValueError("Isolation Forest not trained yet")
        
        return self.isolation_forest.predict(X)
    
    def detect_anomalies_lof(self, X: np.ndarray) -> np.ndarray:
        """
        Detect anomalies using LOF.
        
        Args:
            X: Features
            
        Returns:
            Anomaly predictions (-1: anomaly, 1: normal)
        """
        if self.lof is None:
            raise ValueError("LOF not trained yet")
        
        return self.lof.predict(X)
    
    def get_anomaly_scores_if(self, X: np.ndarray) -> np.ndarray:
        """
        Get anomaly scores from Isolation Forest (lower is more anomalous).
        
        Args:
            X: Features
            
        Returns:
            Anomaly scores
        """
        if self.isolation_forest is None:
            raise ValueError("Isolation Forest not trained yet")
        
        return self.isolation_forest.score_samples(X)


if __name__ == "__main__":
    logger = setup_logging(__name__)
    logger.info("Models module loaded successfully")
