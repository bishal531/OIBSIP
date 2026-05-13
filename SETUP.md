# Project Setup Guide

## Prerequisites
- Python 3.7 or higher
- Jupyter Notebook or JupyterLab
- Kaggle account (for downloading dataset)

## Installation Steps

### Step 1: Install Required Packages
```bash
pip install pandas numpy scikit-learn matplotlib seaborn scipy
```

### Step 2: Download Dataset from Kaggle

#### Option A: Using Kaggle API (Recommended)

1. **Install Kaggle CLI:**
```bash
pip install kaggle
```

2. **Set up Kaggle API credentials:**
   - Go to https://www.kaggle.com/settings/account
   - Click "Create New API Token"
   - This downloads `kaggle.json` file
   - Place it in `~/.kaggle/` directory (create if doesn't exist)
   - On Windows: `C:\Users\<YourUsername>\.kaggle\`
   - On Mac/Linux: `~/.kaggle/`

3. **Download the dataset:**
```bash
kaggle datasets download ashydv/housing-price-prediction-linear-regression -p ./data/
cd data/
unzip -q housing-price-prediction-linear-regression.zip
rm housing-price-prediction-linear-regression.zip
```

#### Option B: Manual Download

1. Visit: https://www.kaggle.com/code/ashydv/housing-price-prediction-linear-regression
2. Find the "Data" section
3. Download the dataset
4. Extract the files to the `data/` folder
5. Rename the CSV file to `train.csv` if necessary

### Step 3: Verify Dataset
Check that `data/train.csv` exists in your project directory.

### Step 4: Run the Notebook
```bash
jupyter notebook notebooks/house_price_prediction.ipynb
```

Or for JupyterLab:
```bash
jupyter lab notebooks/house_price_prediction.ipynb
```

## Project Structure After Setup
```
house prediction/
├── data/
│   └── train.csv                              # Dataset file
├── notebooks/
│   └── house_price_prediction.ipynb          # Main notebook
├── models/                                    # For saving trained models
├── README.md                                  # Project overview
└── SETUP.md                                   # This file
```

## Expected Dataset Format
The dataset should contain:
- Numerical features (various house characteristics)
- Target variable for house prices
- Comma-separated values (CSV) format

## Troubleshooting

### Issue: FileNotFoundError when loading data
**Solution:** Ensure `train.csv` is in the `data/` folder. Check the exact filename.

### Issue: ModuleNotFoundError
**Solution:** Install all required packages using the command above

### Issue: Kaggle API authentication error
**Solution:** 
- Verify kaggle.json is in the correct location
- Check file permissions
- Re-download the token from Kaggle

## Running the Notebook

1. All cells are designed to run sequentially
2. The notebook checks if data is loaded before executing analysis
3. Missing data is handled automatically
4. Follow the markdown sections for understanding each step

## Model Output
The notebook will generate:
- Statistical summaries and data descriptions
- Correlation analysis and visualizations
- Distribution plots and scatter plots
- Model performance metrics (MSE, RMSE, R²)
- Prediction visualizations
- Residual analysis plots
- Feature importance visualization

## Next Steps
After running the notebook:
1. Review the model performance metrics
2. Analyze feature coefficients
3. Examine visualization plots
4. Experiment with:
   - Different train-test splits
   - Feature scaling approaches
   - Adding polynomial features
   - Implementing regularization (Ridge/Lasso)

## Resources
- [Scikit-Learn Linear Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Matplotlib Visualization](https://matplotlib.org/)
- [Kaggle Dataset](https://www.kaggle.com/code/ashydv/housing-price-prediction-linear-regression)

## Support
If you encounter issues:
1. Check the troubleshooting section above
2. Review the notebook comments
3. Verify all dependencies are installed
4. Ensure dataset file is correctly placed
