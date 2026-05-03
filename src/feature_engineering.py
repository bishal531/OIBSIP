"""
Feature Engineering Module for Fraud Detection System
"""

import logging
from typing import Tuple, List, Optional

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import PolynomialFeatures

import config
from src.utils import setup_logging


class FeatureEngineer:
    """Handle feature engineering and transformation."""
    
    def __init__(self):
        """Initialize the feature engineer."""
        self.logger = setup_logging(__name__)
        self.pca = None
        self.polynomial_features = None
        self.feature_names = None
    
    def engineer_time_features(self, df: pd.DataFrame, time_column: str = "Time") -> pd.DataFrame:
        """
        Engineer time-based features from Time column.
        
        Args:
            df: Input dataframe
            time_column: Name of time column (in seconds)
            
        Returns:
            Dataframe with time features added
        """
        if not config.ENGINEER_TIME_FEATURES:
            return df
        
        if time_column not in df.columns:
            self.logger.warning(f"Time column '{time_column}' not found")
            return df
        
        self.logger.info("Engineering time features...")
        
        # Convert seconds to hours (assuming data is within 48 hours)
        df['Hour'] = (df[time_column] / 3600) % 24
        df['Day'] = df[time_column] // (3600 * 24)
        
        # Time intervals (peak hours, off-peak)
        df['IsPeakHour'] = ((df['Hour'] >= 9) & (df['Hour'] <= 17)).astype(int)
        df['IsNight'] = ((df['Hour'] >= 22) | (df['Hour'] < 6)).astype(int)
        
        # Sin/Cos transformation for cyclical time
        df['Hour_sin'] = np.sin(2 * np.pi * df['Hour'] / 24)
        df['Hour_cos'] = np.cos(2 * np.pi * df['Hour'] / 24)
        
        self.logger.info("Time features engineered")
        return df
    
    def engineer_amount_features(self, df: pd.DataFrame, amount_column: str = "Amount") -> pd.DataFrame:
        """
        Engineer amount-based features.
        
        Args:
            df: Input dataframe
            amount_column: Name of amount column
            
        Returns:
            Dataframe with amount features added
        """
        if not config.ENGINEER_AMOUNT_FEATURES:
            return df
        
        if amount_column not in df.columns:
            self.logger.warning(f"Amount column '{amount_column}' not found")
            return df
        
        self.logger.info("Engineering amount features...")
        
        # Log transformation
        df['Amount_log'] = np.log1p(df[amount_column])
        
        # Amount bins
        df['Amount_bin'] = pd.qcut(df[amount_column], q=10, labels=False, duplicates='drop')
        
        # Amount categories
        df['IsSmallAmount'] = (df[amount_column] < df[amount_column].quantile(0.25)).astype(int)
        df['IsLargeAmount'] = (df[amount_column] > df[amount_column].quantile(0.75)).astype(int)
        
        # Amount statistics
        df['Amount_zscore'] = np.abs((df[amount_column] - df[amount_column].mean()) / df[amount_column].std())
        
        self.logger.info("Amount features engineered")
        return df
    
    def engineer_interaction_features(self, X: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
        """
        Engineer interaction features between top features.
        
        Args:
            X: Input dataframe with features
            top_n: Number of top features to use for interactions
            
        Returns:
            Dataframe with interaction features added
        """
        if not config.ENGINEER_INTERACTION_FEATURES:
            return X
        
        self.logger.info("Engineering interaction features...")
        
        # Select top numeric features by variance
        numeric_cols = X.select_dtypes(include=[np.number]).columns
        variances = X[numeric_cols].var().sort_values(ascending=False)
        top_features = variances.head(top_n).index.tolist()
        
        # Create interaction features
        interaction_count = 0
        for i in range(len(top_features)):
            for j in range(i + 1, len(top_features)):
                feature1, feature2 = top_features[i], top_features[j]
                interaction_name = f"{feature1}_X_{feature2}"
                X[interaction_name] = X[feature1] * X[feature2]
                interaction_count += 1
        
        self.logger.info(f"Created {interaction_count} interaction features")
        return X
    
    def apply_pca(self, X_train: pd.DataFrame, X_test: pd.DataFrame = None, 
                 n_components: int = None) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Apply Principal Component Analysis for dimensionality reduction.
        
        Args:
            X_train: Training features
            X_test: Test features
            n_components: Number of components (if None, uses config)
            
        Returns:
            Tuple of (transformed_train, transformed_test)
        """
        if not config.USE_PCA:
            return X_train.values, X_test.values if X_test is not None else None
        
        if n_components is None:
            n_components = config.PCA_COMPONENTS
        
        self.logger.info(f"Applying PCA with {n_components} components...")
        
        self.pca = PCA(n_components=n_components, random_state=config.RANDOM_STATE)
        X_train_pca = self.pca.fit_transform(X_train)
        
        # Calculate explained variance
        explained_variance = self.pca.explained_variance_ratio_.sum()
        self.logger.info(f"Explained variance: {explained_variance:.4f}")
        
        X_test_pca = None
        if X_test is not None:
            X_test_pca = self.pca.transform(X_test)
        
        return X_train_pca, X_test_pca
    
    def create_polynomial_features(self, X_train: np.ndarray, X_test: np.ndarray = None, 
                                  degree: int = 2) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Create polynomial features.
        
        Args:
            X_train: Training features
            X_test: Test features
            degree: Polynomial degree
            
        Returns:
            Tuple of (transformed_train, transformed_test)
        """
        self.logger.info(f"Creating polynomial features with degree {degree}...")
        
        self.polynomial_features = PolynomialFeatures(degree=degree, include_bias=False)
        X_train_poly = self.polynomial_features.fit_transform(X_train)
        
        X_test_poly = None
        if X_test is not None:
            X_test_poly = self.polynomial_features.transform(X_test)
        
        self.logger.info(f"Polynomial features shape: {X_train_poly.shape}")
        return X_train_poly, X_test_poly
    
    def handle_categorical_features(self, X: pd.DataFrame, method: str = "onehot") -> pd.DataFrame:
        """
        Handle categorical features.
        
        Args:
            X: Input dataframe
            method: Encoding method ('onehot' or 'label')
            
        Returns:
            Dataframe with categorical features encoded
        """
        categorical_cols = X.select_dtypes(include=['object']).columns
        
        if len(categorical_cols) == 0:
            return X
        
        self.logger.info(f"Encoding {len(categorical_cols)} categorical features...")
        
        if method == "onehot":
            X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
        elif method == "label":
            from sklearn.preprocessing import LabelEncoder
            le = LabelEncoder()
            for col in categorical_cols:
                X[col] = le.fit_transform(X[col])
        
        return X
    
    def scale_features_robust(self, X_train: np.ndarray, X_test: np.ndarray = None) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Scale features using RobustScaler (resistant to outliers).
        
        Args:
            X_train: Training features
            X_test: Test features
            
        Returns:
            Tuple of (scaled_train, scaled_test)
        """
        from sklearn.preprocessing import RobustScaler
        
        self.logger.info("Scaling features using RobustScaler...")
        
        scaler = RobustScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        
        X_test_scaled = None
        if X_test is not None:
            X_test_scaled = scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled
    
    def engineer_statistical_features(self, X: pd.DataFrame, window_size: int = 10) -> pd.DataFrame:
        """
        Engineer statistical features using rolling windows.
        
        Args:
            X: Input dataframe
            window_size: Size of rolling window
            
        Returns:
            Dataframe with statistical features added
        """
        self.logger.info("Engineering statistical features...")
        
        numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) == 0:
            return X
        
        # Rolling statistics
        X['Rolling_Mean'] = X[numeric_cols].rolling(window=window_size).mean().fillna(0)
        X['Rolling_Std'] = X[numeric_cols].rolling(window=window_size).std().fillna(0)
        
        # Expanding statistics
        X['Expanding_Mean'] = X[numeric_cols].expanding().mean()
        X['Expanding_Std'] = X[numeric_cols].expanding().std().fillna(0)
        
        self.logger.info("Statistical features engineered")
        return X
    
    def get_feature_importance_correlation(self, X: pd.DataFrame, y: np.ndarray, top_n: int = 20) -> pd.DataFrame:
        """
        Get correlation-based feature importance.
        
        Args:
            X: Features dataframe
            y: Target array
            top_n: Number of top features to return
            
        Returns:
            Dataframe with feature importance
        """
        self.logger.info("Computing correlation-based feature importance...")
        
        # Create temporary dataframe with target
        X_temp = X.copy()
        X_temp['Target'] = y
        
        # Calculate correlation with target
        correlation = X_temp.corr()['Target'].drop('Target').abs().sort_values(ascending=False)
        
        importance_df = pd.DataFrame({
            'Feature': correlation.index,
            'Correlation': correlation.values
        }).head(top_n)
        
        self.logger.info(f"\nTop {top_n} Features by Correlation:")
        self.logger.info(importance_df.to_string())
        
        return importance_df
    
    def select_features(self, X: pd.DataFrame, y: np.ndarray, method: str = "variance", 
                       threshold: float = 0.01) -> pd.DataFrame:
        """
        Select features based on various methods.
        
        Args:
            X: Features dataframe
            y: Target array
            method: Selection method ('variance', 'mutual_info', 'chi2')
            threshold: Selection threshold
            
        Returns:
            Dataframe with selected features
        """
        from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif, VarianceThreshold
        
        self.logger.info(f"Selecting features using {method} method...")
        
        if method == "variance":
            selector = VarianceThreshold(threshold=threshold)
            X_selected = selector.fit_transform(X)
            selected_features = X.columns[selector.get_support()].tolist()
        
        elif method == "mutual_info":
            selector = SelectKBest(score_func=mutual_info_classif, k=min(20, X.shape[1]))
            X_selected = selector.fit_transform(X, y)
            selected_features = X.columns[selector.get_support()].tolist()
        
        elif method == "chi2":
            # Chi2 requires non-negative features
            X_pos = X - X.min() + 1e-10
            selector = SelectKBest(score_func=lambda X, y: (np.abs(f_classif(X, y)[1]),), k=min(20, X.shape[1]))
            X_selected = selector.fit_transform(X_pos, y)
            selected_features = X.columns[selector.get_support()].tolist()
        
        else:
            raise ValueError(f"Unknown method: {method}")
        
        self.logger.info(f"Selected {len(selected_features)} features")
        return X[selected_features]
    
    def complete_feature_engineering(self, X_train: pd.DataFrame, X_test: pd.DataFrame = None) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Complete feature engineering pipeline.
        
        Args:
            X_train: Training features
            X_test: Test features
            
        Returns:
            Tuple of (engineered_train, engineered_test)
        """
        self.logger.info("Starting complete feature engineering pipeline...")
        
        # Engineer time features
        X_train = self.engineer_time_features(X_train)
        if X_test is not None:
            X_test = self.engineer_time_features(X_test)
        
        # Engineer amount features
        X_train = self.engineer_amount_features(X_train)
        if X_test is not None:
            X_test = self.engineer_amount_features(X_test)
        
        # Engineer interaction features
        X_train = self.engineer_interaction_features(X_train)
        if X_test is not None:
            X_test = self.engineer_interaction_features(X_test)
        
        # Handle categorical features
        X_train = self.handle_categorical_features(X_train)
        if X_test is not None:
            X_test = self.handle_categorical_features(X_test)
        
        # Apply PCA
        X_train_final, X_test_final = self.apply_pca(X_train, X_test)
        
        self.logger.info("Feature engineering pipeline completed!")
        
        return X_train_final, X_test_final


if __name__ == "__main__":
    logger = setup_logging(__name__)
    logger.info("Feature Engineering module loaded successfully")
