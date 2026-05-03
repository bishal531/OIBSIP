"""
Model Evaluation Module for Fraud Detection System
"""

import logging
from typing import Dict, Any, Optional, List

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, auc, precision_recall_curve,
    confusion_matrix, classification_report, matthews_corrcoef
)
import matplotlib.pyplot as plt
import seaborn as sns

import config
from src.utils import setup_logging, optimize_threshold


class ModelEvaluator:
    """Evaluate and compare model performance."""
    
    def __init__(self):
        """Initialize the model evaluator."""
        self.logger = setup_logging(__name__)
        self.results = {}
        self.best_model = None
        self.best_metric = None
    
    def evaluate_model(self, model_name: str, y_true: np.ndarray, y_pred: np.ndarray,
                      y_pred_proba: Optional[np.ndarray] = None) -> Dict[str, float]:
        """
        Evaluate a single model.
        
        Args:
            model_name: Name of the model
            y_true: True labels
            y_pred: Predicted labels
            y_pred_proba: Prediction probabilities
            
        Returns:
            Dictionary of evaluation metrics
        """
        self.logger.info(f"Evaluating {model_name}...")
        
        metrics = {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1": f1_score(y_true, y_pred, zero_division=0),
            "matthews_corrcoef": matthews_corrcoef(y_true, y_pred),
        }
        
        # Calculate ROC-AUC if probabilities provided
        if y_pred_proba is not None and len(np.unique(y_true)) > 1:
            try:
                if len(y_pred_proba.shape) > 1:
                    y_pred_proba_binary = y_pred_proba[:, 1]
                else:
                    y_pred_proba_binary = y_pred_proba
                
                metrics["roc_auc"] = roc_auc_score(y_true, y_pred_proba_binary)
                
                # Calculate PR-AUC
                precision_vals, recall_vals, _ = precision_recall_curve(y_true, y_pred_proba_binary)
                metrics["pr_auc"] = auc(recall_vals, precision_vals)
            except Exception as e:
                self.logger.warning(f"Could not calculate ROC-AUC/PR-AUC: {str(e)}")
        
        # Confusion matrix
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        metrics["true_positives"] = int(tp)
        metrics["true_negatives"] = int(tn)
        metrics["false_positives"] = int(fp)
        metrics["false_negatives"] = int(fn)
        
        # Additional metrics
        metrics["specificity"] = tn / (tn + fp) if (tn + fp) > 0 else 0
        metrics["sensitivity"] = tp / (tp + fn) if (tp + fn) > 0 else 0
        metrics["fpr"] = fp / (fp + tn) if (fp + tn) > 0 else 0
        metrics["fnr"] = fn / (fn + tp) if (fn + tp) > 0 else 0
        
        self.results[model_name] = metrics
        
        self._log_metrics(model_name, metrics)
        
        return metrics
    
    def _log_metrics(self, model_name: str, metrics: Dict[str, float]) -> None:
        """Log metrics to logger."""
        self.logger.info(f"\n{'='*50}")
        self.logger.info(f"Evaluation Results for {model_name}")
        self.logger.info(f"{'='*50}")
        
        for key, value in metrics.items():
            if not key.startswith('_'):
                if isinstance(value, float):
                    self.logger.info(f"{key:.<30} {value:.4f}")
                else:
                    self.logger.info(f"{key:.<30} {value}")
    
    def compare_models(self, metric: str = "f1") -> pd.DataFrame:
        """
        Compare all evaluated models on a specific metric.
        
        Args:
            metric: Metric to compare (default: f1)
            
        Returns:
            Dataframe with model comparison sorted by metric
        """
        comparison_data = []
        
        for model_name, metrics in self.results.items():
            if metric in metrics:
                comparison_data.append({
                    "Model": model_name,
                    metric: metrics[metric],
                    "Accuracy": metrics.get("accuracy", None),
                    "Precision": metrics.get("precision", None),
                    "Recall": metrics.get("recall", None),
                    "F1": metrics.get("f1", None),
                    "ROC-AUC": metrics.get("roc_auc", None),
                })
        
        comparison_df = pd.DataFrame(comparison_data).sort_values(metric, ascending=False)
        
        self.logger.info(f"\n{'='*80}")
        self.logger.info(f"Model Comparison (sorted by {metric})")
        self.logger.info(f"{'='*80}")
        self.logger.info(comparison_df.to_string(index=False))
        
        return comparison_df
    
    def get_best_model(self, metric: str = "f1") -> str:
        """Get best model by metric."""
        comparison_df = self.compare_models(metric)
        if len(comparison_df) > 0:
            self.best_model = comparison_df.iloc[0]["Model"]
            self.best_metric = metric
            return self.best_model
        return None
    
    def plot_confusion_matrix(self, y_true: np.ndarray, y_pred: np.ndarray, 
                             model_name: str = "Model") -> None:
        """
        Plot confusion matrix.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            model_name: Model name for title
        """
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Legitimate', 'Fraudulent'],
                   yticklabels=['Legitimate', 'Fraudulent'])
        plt.title(f'Confusion Matrix - {model_name}')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        output_path = config.OUTPUT_DIR / f"confusion_matrix_{model_name}.png"
        plt.savefig(output_path, dpi=config.DPI, bbox_inches='tight')
        self.logger.info(f"Confusion matrix saved to {output_path}")
        plt.close()
    
    def plot_roc_curve(self, y_true: np.ndarray, y_pred_proba: np.ndarray,
                      model_name: str = "Model") -> None:
        """
        Plot ROC curve.
        
        Args:
            y_true: True labels
            y_pred_proba: Prediction probabilities
            model_name: Model name for title
        """
        if len(y_pred_proba.shape) > 1:
            y_pred_proba = y_pred_proba[:, 1]
        
        fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.3f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'ROC Curve - {model_name}')
        plt.legend(loc="lower right")
        
        output_path = config.OUTPUT_DIR / f"roc_curve_{model_name}.png"
        plt.savefig(output_path, dpi=config.DPI, bbox_inches='tight')
        self.logger.info(f"ROC curve saved to {output_path}")
        plt.close()
    
    def plot_precision_recall_curve(self, y_true: np.ndarray, y_pred_proba: np.ndarray,
                                   model_name: str = "Model") -> None:
        """
        Plot Precision-Recall curve.
        
        Args:
            y_true: True labels
            y_pred_proba: Prediction probabilities
            model_name: Model name for title
        """
        if len(y_pred_proba.shape) > 1:
            y_pred_proba = y_pred_proba[:, 1]
        
        precision_vals, recall_vals, _ = precision_recall_curve(y_true, y_pred_proba)
        pr_auc = auc(recall_vals, precision_vals)
        
        plt.figure(figsize=(8, 6))
        plt.plot(recall_vals, precision_vals, color='darkblue', lw=2, 
                label=f'PR curve (AUC = {pr_auc:.3f})')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title(f'Precision-Recall Curve - {model_name}')
        plt.legend(loc="best")
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        
        output_path = config.OUTPUT_DIR / f"pr_curve_{model_name}.png"
        plt.savefig(output_path, dpi=config.DPI, bbox_inches='tight')
        self.logger.info(f"PR curve saved to {output_path}")
        plt.close()
    
    def plot_model_comparison(self, metric: str = "f1", top_n: int = None) -> None:
        """
        Plot model comparison bar chart.
        
        Args:
            metric: Metric to plot
            top_n: Number of top models to display
        """
        comparison_df = self.compare_models(metric)
        
        if top_n is not None:
            comparison_df = comparison_df.head(top_n)
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(comparison_df['Model'], comparison_df[metric], color='steelblue')
        plt.xlabel('Model')
        plt.ylabel(metric.capitalize())
        plt.title(f'Model Comparison - {metric.upper()}')
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.3f}', ha='center', va='bottom')
        
        plt.tight_layout()
        output_path = config.OUTPUT_DIR / f"model_comparison_{metric}.png"
        plt.savefig(output_path, dpi=config.DPI, bbox_inches='tight')
        self.logger.info(f"Model comparison plot saved to {output_path}")
        plt.close()
    
    def generate_report(self, y_true: np.ndarray, y_pred: np.ndarray) -> str:
        """
        Generate detailed classification report.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            
        Returns:
            Classification report string
        """
        report = classification_report(y_true, y_pred, 
                                      target_names=['Legitimate', 'Fraudulent'])
        return report
    
    def calculate_optimal_threshold(self, y_true: np.ndarray, y_pred_proba: np.ndarray,
                                   metric: str = "f1") -> Tuple[float, float]:
        """
        Calculate optimal classification threshold.
        
        Args:
            y_true: True labels
            y_pred_proba: Prediction probabilities
            metric: Metric to optimize
            
        Returns:
            Tuple of (optimal_threshold, metric_value)
        """
        if len(y_pred_proba.shape) > 1:
            y_pred_proba = y_pred_proba[:, 1]
        
        optimal_threshold, best_value = optimize_threshold(y_true, y_pred_proba, metric)
        
        self.logger.info(f"Optimal threshold for {metric}: {optimal_threshold:.4f}")
        self.logger.info(f"Metric value at optimal threshold: {best_value:.4f}")
        
        return optimal_threshold, best_value


# Type hint import
from typing import Tuple


if __name__ == "__main__":
    logger = setup_logging(__name__)
    logger.info("Evaluation module loaded successfully")
