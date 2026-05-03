"""
Generate Interactive Dashboards for Fraud Detection System
"""

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_curve, auc, confusion_matrix

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
from src.utils import setup_logging
from src.preprocessing import DataPreprocessor
from src.models import ModelTrainer
from src.dashboard import InteractiveDashboard
from src.power_bi_export import PowerBIExporter


def generate_interactive_dashboards(X_train, X_test, y_train, y_test, 
                                    trained_models, results):
    """
    Generate interactive Plotly dashboards.
    
    Args:
        X_train: Training features
        X_test: Test features
        y_train: Training labels
        y_test: Test labels
        trained_models: Dictionary of trained models
        results: Model evaluation results
    """
    logger = setup_logging("dashboard_generator")
    logger.info("Generating interactive dashboards...")
    
    dashboard = InteractiveDashboard()
    
    # 1. Class Distribution
    logger.info("Creating class distribution chart...")
    fig_dist = dashboard.create_class_distribution_chart(y_test)
    dashboard.save_interactive_html(fig_dist, "01_class_distribution.html")
    
    # 2. Feature Correlation
    logger.info("Creating feature correlation chart...")
    fig_corr = dashboard.create_feature_correlation_chart(X_test, y_test, top_n=15)
    dashboard.save_interactive_html(fig_corr, "02_feature_correlation.html")
    
    # 3. Model Comparison
    logger.info("Creating model comparison chart...")
    fig_models = dashboard.create_model_comparison_chart(results, metric='f1')
    dashboard.save_interactive_html(fig_models, "03_model_comparison_f1.html")
    
    fig_models_auc = dashboard.create_model_comparison_chart(results, metric='roc_auc')
    dashboard.save_interactive_html(fig_models_auc, "04_model_comparison_roc_auc.html")
    
    # 4. ROC Curves and Confusion Matrices
    for model_name, model in trained_models.items():
        if model_name not in results:
            continue
        
        y_pred = model.predict(X_test)
        
        try:
            if hasattr(model, 'predict_proba'):
                y_pred_proba = model.predict_proba(X_test)
            elif hasattr(model, 'decision_function'):
                y_pred_proba = model.decision_function(X_test)
            else:
                y_pred_proba = None
            
            if y_pred_proba is not None:
                if len(y_pred_proba.shape) > 1:
                    y_pred_proba = y_pred_proba[:, 1]
                
                fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
                roc_auc = auc(fpr, tpr)
                
                fig_roc = dashboard.create_roc_curve_chart(fpr, tpr, roc_auc, model_name)
                dashboard.save_interactive_html(fig_roc, f"roc_curve_{model_name}.html")
        except Exception as e:
            logger.warning(f"Could not create ROC curve for {model_name}: {str(e)}")
        
        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        fig_cm = dashboard.create_confusion_matrix_heatmap(cm, model_name)
        dashboard.save_interactive_html(fig_cm, f"confusion_matrix_{model_name}.html")
    
    # 5. Amount Distribution
    logger.info("Creating amount distribution chart...")
    if 'Amount' in X_test.columns:
        fig_amount = dashboard.create_amount_distribution_chart(X_test, y_test)
        if fig_amount:
            dashboard.save_interactive_html(fig_amount, "05_amount_distribution.html")
    
    # 6. Time Distribution
    logger.info("Creating time distribution chart...")
    if 'Time' in X_test.columns:
        fig_time = dashboard.create_time_distribution_chart(X_test, y_test)
        if fig_time:
            dashboard.save_interactive_html(fig_time, "06_time_distribution.html")
    
    # 7. Create main dashboard HTML
    logger.info("Creating main dashboard HTML...")
    dashboard.create_dashboard_html()
    
    logger.info(f"✓ Interactive dashboards created in {config.OUTPUT_DIR}")


def export_for_powerbi(X_test, y_test, y_pred, y_pred_proba, 
                       trained_models, results, feature_names=None):
    """
    Export all data for Power BI integration.
    
    Args:
        X_test: Test features
        y_test: Test labels
        y_pred: Predictions
        y_pred_proba: Prediction probabilities
        trained_models: Dictionary of trained models
        results: Model evaluation results
        feature_names: List of feature names
    """
    logger = setup_logging("powerbi_exporter")
    logger.info("Exporting data for Power BI...")
    
    exporter = PowerBIExporter()
    
    cm = confusion_matrix(y_test, y_pred)
    best_model = max(results.items(), key=lambda x: x[1].get('f1', 0))[0]
    
    exported = exporter.export_all(
        results=results,
        y_true=y_test,
        y_pred=y_pred,
        y_pred_proba=y_pred_proba,
        X=X_test,
        feature_names=feature_names or [f"Feature_{i}" for i in range(X_test.shape[1])],
        cm=cm,
        model_name=best_model
    )
    
    logger.info("✓ Power BI exports created:")
    for export_type, path in exported.items():
        logger.info(f"  - {export_type}: {path}")
    
    return exported


if __name__ == "__main__":
    logger = setup_logging("main", config.LOG_LEVEL)
    
    # Check if dataset exists
    if not config.DATASET_PATH.exists():
        logger.error(f"Dataset not found at {config.DATASET_PATH}")
        logger.info("Please download from: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud")
        sys.exit(1)
    
    try:
        # Load and preprocess data
        logger.info("Loading and preprocessing data...")
        preprocessor = DataPreprocessor()
        X_train, X_test, y_train, y_test = preprocessor.prepare_data(config.DATASET_PATH)
        
        # Train models
        logger.info("Training models...")
        trainer = ModelTrainer()
        trained_models = trainer.train_all_models(X_train, y_train)
        
        # Evaluate and get results
        logger.info("Evaluating models...")
        from src.evaluation import ModelEvaluator
        evaluator = ModelEvaluator()
        
        best_model = None
        best_f1 = 0
        y_pred_best = None
        y_pred_proba_best = None
        
        results = {}
        for model_name, model in trained_models.items():
            y_pred = model.predict(X_test)
            
            y_pred_proba = None
            try:
                if hasattr(model, 'predict_proba'):
                    y_pred_proba = model.predict_proba(X_test)
                elif hasattr(model, 'decision_function'):
                    y_pred_proba = model.decision_function(X_test)
            except:
                pass
            
            metrics = evaluator.evaluate_model(model_name, y_test, y_pred, y_pred_proba)
            results[model_name] = metrics
            
            if metrics.get('f1', 0) > best_f1:
                best_f1 = metrics['f1']
                best_model = model_name
                y_pred_best = y_pred
                y_pred_proba_best = y_pred_proba
        
        # Generate interactive dashboards
        logger.info("\n" + "="*80)
        logger.info("GENERATING INTERACTIVE DASHBOARDS")
        logger.info("="*80)
        generate_interactive_dashboards(X_train, X_test, y_train, y_test, 
                                       trained_models, results)
        
        # Export for Power BI
        logger.info("\n" + "="*80)
        logger.info("EXPORTING FOR POWER BI")
        logger.info("="*80)
        export_for_powerbi(X_test, y_test, y_pred_best, y_pred_proba_best,
                          trained_models, results, 
                          feature_names=preprocessor.get_feature_names())
        
        logger.info("\n" + "="*80)
        logger.info("✓ DASHBOARDS AND EXPORTS COMPLETED SUCCESSFULLY!")
        logger.info("="*80)
        logger.info(f"\n📊 Interactive Dashboards: {config.OUTPUT_DIR}")
        logger.info(f"📈 Power BI Exports: {config.OUTPUT_DIR}")
        logger.info(f"\nOpen dashboard.html in your browser to view interactive charts!")
        logger.info(f"Import Excel files into Power BI Desktop for advanced analytics!")
        
    except Exception as e:
        logger.error(f"Error generating dashboards: {str(e)}", exc_info=True)
        sys.exit(1)
