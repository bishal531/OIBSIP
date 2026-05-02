"""
Utility Functions for Fraud Detection System
"""

import logging
import pickle
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)

import config


def setup_logging(name: str = __name__, log_level: str = config.LOG_LEVEL) -> logging.Logger:
    """
    Setup logging configuration.
    
    Args:
        name: Logger name
        log_level: Logging level
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(config.LOG_FORMAT)
    console_handler.setFormatter(console_formatter)
    
    # File handler
    file_handler = logging.FileHandler(config.LOG_FILE)
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter(config.LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


def save_model(model: Any, filepath: Path) -> None:
    """
    Save model to disk using pickle.
    
    Args:
        model: Trained model
        filepath: Path to save model
    """
    logger = setup_logging(__name__)
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(model, f)
        logger.info(f"Model saved to {filepath}")
    except Exception as e:
        logger.error(f"Error saving model: {str(e)}")
        raise


def load_model(filepath: Path) -> Any:
    """
    Load model from disk.
    
    Args:
        filepath: Path to model file
        
    Returns:
        Loaded model
    """
    logger = setup_logging(__name__)
    try:
        with open(filepath, 'rb') as f:
            model = pickle.load(f)
        logger.info(f"Model loaded from {filepath}")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise


def save_results(results: Dict[str, Any], filepath: Path, format: str = "json") -> None:
    """
    Save results to file.
    
    Args:
        results: Dictionary of results
        filepath: Path to save results
        format: File format ('json' or 'pickle')
    """
    logger = setup_logging(__name__)
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        if format == "json":
            # Convert numpy types to native Python types for JSON serialization
            results_serializable = convert_to_serializable(results)
            with open(filepath, 'w') as f:
                json.dump(results_serializable, f, indent=4)
        else:  # pickle
            with open(filepath, 'wb') as f:
                pickle.dump(results, f)
        
        logger.info(f"Results saved to {filepath}")
    except Exception as e:
        logger.error(f"Error saving results: {str(e)}")
        raise


def load_results(filepath: Path) -> Dict[str, Any]:
    """
    Load results from file.
    
    Args:
        filepath: Path to results file
        
    Returns:
        Results dictionary
    """
    logger = setup_logging(__name__)
    try:
        if filepath.suffix == ".json":
            with open(filepath, 'r') as f:
                results = json.load(f)
        else:  # pickle
            with open(filepath, 'rb') as f:
                results = pickle.load(f)
        
        logger.info(f"Results loaded from {filepath}")
        return results
    except Exception as e:
        logger.error(f"Error loading results: {str(e)}")
        raise


def convert_to_serializable(obj: Any) -> Any:
    """
    Convert numpy/pandas objects to Python native types for JSON serialization.
    
    Args:
        obj: Object to convert
        
    Returns:
        Serializable object
    """
    if isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    elif isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.DataFrame):
        return obj.to_dict()
    elif isinstance(obj, pd.Series):
        return obj.to_dict()
    else:
        return obj


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, 
                   y_pred_proba: np.ndarray = None) -> Dict[str, float]:
    """
    Compute classification metrics.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        y_pred_proba: Prediction probabilities
        
    Returns:
        Dictionary of metrics
    """
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
    }
    
    if y_pred_proba is not None and len(np.unique(y_true)) > 1:
        try:
            metrics["roc_auc"] = roc_auc_score(y_true, y_pred_proba)
        except:
            metrics["roc_auc"] = None
    
    return metrics


def get_classification_report(y_true: np.ndarray, y_pred: np.ndarray) -> str:
    """
    Get detailed classification report.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        
    Returns:
        Classification report string
    """
    return classification_report(y_true, y_pred, target_names=["Legitimate", "Fraudulent"])


def get_confusion_matrix_dict(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, int]:
    """
    Get confusion matrix as dictionary.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        
    Returns:
        Dictionary with TP, TN, FP, FN
    """
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return {
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
    }


def calculate_fraud_rate(y: np.ndarray) -> float:
    """
    Calculate fraud rate in dataset.
    
    Args:
        y: Labels array
        
    Returns:
        Fraud rate as percentage
    """
    return (y.sum() / len(y)) * 100


def print_data_statistics(X: pd.DataFrame, y: pd.Series) -> None:
    """
    Print dataset statistics.
    
    Args:
        X: Features dataframe
        y: Target series
    """
    logger = setup_logging(__name__)
    
    logger.info(f"Dataset shape: {X.shape}")
    logger.info(f"Number of features: {X.shape[1]}")
    logger.info(f"Number of samples: {X.shape[0]}")
    
    fraud_rate = (y.sum() / len(y)) * 100
    logger.info(f"Fraud rate: {fraud_rate:.2f}%")
    logger.info(f"Fraudulent transactions: {y.sum()}")
    logger.info(f"Legitimate transactions: {len(y) - y.sum()}")
    logger.info(f"Class ratio (Fraud:Legit): 1:{(len(y) - y.sum()) / y.sum():.0f}")
    
    logger.info("\nFeature statistics:")
    logger.info(f"\nDescriptive statistics:\n{X.describe()}")
    logger.info(f"\nMissing values:\n{X.isnull().sum()}")


def optimize_threshold(y_true: np.ndarray, y_pred_proba: np.ndarray, 
                      metric: str = "f1") -> Tuple[float, float]:
    """
    Find optimal classification threshold.
    
    Args:
        y_true: True labels
        y_pred_proba: Prediction probabilities
        metric: Metric to optimize ('f1', 'precision', 'recall')
        
    Returns:
        Optimal threshold and metric value
    """
    thresholds = np.arange(0.0, 1.01, 0.01)
    best_threshold = 0.5
    best_value = 0.0
    
    for threshold in thresholds:
        y_pred = (y_pred_proba >= threshold).astype(int)
        
        if metric == "f1":
            value = f1_score(y_true, y_pred, zero_division=0)
        elif metric == "precision":
            value = precision_score(y_true, y_pred, zero_division=0)
        elif metric == "recall":
            value = recall_score(y_true, y_pred, zero_division=0)
        else:
            raise ValueError(f"Unknown metric: {metric}")
        
        if value > best_value:
            best_value = value
            best_threshold = threshold
    
    return best_threshold, best_value


class PerformanceTracker:
    """Track model performance across experiments."""
    
    def __init__(self):
        self.results = []
        self.logger = setup_logging(__name__)
    
    def add_result(self, experiment_name: str, model_name: str, metrics: Dict[str, float]) -> None:
        """Add result to tracker."""
        result = {
            "experiment": experiment_name,
            "model": model_name,
            **metrics
        }
        self.results.append(result)
        self.logger.info(f"Added result: {experiment_name} - {model_name}")
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert results to DataFrame."""
        return pd.DataFrame(self.results)
    
    def get_best_model(self, metric: str = "roc_auc") -> Dict[str, Any]:
        """Get best model by metric."""
        df = self.to_dataframe()
        best_idx = df[metric].idxmax()
        return df.iloc[best_idx].to_dict()
    
    def save(self, filepath: Path) -> None:
        """Save results to file."""
        save_results({"results": self.results}, filepath)
        self.logger.info(f"Tracker results saved to {filepath}")


if __name__ == "__main__":
    logger = setup_logging(__name__)
    logger.info("Utilities module loaded successfully")
