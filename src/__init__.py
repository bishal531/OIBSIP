"""
Fraud Detection System Package
"""

__version__ = "1.0.0"
__author__ = "Fraud Detection Team"
__description__ = "Advanced Machine Learning Fraud Detection System"

from src.preprocessing import DataPreprocessor
from src.feature_engineering import FeatureEngineer
from src.models import ModelTrainer
from src.evaluation import ModelEvaluator
from src.utils import setup_logging

__all__ = [
    "DataPreprocessor",
    "FeatureEngineer",
    "ModelTrainer",
    "ModelEvaluator",
    "setup_logging",
]
