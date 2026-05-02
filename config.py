"""
Configuration Settings for Fraud Detection System
"""

import os
from pathlib import Path

# Project Directories
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
ANALYSIS_DATA_DIR = DATA_DIR / "analysis"
MODELS_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"
OUTPUT_DIR = PROJECT_ROOT / "output"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

# Create directories if they don't exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, ANALYSIS_DATA_DIR, MODELS_DIR, LOGS_DIR, OUTPUT_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Dataset Configuration
DATASET_PATH = RAW_DATA_DIR / "creditcard.csv"
RANDOM_STATE = 42
TEST_SIZE = 0.2
VALIDATION_SIZE = 0.1

# Feature Configuration
TARGET_COLUMN = "Class"
FRAUD_LABEL = 1
LEGITIMATE_LABEL = 0

# Preprocessing Configuration
NORMALIZE_FEATURES = True
HANDLE_MISSING_VALUES = True
REMOVE_OUTLIERS = False
OUTLIER_METHOD = "iqr"  # 'iqr' or 'zscore'

# Feature Engineering Configuration
ENGINEER_TIME_FEATURES = True
ENGINEER_AMOUNT_FEATURES = True
ENGINEER_INTERACTION_FEATURES = False
USE_PCA = False
PCA_COMPONENTS = 20

# Class Imbalance Handling
HANDLE_IMBALANCE = True
IMBALANCE_METHOD = "smote"  # 'smote', 'adasyn', 'random_over_sampling', 'class_weights'
SMOTE_RATIO = 0.3  # Ratio of minority class samples to generate
RANDOM_STATE_SMOTE = 42

# Model Configuration
MODELS_TO_TRAIN = [
    "logistic_regression",
    "decision_tree",
    "random_forest",
    "gradient_boosting",
    "xgboost",
    "lightgbm",
    "neural_network",
    "isolation_forest",
    "local_outlier_factor",
]

# Model Hyperparameters
HYPERPARAMETERS = {
    "logistic_regression": {
        "C": 1.0,
        "penalty": "l2",
        "solver": "lbfgs",
        "max_iter": 1000,
    },
    "decision_tree": {
        "max_depth": 10,
        "min_samples_split": 10,
        "min_samples_leaf": 5,
        "random_state": RANDOM_STATE,
    },
    "random_forest": {
        "n_estimators": 100,
        "max_depth": 15,
        "min_samples_split": 10,
        "min_samples_leaf": 5,
        "random_state": RANDOM_STATE,
        "n_jobs": -1,
    },
    "gradient_boosting": {
        "n_estimators": 100,
        "learning_rate": 0.1,
        "max_depth": 5,
        "min_samples_split": 10,
        "min_samples_leaf": 5,
        "random_state": RANDOM_STATE,
    },
    "xgboost": {
        "n_estimators": 100,
        "learning_rate": 0.1,
        "max_depth": 6,
        "min_child_weight": 1,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "random_state": RANDOM_STATE,
    },
    "lightgbm": {
        "n_estimators": 100,
        "learning_rate": 0.1,
        "max_depth": 6,
        "num_leaves": 31,
        "min_data_in_leaf": 20,
        "random_state": RANDOM_STATE,
    },
    "neural_network": {
        "hidden_layers": [128, 64, 32],
        "activation": "relu",
        "dropout_rate": 0.3,
        "learning_rate": 0.001,
        "batch_size": 32,
        "epochs": 50,
        "validation_split": 0.2,
    },
    "isolation_forest": {
        "contamination": 0.001,
        "n_estimators": 100,
        "random_state": RANDOM_STATE,
        "n_jobs": -1,
    },
    "local_outlier_factor": {
        "n_neighbors": 20,
        "contamination": 0.001,
    },
}

# Anomaly Detection Configuration
ANOMALY_DETECTION_METHODS = ["isolation_forest", "local_outlier_factor", "if"]
CONTAMINATION_RATIO = 0.001  # Expected fraud rate

# Model Evaluation Configuration
CROSS_VALIDATION_FOLDS = 5
METRICS_TO_COMPUTE = [
    "accuracy",
    "precision",
    "recall",
    "f1",
    "roc_auc",
    "pr_auc",
    "confusion_matrix",
]

# Threshold Optimization
OPTIMIZE_THRESHOLD = True
THRESHOLD_OPTIMIZATION_METRIC = "f1"  # 'f1', 'precision_recall', 'youden'

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "fraud_detection.log"

# Visualization Configuration
PLOT_FORMAT = "png"  # 'png', 'pdf', 'svg'
DPI = 300
FIGURE_SIZE = (12, 8)
STYLE = "seaborn-v0_8-darkgrid"

# Real-time Monitoring Configuration
ENABLE_REAL_TIME_MONITORING = False
MONITORING_ALERT_THRESHOLD = 0.7  # Risk score threshold for alerts
MAX_TRANSACTIONS_PER_BATCH = 1000
BATCH_PROCESSING_TIMEOUT = 60  # seconds

# Feature Importance Configuration
COMPUTE_FEATURE_IMPORTANCE = True
FEATURE_IMPORTANCE_METHOD = "permutation"  # 'permutation', 'shap'
TOP_N_FEATURES = 20

# Experiment Tracking
TRACK_EXPERIMENTS = True
EXPERIMENT_NAME = "fraud_detection_baseline"
SAVE_BEST_MODEL = True
BEST_MODEL_METRIC = "roc_auc"

# API Configuration (for future deployment)
API_HOST = "0.0.0.0"
API_PORT = 5000
API_DEBUG = False

# Data Configuration
DATA_ENCODING = "utf-8"
MISSING_VALUE_THRESHOLD = 0.5  # Drop columns with >50% missing values

# Performance Optimization
USE_GPU = False
N_JOBS = -1  # Use all available processors
BATCH_SIZE_PREDICTION = 10000

# Model Deployment
MODEL_VERSION = "1.0.0"
MODEL_FRAMEWORK = "scikit-learn"  # 'scikit-learn', 'xgboost', 'tensorflow'

# Audit and Compliance
AUDIT_LOGGING = True
COMPLIANCE_MODE = False  # Enable for GDPR/PCI compliance
ENCRYPTION_ENABLED = False

print("Configuration loaded successfully!")
