# Fraud Detection System - Getting Started Guide

## Quick Setup (5 minutes)

### 1. Install Dependencies
```bash
cd frauddetection
pip install -r requirements.txt
```

### 2. Download Dataset
1. Go to [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
2. Sign in (create account if needed)
3. Click "Download"
4. Unzip and place `creditcard.csv` in `data/raw/` folder

### 3. Run the Pipeline
```bash
python main.py
```

This will:
- Load and preprocess data
- Train multiple ML models
- Evaluate performance
- Generate visualizations
- Save results

### 4. View Results
- Check `output/` folder for visualizations
- Check `logs/fraud_detection.log` for details
- Models saved in `models/` folder

## Exploratory Analysis (Jupyter)

```bash
jupyter notebook notebooks/01_data_exploration.ipynb
```

Then run cells sequentially to:
1. Load and explore dataset
2. Analyze class distribution (highly imbalanced!)
3. Examine feature patterns
4. Understand fraud vs legitimate patterns

## Key Findings

📊 **Dataset**: 284,807 transactions, 492 frauds (0.17%)
🔴 **Challenge**: Class imbalance (1 fraud per 578 legitimate)
💡 **Solution**: SMOTE, ensemble models, threshold optimization
✅ **Expected F1-Score**: 0.80-0.85 with proper tuning

## Project Structure

```
frauddetection/
├── data/               # Dataset folder
├── src/               # Core modules
│   ├── preprocessing.py      # Data cleaning
│   ├── feature_engineering.py # Feature creation
│   ├── models.py             # Model training
│   ├── evaluation.py         # Model evaluation
│   └── anomaly_detection.py  # Anomaly detection
├── notebooks/         # Jupyter notebooks
├── models/           # Trained models
├── output/           # Results & visualizations
├── config.py         # Configuration
├── main.py          # Main pipeline
└── requirements.txt # Dependencies
```

## Advanced Configuration

Edit `config.py` to:
- Change model hyperparameters
- Adjust preprocessing settings
- Configure anomaly detection methods
- Enable/disable features

## Next Steps

1. ✅ **Data Exploration**: Run the Jupyter notebook
2. 🏋️ **Model Training**: Execute `python main.py`
3. 📊 **Hyperparameter Tuning**: Modify `config.py`
4. 🚀 **Deployment**: Create REST API or batch processor
5. 📈 **Monitoring**: Track model performance over time

## Troubleshooting

### Dataset not found
```
Error: Dataset not found at data/raw/creditcard.csv
Solution: Download from Kaggle and place in data/raw/
```

### Memory issues
```
Reduce BATCH_SIZE_PREDICTION in config.py
Use subset of data for initial testing
```

### Import errors
```
Make sure all dependencies are installed:
pip install -r requirements.txt --upgrade
```

## Resources

- 📚 [README.md](README.md) - Full documentation
- 🔗 [Kaggle Dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- 📖 [Scikit-learn Docs](https://scikit-learn.org/)
- 🎯 [XGBoost Documentation](https://xgboost.readthedocs.io/)

---

**Happy Fraud Detecting! 🔍**
