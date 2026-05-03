"""
Interactive Dashboard Module for Fraud Detection System
Uses Plotly for interactive visualizations
"""

import logging
from pathlib import Path
from typing import Dict, Any, List

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

import config
from src.utils import setup_logging


class InteractiveDashboard:
    """Create interactive Plotly dashboards for fraud detection."""
    
    def __init__(self):
        """Initialize dashboard creator."""
        self.logger = setup_logging(__name__)
        self.plots = {}
    
    def create_class_distribution_chart(self, y: np.ndarray) -> go.Figure:
        """
        Create interactive class distribution chart.
        
        Args:
            y: Target labels
            
        Returns:
            Plotly figure
        """
        self.logger.info("Creating class distribution chart...")
        
        fraud_count = (y == 1).sum()
        legit_count = (y == 0).sum()
        
        fig = go.Figure(data=[
            go.Bar(x=['Legitimate', 'Fraudulent'], 
                  y=[legit_count, fraud_count],
                  marker=dict(color=['#2ecc71', '#e74c3c']),
                  text=[f"{legit_count:,}", f"{fraud_count:,}"],
                  textposition='auto')
        ])
        
        fig.update_layout(
            title='Transaction Distribution by Class',
            xaxis_title='Class',
            yaxis_title='Count',
            hovermode='x unified',
            template='plotly_dark',
            height=500
        )
        
        return fig
    
    def create_feature_correlation_chart(self, X: pd.DataFrame, y: np.ndarray, 
                                        top_n: int = 15) -> go.Figure:
        """
        Create feature correlation with target chart.
        
        Args:
            X: Features dataframe
            y: Target array
            top_n: Number of top features
            
        Returns:
            Plotly figure
        """
        self.logger.info("Creating feature correlation chart...")
        
        # Calculate correlations
        X_temp = X.copy()
        X_temp['Class'] = y
        correlations = X_temp.corr()['Class'].drop('Class').abs().sort_values(ascending=True).tail(top_n)
        
        fig = go.Figure(data=[
            go.Bar(
                y=correlations.index,
                x=correlations.values,
                orientation='h',
                marker=dict(color=correlations.values, colorscale='Viridis'),
                hovertemplate='%{y}: %{x:.4f}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=f'Top {top_n} Features by Correlation with Fraud',
            xaxis_title='Absolute Correlation',
            yaxis_title='Feature',
            template='plotly_dark',
            height=600,
            hovermode='closest'
        )
        
        return fig
    
    def create_roc_curve_chart(self, fpr: np.ndarray, tpr: np.ndarray, 
                              roc_auc: float, model_name: str = "Model") -> go.Figure:
        """
        Create interactive ROC curve chart.
        
        Args:
            fpr: False positive rates
            tpr: True positive rates
            roc_auc: ROC-AUC score
            model_name: Model name
            
        Returns:
            Plotly figure
        """
        self.logger.info("Creating ROC curve chart...")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=fpr, y=tpr,
            mode='lines',
            name=f'{model_name} (AUC = {roc_auc:.3f})',
            line=dict(color='#3498db', width=3),
            hovertemplate='FPR: %{x:.3f}<br>TPR: %{y:.3f}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=[0, 1], y=[0, 1],
            mode='lines',
            name='Random Classifier',
            line=dict(color='#95a5a6', width=2, dash='dash'),
            hovertemplate='Random Classifier<extra></extra>'
        ))
        
        fig.update_layout(
            title=f'ROC Curve - {model_name}',
            xaxis_title='False Positive Rate',
            yaxis_title='True Positive Rate',
            template='plotly_dark',
            height=600,
            hovermode='closest',
            xaxis=dict(range=[0, 1]),
            yaxis=dict(range=[0, 1])
        )
        
        return fig
    
    def create_confusion_matrix_heatmap(self, cm: np.ndarray, 
                                       model_name: str = "Model") -> go.Figure:
        """
        Create interactive confusion matrix heatmap.
        
        Args:
            cm: Confusion matrix
            model_name: Model name
            
        Returns:
            Plotly figure
        """
        self.logger.info("Creating confusion matrix heatmap...")
        
        fig = go.Figure(data=go.Heatmap(
            z=cm,
            x=['Predicted Legitimate', 'Predicted Fraudulent'],
            y=['Actual Legitimate', 'Actual Fraudulent'],
            text=cm,
            texttemplate='%{text}',
            colorscale='Blues',
            hovertemplate='%{y}<br>%{x}<br>Count: %{text}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f'Confusion Matrix - {model_name}',
            template='plotly_dark',
            height=500
        )
        
        return fig
    
    def create_model_comparison_chart(self, results: Dict[str, Dict[str, float]], 
                                     metric: str = 'f1') -> go.Figure:
        """
        Create model comparison chart.
        
        Args:
            results: Model evaluation results
            metric: Metric to compare
            
        Returns:
            Plotly figure
        """
        self.logger.info("Creating model comparison chart...")
        
        models = []
        metrics = []
        colors = []
        color_map = {
            'accuracy': '#3498db',
            'precision': '#2ecc71',
            'recall': '#f39c12',
            'f1': '#e74c3c',
            'roc_auc': '#9b59b6'
        }
        
        for model_name, model_metrics in results.items():
            if metric in model_metrics:
                models.append(model_name)
                metrics.append(model_metrics[metric])
                colors.append(color_map.get(metric, '#3498db'))
        
        fig = go.Figure(data=[
            go.Bar(
                x=models,
                y=metrics,
                marker=dict(color=colors),
                text=[f'{m:.3f}' for m in metrics],
                textposition='auto',
                hovertemplate='%{x}<br>' + metric + ': %{y:.4f}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=f'Model Comparison - {metric.upper()}',
            xaxis_title='Model',
            yaxis_title=metric.capitalize(),
            template='plotly_dark',
            height=500,
            hovermode='x unified',
            xaxis_tickangle=-45
        )
        
        return fig
    
    def create_metrics_gauge_chart(self, metrics: Dict[str, float]) -> go.Figure:
        """
        Create gauge charts for key metrics.
        
        Args:
            metrics: Dictionary of metrics
            
        Returns:
            Plotly figure
        """
        self.logger.info("Creating metrics gauge chart...")
        
        key_metrics = ['accuracy', 'precision', 'recall', 'f1']
        available_metrics = {k: v for k, v in metrics.items() if k in key_metrics and v is not None}
        
        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{'type': 'indicator'}, {'type': 'indicator'}],
                   [{'type': 'indicator'}, {'type': 'indicator'}]]
        )
        
        positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
        colors_list = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']
        
        for i, (metric_name, metric_value) in enumerate(available_metrics.items()):
            if i < 4:
                fig.add_trace(
                    go.Indicator(
                        mode='gauge+number+delta',
                        value=metric_value * 100,
                        title={'text': metric_name.capitalize()},
                        domain={'x': [0, 1], 'y': [0, 1]},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': colors_list[i]},
                            'steps': [
                                {'range': [0, 50], 'color': '#ecf0f1'},
                                {'range': [50, 100], 'color': '#d5dbdb'}
                            ],
                            'threshold': {
                                'line': {'color': 'red', 'width': 4},
                                'thickness': 0.75,
                                'value': 80
                            }
                        }
                    ),
                    row=positions[i][0], col=positions[i][1]
                )
        
        fig.update_layout(
            title_text='Model Performance Metrics',
            template='plotly_dark',
            height=600
        )
        
        return fig
    
    def create_amount_distribution_chart(self, X: pd.DataFrame, y: np.ndarray) -> go.Figure:
        """
        Create interactive amount distribution chart.
        
        Args:
            X: Features dataframe
            y: Target labels
            
        Returns:
            Plotly figure
        """
        self.logger.info("Creating amount distribution chart...")
        
        if 'Amount' not in X.columns:
            self.logger.warning("Amount column not found")
            return None
        
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=X[y == 0]['Amount'],
            name='Legitimate',
            opacity=0.7,
            marker_color='#2ecc71',
            nbinsx=50,
            hovertemplate='Amount: %{x:.2f}<br>Count: %{y}<extra></extra>'
        ))
        
        fig.add_trace(go.Histogram(
            x=X[y == 1]['Amount'],
            name='Fraudulent',
            opacity=0.7,
            marker_color='#e74c3c',
            nbinsx=50,
            hovertemplate='Amount: %{x:.2f}<br>Count: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Transaction Amount Distribution',
            xaxis_title='Amount ($)',
            yaxis_title='Frequency',
            barmode='overlay',
            template='plotly_dark',
            height=500,
            hovermode='x unified'
        )
        
        return fig
    
    def create_time_distribution_chart(self, X: pd.DataFrame, y: np.ndarray) -> go.Figure:
        """
        Create interactive time distribution chart.
        
        Args:
            X: Features dataframe
            y: Target labels
            
        Returns:
            Plotly figure
        """
        self.logger.info("Creating time distribution chart...")
        
        if 'Time' not in X.columns:
            self.logger.warning("Time column not found")
            return None
        
        # Convert to hours
        X_copy = X.copy()
        X_copy['Hour'] = (X_copy['Time'] / 3600) % 24
        
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=X_copy[y == 0]['Hour'],
            name='Legitimate',
            opacity=0.7,
            marker_color='#2ecc71',
            nbinsx=24,
            hovertemplate='Hour: %{x:.1f}<br>Count: %{y}<extra></extra>'
        ))
        
        fig.add_trace(go.Histogram(
            x=X_copy[y == 1]['Hour'],
            name='Fraudulent',
            opacity=0.7,
            marker_color='#e74c3c',
            nbinsx=24,
            hovertemplate='Hour: %{x:.1f}<br>Count: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Transaction Time Distribution by Hour',
            xaxis_title='Hour of Day',
            yaxis_title='Frequency',
            barmode='overlay',
            template='plotly_dark',
            height=500,
            hovermode='x unified'
        )
        
        return fig
    
    def create_dashboard_html(self, output_path: Path = None) -> str:
        """
        Create combined HTML dashboard.
        
        Args:
            output_path: Path to save HTML
            
        Returns:
            HTML string
        """
        if output_path is None:
            output_path = config.OUTPUT_DIR / "dashboard.html"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create basic HTML structure
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Fraud Detection Dashboard</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    color: #fff;
                    padding: 20px;
                }
                
                .container {
                    max-width: 1400px;
                    margin: 0 auto;
                }
                
                header {
                    text-align: center;
                    margin-bottom: 40px;
                    padding: 20px;
                    background: rgba(0, 0, 0, 0.3);
                    border-radius: 10px;
                    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                }
                
                h1 {
                    font-size: 2.5em;
                    margin-bottom: 10px;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
                }
                
                .subtitle {
                    font-size: 1.1em;
                    opacity: 0.9;
                }
                
                .dashboard-grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                    margin-top: 30px;
                }
                
                .dashboard-grid.full {
                    grid-template-columns: 1fr;
                }
                
                .card {
                    background: rgba(0, 0, 0, 0.2);
                    border-radius: 10px;
                    padding: 20px;
                    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(4px);
                }
                
                .card h2 {
                    font-size: 1.3em;
                    margin-bottom: 15px;
                    color: #3498db;
                }
                
                .plot {
                    width: 100%;
                    height: 500px;
                }
                
                .metrics-row {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin-top: 20px;
                }
                
                .metric {
                    background: rgba(0, 0, 0, 0.3);
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                    border-left: 4px solid #3498db;
                }
                
                .metric-value {
                    font-size: 2em;
                    font-weight: bold;
                    color: #2ecc71;
                }
                
                .metric-label {
                    font-size: 0.9em;
                    opacity: 0.8;
                    margin-top: 5px;
                }
                
                footer {
                    text-align: center;
                    margin-top: 40px;
                    padding: 20px;
                    border-top: 1px solid rgba(255, 255, 255, 0.1);
                    opacity: 0.7;
                }
                
                @media (max-width: 1024px) {
                    .dashboard-grid {
                        grid-template-columns: 1fr;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>🔍 Fraud Detection Dashboard</h1>
                    <p class="subtitle">Real-time Fraud Analytics & Model Performance Monitoring</p>
                </header>
                
                <div class="dashboard-grid">
                    <div class="card">
                        <h2>📊 Key Metrics</h2>
                        <div class="metrics-row" id="metrics"></div>
                    </div>
                </div>
                
                <div class="dashboard-grid">
                    <div class="card">
                        <h2>Class Distribution</h2>
                        <div class="plot" id="distribution"></div>
                    </div>
                    <div class="card">
                        <h2>Feature Importance</h2>
                        <div class="plot" id="features"></div>
                    </div>
                </div>
                
                <div class="dashboard-grid full">
                    <div class="card">
                        <h2>Model Performance Comparison</h2>
                        <div class="plot" id="models"></div>
                    </div>
                </div>
                
                <div class="dashboard-grid">
                    <div class="card">
                        <h2>ROC Curve Analysis</h2>
                        <div class="plot" id="roc"></div>
                    </div>
                    <div class="card">
                        <h2>Confusion Matrix</h2>
                        <div class="plot" id="confusion"></div>
                    </div>
                </div>
                
                <footer>
                    <p>Fraud Detection System v1.0.0 | Last Updated: April 2026</p>
                    <p>Data-driven insights for financial security</p>
                </footer>
            </div>
        </body>
        </html>
        """
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        self.logger.info(f"Dashboard HTML created at {output_path}")
        return str(output_path)
    
    def save_interactive_html(self, fig: go.Figure, filename: str) -> Path:
        """
        Save interactive Plotly figure to HTML.
        
        Args:
            fig: Plotly figure
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        output_path = config.OUTPUT_DIR / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        fig.write_html(output_path)
        self.logger.info(f"Saved interactive plot to {output_path}")
        
        return output_path


if __name__ == "__main__":
    logger = setup_logging(__name__)
    logger.info("Dashboard module loaded successfully")
