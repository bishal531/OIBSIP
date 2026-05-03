"""
Main Execution Script for Fraud Detection System
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from config import *
from src.utils import setup_logging, save_results, PerformanceTracker
from src.preprocessing import DataPreprocessor
from src.feature_engineering import FeatureEngineer
from src.models import ModelTrainer, AnomalyDetector
from src.evaluation import ModelEvaluator
from src.anomaly_detection import AnomalyDetectionEngine


def main():
    """Main execution pipeline."""
    
    logger = setup_logging("main", config.LOG_LEVEL)
    logger.info("="*80)
    logger.info("FRAUD DETECTION SYSTEM - MAIN EXECUTION")
    logger.info("="*80)
    
    try:
        # Step 1: Data Preprocessing
        logger.info("\n[STEP 1] DATA PREPROCESSING")
        logger.info("-"*80)
        preprocessor = DataPreprocessor()
        
        # Check if dataset exists
        if not DATASET_PATH.exists():
            logger.error(f"Dataset not found at {DATASET_PATH}")
            logger.info("Please download the dataset from Kaggle:")
            logger.info("https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud")
            logger.info(f"And place creditcard.csv in {RAW_DATA_DIR}/")
            return
        
        X_train, X_test, y_train, y_test = preprocessor.prepare_data(DATASET_PATH)
        logger.info(f"✓ Data preprocessing completed")
        logger.info(f"  Train shape: {X_train.shape}, Test shape: {X_test.shape}")
        
        # Step 2: Feature Engineering
        logger.info("\n[STEP 2] FEATURE ENGINEERING")
        logger.info("-"*80)
        feature_engineer = FeatureEngineer()
        
        # For demonstration, we'll use the preprocessed data as-is
        logger.info("✓ Features prepared for model training")
        
        # Step 3: Model Training
        logger.info("\n[STEP 3] MODEL TRAINING")
        logger.info("-"*80)
        trainer = ModelTrainer()
        trained_models = trainer.train_all_models(X_train, y_train)
        logger.info(f"✓ Trained {len(trained_models)} models")
        
        # Step 4: Model Evaluation
        logger.info("\n[STEP 4] MODEL EVALUATION")
        logger.info("-"*80)
        evaluator = ModelEvaluator()
        performance_tracker = PerformanceTracker()
        
        for model_name, model in trained_models.items():
            # Get predictions
            y_pred = model.predict(X_test)
            
            # Get probabilities if available
            y_pred_proba = None
            try:
                if hasattr(model, 'predict_proba'):
                    y_pred_proba = model.predict_proba(X_test)
                elif hasattr(model, 'decision_function'):
                    y_pred_proba = model.decision_function(X_test)
            except:
                pass
            
            # Evaluate
            metrics = evaluator.evaluate_model(model_name, y_test, y_pred, y_pred_proba)
            performance_tracker.add_result("baseline", model_name, metrics)
            
            # Generate visualizations
            if config.COMPUTE_FEATURE_IMPORTANCE:
                evaluator.plot_confusion_matrix(y_test, y_pred, model_name)
                if y_pred_proba is not None:
                    evaluator.plot_roc_curve(y_test, y_pred_proba, model_name)
                    evaluator.plot_precision_recall_curve(y_test, y_pred_proba, model_name)
        
        # Model comparison
        logger.info("\n[STEP 5] MODEL COMPARISON")
        logger.info("-"*80)
        best_model = evaluator.get_best_model("f1")
        logger.info(f"✓ Best model: {best_model} (by F1-score)")
        
        evaluator.plot_model_comparison("f1")
        evaluator.plot_model_comparison("roc_auc")
        
        # Step 5: Anomaly Detection
        logger.info("\n[STEP 6] ANOMALY DETECTION")
        logger.info("-"*80)
        anomaly_engine = AnomalyDetectionEngine()
        anomaly_engine.train_all_detectors(X_train)
        logger.info("✓ Anomaly detectors trained")
        
        # Detect anomalies
        ensemble_predictions = anomaly_engine.ensemble_detection(X_test)
        anomaly_proba = anomaly_engine.get_anomaly_probability(X_test)
        logger.info(f"✓ Detected {ensemble_predictions.sum()} anomalies in test set")
        
        # Step 6: Save Results
        logger.info("\n[STEP 7] SAVING RESULTS")
        logger.info("-"*80)
        
        # Save models
        trainer.save_trained_models()
        logger.info("✓ Models saved")
        
        # Save performance metrics
        results_dict = {
            "models": evaluator.results,
            "best_model": best_model,
            "anomalies_detected": int(ensemble_predictions.sum()),
        }
        save_results(results_dict, OUTPUT_DIR / "performance_metrics.json")
        logger.info("✓ Performance metrics saved")
        
        # Generate summary report
        logger.info("\n[STEP 8] SUMMARY REPORT")
        logger.info("-"*80)
        comparison_df = evaluator.compare_models("f1")
        logger.info("\nModel Comparison Summary:")
        logger.info(comparison_df.to_string())
        
        logger.info("\n" + "="*80)
        logger.info("✓ FRAUD DETECTION PIPELINE COMPLETED SUCCESSFULLY!")
        logger.info("="*80)
        logger.info(f"\nResults saved to: {OUTPUT_DIR}")
        logger.info(f"Models saved to: {MODELS_DIR}")
        logger.info(f"Logs saved to: {LOG_FILE}")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    import config
    main()
