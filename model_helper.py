"""
Housing Price Prediction Model Helper Script
This script provides utility functions for model training, prediction, and evaluation.
"""

import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import os

class HousingPricePredictor:
    """
    A class to encapsulate the housing price prediction model workflow.
    Handles data loading, preprocessing, model training, and predictions.
    """
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.target_name = None
        
    def load_data(self, filepath):
        """Load data from CSV file."""
        try:
            data = pd.read_csv(filepath)
            print(f"✓ Data loaded successfully. Shape: {data.shape}")
            return data
        except FileNotFoundError:
            print(f"✗ Error: File '{filepath}' not found.")
            return None
    
    def preprocess_data(self, df, target_col=None):
        """
        Preprocess the dataset:
        - Handle missing values
        - Remove duplicates
        - Encode categorical variables
        - Scale features
        """
        # Auto-detect target column if not provided
        if target_col is None:
            numerical_cols = df.select_dtypes(include=[np.number]).columns
            target_col = numerical_cols[-1]
            print(f"Auto-detected target column: {target_col}")
        
        self.target_name = target_col
        
        # Handle missing values
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        for col in numerical_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].median(), inplace=True)
        
        for col in categorical_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].mode()[0], inplace=True)
        
        # Remove duplicates
        df.drop_duplicates(inplace=True)
        
        # Encode categorical variables
        df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
        
        print(f"✓ Data preprocessed. New shape: {df.shape}")
        return df
    
    def prepare_features_target(self, df, target_col):
        """Separate features and target, apply scaling."""
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        # Store feature names
        self.feature_names = X.columns.tolist()
        
        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
        
        print(f"✓ Features prepared. Shape: {X_scaled.shape}")
        return X_scaled, y
    
    def train(self, X_train, y_train):
        """Train the linear regression model."""
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        print("✓ Model training completed!")
        
        train_r2 = r2_score(y_train, self.model.predict(X_train))
        print(f"  Training R² Score: {train_r2:.4f}")
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance on test data."""
        if self.model is None:
            print("✗ Model not trained yet!")
            return None
        
        y_pred = self.model.predict(X_test)
        
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        metrics = {
            'MAE': mae,
            'MSE': mse,
            'RMSE': rmse,
            'R2': r2
        }
        
        print("\n" + "="*50)
        print("MODEL EVALUATION METRICS")
        print("="*50)
        print(f"Mean Absolute Error (MAE):      ${mae:,.2f}")
        print(f"Mean Squared Error (MSE):       {mse:,.2f}")
        print(f"Root Mean Squared Error (RMSE): ${rmse:,.2f}")
        print(f"R² Score:                       {r2:.4f}")
        
        return metrics
    
    def predict(self, X_new):
        """Make predictions on new data."""
        if self.model is None:
            print("✗ Model not trained yet!")
            return None
        
        X_new_scaled = self.scaler.transform(X_new)
        predictions = self.model.predict(X_new_scaled)
        return predictions
    
    def save_model(self, filepath):
        """Save the trained model to a file."""
        if self.model is None:
            print("✗ No model to save!")
            return False
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'target_name': self.target_name
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"✓ Model saved to '{filepath}'")
        return True
    
    def load_model(self, filepath):
        """Load a previously trained model."""
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.feature_names = model_data['feature_names']
            self.target_name = model_data['target_name']
            
            print(f"✓ Model loaded from '{filepath}'")
            return True
        except FileNotFoundError:
            print(f"✗ Model file '{filepath}' not found!")
            return False
    
    def get_coefficients(self, top_n=10):
        """Get and display top feature coefficients."""
        if self.model is None:
            print("✗ Model not trained yet!")
            return None
        
        coef_df = pd.DataFrame({
            'Feature': self.feature_names,
            'Coefficient': self.model.coef_
        }).sort_values('Coefficient', key=abs, ascending=False)
        
        print(f"\nTop {top_n} Feature Coefficients:")
        print(coef_df.head(top_n).to_string(index=False))
        
        return coef_df


# Example usage function
def run_complete_pipeline(data_path='data/train.csv'):
    """Run the complete machine learning pipeline."""
    
    print("="*70)
    print("HOUSING PRICE PREDICTION - COMPLETE PIPELINE")
    print("="*70)
    
    # Initialize predictor
    predictor = HousingPricePredictor()
    
    # Load data
    df = predictor.load_data(data_path)
    if df is None:
        return
    
    # Preprocess
    df = predictor.preprocess_data(df)
    
    # Prepare features and target
    X, y = predictor.prepare_features_target(df, predictor.target_name)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=predictor.random_state
    )
    print(f"✓ Data split: {len(X_train)} training, {len(X_test)} testing samples")
    
    # Train model
    predictor.train(X_train, y_train)
    
    # Evaluate
    metrics = predictor.evaluate(X_test, y_test)
    
    # Display coefficients
    predictor.get_coefficients(top_n=10)
    
    # Save model
    os.makedirs('models', exist_ok=True)
    predictor.save_model('models/linear_regression_model.pkl')
    
    return predictor, X_test, y_test, metrics


if __name__ == "__main__":
    # Run the pipeline
    predictor, X_test, y_test, metrics = run_complete_pipeline()
    
    print("\n" + "="*70)
    print("Pipeline completed successfully!")
    print("Model saved to: models/linear_regression_model.pkl")
    print("="*70)
