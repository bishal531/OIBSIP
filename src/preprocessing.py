"""
Data Preprocessing Module for Fraud Detection System
"""

import logging
from pathlib import Path
from typing import Tuple, Optional

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split

import config
from src.utils import setup_logging, print_data_statistics


class DataPreprocessor:
    """Handle data loading, cleaning, and preprocessing."""
    
    def __init__(self):
        """Initialize the data preprocessor."""
        self.logger = setup_logging(__name__)
        self.scaler = StandardScaler() if config.NORMALIZE_FEATURES else None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.feature_names = None
    
    def load_data(self, filepath: Path) -> pd.DataFrame:
        """
        Load dataset from CSV file.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            Loaded dataframe
        """
        try:
            self.logger.info(f"Loading data from {filepath}")
            df = pd.read_csv(filepath, encoding=config.DATA_ENCODING)
            self.logger.info(f"Data loaded successfully. Shape: {df.shape}")
            return df
        except FileNotFoundError:
            self.logger.error(f"File not found: {filepath}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")
            raise
    
    def check_data_quality(self, df: pd.DataFrame) -> dict:
        """
        Check data quality and report issues.
        
        Args:
            df: Input dataframe
            
        Returns:
            Dictionary with quality metrics
        """
        quality_report = {
            "shape": df.shape,
            "missing_values": df.isnull().sum().to_dict(),
            "missing_percentage": (df.isnull().sum() / len(df) * 100).to_dict(),
            "duplicates": df.duplicated().sum(),
            "data_types": df.dtypes.to_dict(),
        }
        
        self.logger.info("Data Quality Report:")
        self.logger.info(f"  Shape: {quality_report['shape']}")
        self.logger.info(f"  Total missing values: {sum(quality_report['missing_values'].values())}")
        self.logger.info(f"  Duplicate rows: {quality_report['duplicates']}")
        
        return quality_report
    
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in dataset.
        
        Args:
            df: Input dataframe
            
        Returns:
            Dataframe with missing values handled
        """
        if not config.HANDLE_MISSING_VALUES:
            return df
        
        self.logger.info("Handling missing values...")
        
        # Drop columns with too many missing values
        missing_threshold = config.MISSING_VALUE_THRESHOLD
        cols_to_drop = df.columns[df.isnull().sum() / len(df) > missing_threshold]
        df = df.drop(columns=cols_to_drop)
        
        if len(cols_to_drop) > 0:
            self.logger.info(f"Dropped {len(cols_to_drop)} columns with >{missing_threshold*100}% missing values")
        
        # Fill remaining missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        
        categorical_cols = df.select_dtypes(include=['object']).columns
        df[categorical_cols] = df[categorical_cols].fillna(df[categorical_cols].mode()[0])
        
        self.logger.info(f"Missing values remaining: {df.isnull().sum().sum()}")
        return df
    
    def handle_outliers(self, df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
        """
        Handle outliers in dataset.
        
        Args:
            df: Input dataframe
            columns: Columns to check for outliers
            
        Returns:
            Dataframe with outliers handled
        """
        if not config.REMOVE_OUTLIERS:
            return df
        
        self.logger.info("Handling outliers...")
        
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns
        
        if config.OUTLIER_METHOD == "iqr":
            for col in columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
                df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
                
                if outliers > 0:
                    self.logger.info(f"  {col}: Removed {outliers} outliers")
        
        elif config.OUTLIER_METHOD == "zscore":
            from scipy import stats
            z_scores = np.abs(stats.zscore(df[columns]))
            df = df[(z_scores < 3).all(axis=1)]
            self.logger.info(f"Removed outliers using Z-score method")
        
        self.logger.info(f"Data shape after outlier handling: {df.shape}")
        return df
    
    def separate_features_target(self, df: pd.DataFrame, 
                                target_column: str = config.TARGET_COLUMN) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Separate features and target variable.
        
        Args:
            df: Input dataframe
            target_column: Name of target column
            
        Returns:
            Tuple of (features, target)
        """
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in dataframe")
        
        y = df[target_column]
        X = df.drop(columns=[target_column])
        
        self.logger.info(f"Separated features ({X.shape[1]}) and target")
        return X, y
    
    def normalize_features(self, X_train: pd.DataFrame, X_test: pd.DataFrame = None) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Normalize features using StandardScaler.
        
        Args:
            X_train: Training features
            X_test: Test features (optional)
            
        Returns:
            Tuple of (normalized_train, normalized_test)
        """
        if not config.NORMALIZE_FEATURES:
            return X_train, X_test
        
        self.logger.info("Normalizing features...")
        
        # Fit scaler on training data
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        X_test_scaled = None
        if X_test is not None:
            X_test_scaled = self.scaler.transform(X_test)
        
        self.logger.info("Features normalized successfully")
        return X_train_scaled, X_test_scaled
    
    def split_data(self, X: pd.DataFrame, y: pd.Series, 
                  test_size: float = config.TEST_SIZE,
                  random_state: int = config.RANDOM_STATE) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Split data into train and test sets with stratification.
        
        Args:
            X: Features
            y: Target
            test_size: Test set ratio
            random_state: Random seed
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        self.logger.info(f"Splitting data with test_size={test_size} and random_state={random_state}")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=test_size,
            random_state=random_state,
            stratify=y  # Stratify to maintain class distribution
        )
        
        self.logger.info(f"Train set: {X_train.shape}")
        self.logger.info(f"Test set: {X_test.shape}")
        self.logger.info(f"Train fraud rate: {y_train.sum() / len(y_train) * 100:.2f}%")
        self.logger.info(f"Test fraud rate: {y_test.sum() / len(y_test) * 100:.2f}%")
        
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        
        return X_train, X_test, y_train, y_test
    
    def prepare_data(self, filepath: Path = None, df: pd.DataFrame = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Complete preprocessing pipeline.
        
        Args:
            filepath: Path to data file (if df is None)
            df: Dataframe (if filepath is None)
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        self.logger.info("Starting complete preprocessing pipeline...")
        
        # Load data
        if df is None:
            if filepath is None:
                filepath = config.DATASET_PATH
            df = self.load_data(filepath)
        
        # Data quality check
        self.check_data_quality(df)
        
        # Handle missing values
        df = self.handle_missing_values(df)
        
        # Handle outliers
        df = self.handle_outliers(df)
        
        # Separate features and target
        X, y = self.separate_features_target(df)
        
        # Store feature names
        self.feature_names = X.columns.tolist()
        
        # Print statistics
        print_data_statistics(X, y)
        
        # Split data
        X_train, X_test, y_train, y_test = self.split_data(X, y)
        
        # Normalize features
        X_train_scaled, X_test_scaled = self.normalize_features(X_train, X_test)
        
        self.logger.info("Preprocessing pipeline completed successfully!")
        
        return X_train_scaled, X_test_scaled, y_train.values, y_test.values
    
    def get_feature_names(self) -> list:
        """Get list of feature names."""
        return self.feature_names
    
    def inverse_transform(self, X_scaled: np.ndarray) -> np.ndarray:
        """Inverse transform scaled features."""
        if self.scaler is None:
            return X_scaled
        return self.scaler.inverse_transform(X_scaled)


if __name__ == "__main__":
    logger = setup_logging(__name__)
    
    # Test the preprocessor
    preprocessor = DataPreprocessor()
    try:
        X_train, X_test, y_train, y_test = preprocessor.prepare_data(config.DATASET_PATH)
        print(f"\nPreprocessing completed successfully!")
        print(f"X_train shape: {X_train.shape}")
        print(f"X_test shape: {X_test.shape}")
    except FileNotFoundError:
        logger.warning("Dataset not found. Please download it from Kaggle and place it in data/raw/")
