# Fraud Detection System

A comprehensive machine learning project for detecting fraudulent financial transactions using advanced analytics and anomaly detection techniques.

## Project Overview

This fraud detection system leverages machine learning algorithms to identify and prevent deceptive activities within financial transactions. The system implements:

- **Anomaly Detection**: Identifying unusual patterns and deviations from normal behavior
- **Machine Learning Models**: Logistic Regression, Decision Trees, Random Forest, Gradient Boosting, and Neural Networks
- **Feature Engineering**: Selecting and transforming relevant features for improved accuracy
- **Real-time Monitoring**: Systems designed for rapid fraud detection
- **Scalability**: Efficient processing of large transaction volumes

## Dataset

**Source**: [Credit Card Fraud Detection - Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)

- **Transactions**: 284,807 credit card transactions
- **Fraudulent**: 492 fraudulent transactions (0.172% of total)
- **Features**: 28 principal component analysis (PCA) transformed features + Time + Amount + Class
- **Class**: Binary classification (0: Legitimate, 1: Fraudulent)

**Data Characteristics**:
- Highly imbalanced dataset (class imbalance: 577:1)
- Features V1-V28: PCA-transformed features
- Time: Seconds elapsed between transaction and first transaction
- Amount: Transaction amount in USD

## Project Structure

```
frauddetection/
├── data/                          # Data storage
│   ├── raw/                      # Original dataset
│   ├── processed/                # Preprocessed data
│   └── analysis/                 # Analysis results
├── src/                          # Source code
│   ├── __init__.py
│   ├── preprocessing.py          # Data preprocessing
│   ├── feature_engineering.py    # Feature engineering
│   ├── models.py                 # Model definitions and training
│   ├── evaluation.py             # Model evaluation metrics
│   ├── anomaly_detection.py      # Anomaly detection algorithms
│   └── utils.py                  # Utility functions
├── notebooks/                    # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_model_training.ipynb
│   └── 05_evaluation.ipynb
├── models/                       # Trained model storage
├── logs/                         # Application logs
├── output/                       # Results and visualizations
├── config.py                     # Configuration settings
├── main.py                       # Main execution script
├── app.py                        # 🎨 Streamlit interactive dashboard
├── web_app.py                    # 🌐 Flask web application
├── run_dashboard.py              # 🚀 Streamlit runner script
├── setup_ui.py                   # 🎯 Interactive setup menu
├── generate_dashboards.py        # 📊 HTML dashboard generator
├── requirements.txt              # Python dependencies
├── GETTING_STARTED.md            # 📚 Quick start guide
├── UI_GUIDE.md                   # 🎨 Detailed UI documentation
├── POWERBI_GUIDE.md              # 💼 Power BI integration guide
├── POWERBI_SETUP.md              # 📊 Power BI setup tutorial
└── README.md                     # This file
```

## Key Features

### 1. Data Preprocessing
- Missing value handling
- Normalization and standardization
- Data validation and cleaning
- Train-test split with stratification

### 2. Feature Engineering
- Statistical features (mean, std, skewness, kurtosis)
- Time-based features (hour, day, month)
- Amount-based features (log transformation, binning)
- Interaction features
- PCA-preserved features analysis

### 3. Machine Learning Models
- **Logistic Regression**: Baseline model with interpretability
- **Decision Trees**: Non-linear patterns
- **Random Forest**: Ensemble with feature importance
- **Gradient Boosting (XGBoost/LightGBM)**: High-performance models
- **Neural Networks**: Deep learning approach
- **Isolation Forest**: Anomaly detection
- **Local Outlier Factor (LOF)**: Density-based anomaly detection

### 4. Evaluation Metrics
- **Accuracy**: Overall correctness
- **Precision**: True positive rate among predicted positives
- **Recall/Sensitivity**: True positive rate among actual positives
- **F1-Score**: Harmonic mean of precision and recall
- **ROC-AUC**: Trade-off between true positive and false positive rates
- **PR-AUC**: Precision-Recall curve area
- **Confusion Matrix**: Detailed classification breakdown

### 5. Handling Class Imbalance
- SMOTE (Synthetic Minority Over-sampling Technique)
- Class weights adjustment
- Threshold optimization
- Stratified cross-validation

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Setup Instructions

1. **Clone or extract the project**:
```bash
cd frauddetection
```

2. **Create virtual environment**:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Download dataset**:
- Download from [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- Place `creditcard.csv` in `data/raw/` folder

## Usage

### Running the Complete Pipeline

```bash
python main.py
```

This will:
1. Load and preprocess data
2. Engineer features
3. Train multiple models
4. Evaluate performance
5. Generate reports and visualizations
6. Save trained models

### Using Jupyter Notebooks

```bash
jupyter notebook notebooks/
```

## 🎨 Interactive Dashboards

The fraud detection system includes multiple interactive web interfaces for real-time monitoring and analysis.

### Quick Start - Choose Your Interface

#### 1. **Streamlit Dashboard** (Recommended) ⭐
```bash
streamlit run app.py
```
**Best for**: Most users, interactive exploration, quick insights
- 🎨 Beautiful dark theme interface
- 📊 Real-time interactive charts
- 🚀 One-click Power BI export
- 📱 Fully responsive design

#### 2. **Flask Web Application**
```bash
python web_app.py
```
**Best for**: Advanced users, custom hosting, API access
- 🌐 Modern web interface
- 🔌 REST API endpoints
- 🎯 Professional design
- 💼 Power BI integration

#### 3. **HTML Dashboards**
```bash
python generate_dashboards.py
```
**Best for**: Sharing, presentations, offline use
- 📄 Standalone HTML files
- 🔗 No server required
- 📤 Easy to email/share
- 💾 Persistent storage

#### 4. **Easy Setup Script**
```bash
python setup_ui.py
```
**Interactive menu** to choose and run your preferred interface

### Dashboard Features

#### Overview Page
- 📦 Total transactions count
- ⚠️ Fraud rate percentage
- ✅ Legitimate vs fraudulent distribution
- 📋 Dataset statistics

#### Data Analysis
- 🔗 Feature correlation with fraud
- 📊 Amount and time distributions
- 🔍 Fraud pattern detection
- 📈 Statistical insights

#### Model Training & Comparison
- 🤖 Train multiple ML models
- 📊 Performance comparison (F1, ROC-AUC, etc.)
- 🎯 ROC curves visualization
- ❌ Confusion matrices
- 📈 Detailed metrics tables

#### Power BI Export
- 📤 One-click data export
- 📊 Excel-ready files
- 💼 Power BI compatible format
- 🔄 Automatic file generation

## 💼 Power BI Integration

Export your fraud detection results directly to Microsoft Power BI for advanced business intelligence and real-time monitoring.

### Exported Data Files

| File | Contents | Purpose |
|------|----------|---------|
| `model_metrics.xlsx` | Performance metrics | KPI cards, comparisons |
| `predictions.xlsx` | Individual predictions | Trend analysis, filtering |
| `feature_statistics.xlsx` | Feature analysis | Statistical insights |
| `confusion_matrix_*.xlsx` | Classification breakdown | Performance review |

### Quick Power BI Setup

1. **Generate exports** from dashboard
2. **Open Power BI Desktop**
3. **Get Data** → Select `.xlsx` files
4. **Build visualizations** using imported data
5. **Publish** to Power BI Service
6. **Share** with stakeholders

[📚 Detailed Power BI Guide →](POWERBI_SETUP.md)

### Sample Power BI Dashboards

Create professional reports with:
- KPI cards showing key metrics
- Model comparison bar charts
- ROC curves for performance analysis
- Confusion matrix heatmaps
- Fraud pattern scatter plots
- Feature importance rankings
- Real-time monitoring alerts

Start with `01_data_exploration.ipynb` and proceed sequentially.

### Training Specific Models

```python
from src.models import ModelTrainer
from src.preprocessing import DataPreprocessor

# Load and preprocess data
preprocessor = DataPreprocessor()
X_train, X_test, y_train, y_test = preprocessor.prepare_data('data/raw/creditcard.csv')

# Train models
trainer = ModelTrainer()
trainer.train_all_models(X_train, y_train)
trainer.evaluate(X_test, y_test)
```

## Model Performance

Expected performance metrics on the test set:

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|-------|----------|-----------|--------|----------|---------|
| Logistic Regression | ~99.5% | ~75% | ~60% | ~67% | ~95% |
| Random Forest | ~99.7% | ~85% | ~75% | ~80% | ~97% |
| XGBoost | ~99.8% | ~90% | ~80% | ~85% | ~98% |
| Neural Network | ~99.8% | ~88% | ~82% | ~85% | ~98% |

*Note: Actual performance depends on data splits and random seeds*

## Real-time Monitoring

For real-time fraud detection:

```python
from src.models import FraudDetectionEngine

detector = FraudDetectionEngine(model_path='models/xgboost_model.pkl')

# Process individual transactions
transaction = {
    'Amount': 150.00,
    'Hour': 14,
    'DayOfWeek': 2,
    # ... other features
}

prediction = detector.predict_transaction(transaction)
if prediction['is_fraud']:
    print(f"Alert: Potential fraud detected. Risk score: {prediction['risk_score']}")
```

## Scalability Considerations

### For Large-Scale Production:

1. **Data Processing**:
   - Use Apache Spark for distributed processing
   - Implement batch and stream processing pipelines
   - Use data warehousing solutions (Snowflake, BigQuery)

2. **Model Deployment**:
   - REST API endpoints (Flask/FastAPI)
   - Model serving (TensorFlow Serving, Seldon Core)
   - Real-time prediction engines (Redis, DynamoDB)

3. **Monitoring**:
   - Model performance tracking
   - Drift detection
   - Automated retraining pipelines
   - Alerting systems

4. **Infrastructure**:
   - Containerization (Docker)
   - Orchestration (Kubernetes)
   - Cloud platforms (AWS SageMaker, Google AI Platform, Azure ML)

## Challenges Addressed

### 1. Class Imbalance
- **Problem**: Only 0.172% fraud rate
- **Solution**: SMOTE, weighted models, threshold tuning

### 2. Feature Privacy
- **Problem**: PCA-transformed features limit interpretability
- **Solution**: Feature importance analysis, SHAP values

### 3. Real-time Performance
- **Problem**: Model inference latency
- **Solution**: Model optimization, caching, batching

### 4. Concept Drift
- **Problem**: Fraud patterns evolve over time
- **Solution**: Regular model retraining, drift monitoring

### 5. False Positives
- **Problem**: Too many false alarms affect user experience
- **Solution**: Threshold optimization, risk scoring

## Technologies & Libraries

- **Data Processing**: Pandas, NumPy, Scikit-learn
- **Machine Learning**: Scikit-learn, XGBoost, LightGBM, TensorFlow/Keras
- **Anomaly Detection**: PyOD, Isolation Forest, LOF
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Notebooks**: Jupyter, JupyterLab
- **Model Evaluation**: Scikit-learn, Custom metrics
- **Utilities**: Python-dotenv, Logging, Joblib

## Performance Optimization

### Model Optimization
- Hyperparameter tuning (Grid Search, Random Search, Bayesian Optimization)
- Model ensemble techniques
- Feature selection and dimensionality reduction
- Early stopping and regularization

### Computational Optimization
- Vectorized operations with NumPy/Pandas
- Model compression and quantization
- Parallel processing with multiprocessing
- GPU acceleration for deep learning

## Contributing

1. Create a new branch for each feature
2. Implement changes with proper documentation
3. Add tests for new functionality
4. Submit pull request with clear description

## Future Enhancements

- [ ] Implement federated learning for privacy-preserving detection
- [ ] Add explainability with SHAP and LIME
- [ ] Develop automated retraining pipeline
- [ ] Create REST API for real-time predictions
- [ ] Build dashboard for monitoring
- [ ] Implement adversarial robustness testing
- [ ] Add graph neural networks for transaction networks

## License

MIT License - See LICENSE file for details

## References

1. Dal Pozzolo, A., Boracchi, G., Caelen, O., Alippi, C., & Bontempi, G. (2018). "Learned lessons in credit card fraud detection from class imbalance"
2. Kaggle Credit Card Fraud Detection Dataset
3. Scikit-learn Documentation
4. XGBoost Documentation

## Contact & Support

For questions or issues, please create an issue in the repository.

---

**Last Updated**: April 2026
**Project Status**: Active Development
