"""
Interactive Streamlit App for Fraud Detection System
Provides real-time dashboards, model comparison, and Power BI integration
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from sklearn.metrics import confusion_matrix, roc_curve, auc

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

import config
from src.utils import setup_logging
from src.preprocessing import DataPreprocessor
from src.models import ModelTrainer
from src.evaluation import ModelEvaluator
from src.dashboard import InteractiveDashboard
from src.power_bi_export import PowerBIExporter


# Configure Streamlit
st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        /* Main background and text */
        .main {
            background-color: #f8f9fa;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #2c3e50;
        }
        
        /* Metric styling */
        [data-testid="metric-container"] {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #2c3e50;
            font-weight: 700;
        }
        
        /* Cards */
        .card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        /* Buttons */
        .stButton>button {
            border-radius: 5px;
            background-color: #3498db;
            color: white;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #2980b9;
            box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
        }
        
        /* Tabs */
        [data-testid="stTabs"] [role="tablist"] {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_data():
    """Load and preprocess data."""
    preprocessor = DataPreprocessor()
    if not config.DATASET_PATH.exists():
        return None, None, None, None
    
    X_train, X_test, y_train, y_test = preprocessor.prepare_data(config.DATASET_PATH)
    return X_train, X_test, y_train, y_test


@st.cache_resource
def train_models(X_train, y_train):
    """Train all models."""
    trainer = ModelTrainer()
    models = trainer.train_all_models(X_train, y_train)
    return models


def main():
    """Main Streamlit app."""
    
    # Header
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px;">
            <h1 style="color: white; margin: 0;">🔍 Fraud Detection System</h1>
            <p style="color: rgba(255,255,255,0.9); margin-top: 10px;">
                Advanced Machine Learning for Financial Transaction Monitoring
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📊 Navigation")
        page = st.radio(
            "Select a page:",
            ["🏠 Overview", "📈 Data Analysis", "🤖 Model Training", 
             "📊 Model Comparison", "💼 Power BI Export", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### 📁 Project Info")
        st.info(
            f"**Dataset**: Credit Card Fraud\n"
            f"**Total Transactions**: 284,807\n"
            f"**Fraudulent Cases**: 492 (0.17%)\n"
            f"**Features**: 30\n"
            f"**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
    
    # Load data
    with st.spinner("Loading data..."):
        X_train, X_test, y_train, y_test = load_data()
    
    if X_train is None:
        st.error("❌ Dataset not found. Please download it from Kaggle.")
        st.info("Download the dataset from: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud")
        return
    
    # Page routing
    if page == "🏠 Overview":
        page_overview(X_train, X_test, y_train, y_test)
    elif page == "📈 Data Analysis":
        page_data_analysis(X_train, X_test, y_train, y_test)
    elif page == "🤖 Model Training":
        page_model_training(X_train, X_test, y_train, y_test)
    elif page == "📊 Model Comparison":
        page_model_comparison(X_train, X_test, y_train, y_test)
    elif page == "💼 Power BI Export":
        page_powerbi_export(X_train, X_test, y_train, y_test)
    elif page == "⚙️ Settings":
        page_settings()


def page_overview(X_train, X_test, y_train, y_test):
    """Overview page with key metrics."""
    st.markdown("## 📊 System Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📦 Total Transactions",
            f"{len(X_train) + len(X_test):,}",
            delta="Training Set"
        )
    
    with col2:
        fraud_rate = (y_test.sum() / len(y_test) * 100)
        st.metric(
            "⚠️ Fraud Rate",
            f"{fraud_rate:.2f}%",
            delta="In Test Set"
        )
    
    with col3:
        st.metric(
            "✅ Legitimate",
            f"{(y_test == 0).sum():,}",
            delta="Test Set"
        )
    
    with col4:
        st.metric(
            "❌ Fraudulent",
            f"{(y_test == 1).sum():,}",
            delta="Test Set"
        )
    
    st.markdown("---")
    
    # Dataset overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Dataset Split")
        split_data = {
            'Set': ['Training', 'Testing'],
            'Samples': [len(X_train), len(X_test)],
            'Percentage': [f"{len(X_train)/(len(X_train)+len(X_test))*100:.1f}%", 
                          f"{len(X_test)/(len(X_train)+len(X_test))*100:.1f}%"]
        }
        st.dataframe(pd.DataFrame(split_data), use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Class Distribution")
        dashboard = InteractiveDashboard()
        fig = dashboard.create_class_distribution_chart(y_test)
        st.plotly_chart(fig, use_container_width=True)
    
    # Feature overview
    st.markdown("### 📊 Feature Overview")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Total Features**: {X_test.shape[1]}")
        st.markdown(f"**Feature Names**: V1 - V28 (PCA Transformed)")
        st.markdown(f"**Additional Features**: Time, Amount")
    
    with col2:
        st.markdown("**Feature Statistics**")
        stats_df = pd.DataFrame({
            'Statistic': ['Mean', 'Std Dev', 'Min', 'Max'],
            'Value': [
                f"{X_test.mean().mean():.4f}",
                f"{X_test.std().mean():.4f}",
                f"{X_test.min().min():.4f}",
                f"{X_test.max().max():.4f}"
            ]
        })
        st.dataframe(stats_df, use_container_width=True)


def page_data_analysis(X_train, X_test, y_train, y_test):
    """Data analysis page."""
    st.markdown("## 📈 Data Analysis & Exploration")
    
    tabs = st.tabs(["📊 Distributions", "🔗 Correlations", "📈 Feature Analysis", "🔍 Fraud Patterns"])
    
    dashboard = InteractiveDashboard()
    
    with tabs[0]:
        st.markdown("### Class Distribution")
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = dashboard.create_class_distribution_chart(y_test)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.markdown("**Statistics**")
            st.metric("Legitimate Transactions", (y_test == 0).sum(), delta="Class 0")
            st.metric("Fraudulent Transactions", (y_test == 1).sum(), delta="Class 1")
            st.metric("Fraud Percentage", f"{(y_test == 1).sum() / len(y_test) * 100:.3f}%")
    
    with tabs[1]:
        st.markdown("### Feature Correlation with Fraud")
        top_n = st.slider("Show top N features:", 5, 30, 15)
        fig = dashboard.create_feature_correlation_chart(X_test, y_test, top_n=top_n)
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[2]:
        st.markdown("### Feature Analysis")
        selected_feature = st.selectbox(
            "Select a feature to analyze:",
            [f"V{i}" for i in range(1, 29)] + ['Time', 'Amount']
        )
        
        if selected_feature in X_test.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribution for legitimate
                legit_values = X_test[X_test.index.isin(X_test.index[y_test == 0])][selected_feature]
                fig1 = px.histogram(legit_values, nbins=50, title=f"{selected_feature} - Legitimate")
                fig1.update_layout(template='plotly_dark', height=400)
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Distribution for fraud
                fraud_values = X_test[X_test.index.isin(X_test.index[y_test == 1])][selected_feature]
                fig2 = px.histogram(fraud_values, nbins=50, title=f"{selected_feature} - Fraudulent")
                fig2.update_layout(template='plotly_dark', height=400)
                st.plotly_chart(fig2, use_container_width=True)
    
    with tabs[3]:
        st.markdown("### Fraud Patterns")
        if 'Amount' in X_test.columns and 'Time' in X_test.columns:
            fig = dashboard.create_amount_distribution_chart(X_test, y_test)
            if fig:
                st.plotly_chart(fig, use_container_width=True)


def page_model_training(X_train, X_test, y_train, y_test):
    """Model training page."""
    st.markdown("## 🤖 Model Training")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### Available Models")
        models_info = {
            "Logistic Regression": "Linear classifier with L2 regularization",
            "Decision Tree": "Tree-based classifier with max depth 10",
            "Random Forest": "Ensemble of 100 decision trees",
            "Gradient Boosting": "Sequential ensemble learning",
            "Neural Network": "Multi-layer perceptron classifier"
        }
        
        for model_name, description in models_info.items():
            st.markdown(f"**{model_name}**: {description}")
    
    with col2:
        if st.button("🚀 Train All Models", key="train_all"):
            with st.spinner("Training models..."):
                trainer = ModelTrainer()
                models = trainer.train_all_models(X_train, y_train)
                
                # Evaluate models
                evaluator = ModelEvaluator()
                results = evaluator.evaluate_all_models(models, X_test, y_test)
                
                st.success("✅ All models trained successfully!")
                
                # Show results
                results_df = pd.DataFrame(results).T
                st.dataframe(results_df, use_container_width=True)


def page_model_comparison(X_train, X_test, y_train, y_test):
    """Model comparison page."""
    st.markdown("## 📊 Model Comparison")
    
    # Train and evaluate models
    with st.spinner("Loading models..."):
        trainer = ModelTrainer()
        models = trainer.train_all_models(X_train, y_train)
        evaluator = ModelEvaluator()
        results = evaluator.evaluate_all_models(models, X_test, y_test)
    
    dashboard = InteractiveDashboard()
    
    tabs = st.tabs(["📊 Metrics", "🎯 ROC Curves", "❌ Confusion Matrices", "📈 Detailed Analysis"])
    
    with tabs[0]:
        st.markdown("### Model Performance Metrics")
        col1, col2 = st.columns(2)
        
        with col1:
            metric = st.selectbox("Select metric:", ["f1", "accuracy", "precision", "recall", "roc_auc"])
            fig = dashboard.create_model_comparison_chart(results, metric=metric)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Results Table")
            results_df = pd.DataFrame(results).T.round(4)
            st.dataframe(results_df, use_container_width=True)
    
    with tabs[1]:
        st.markdown("### ROC Curves")
        cols = st.columns(2)
        
        for idx, (model_name, model) in enumerate(models.items()):
            if model_name not in results:
                continue
            
            try:
                y_pred_proba = None
                if hasattr(model, 'predict_proba'):
                    y_pred_proba = model.predict_proba(X_test)[:, 1]
                elif hasattr(model, 'decision_function'):
                    y_pred_proba = model.decision_function(X_test)
                
                if y_pred_proba is not None:
                    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
                    roc_auc = auc(fpr, tpr)
                    
                    fig = dashboard.create_roc_curve_chart(fpr, tpr, roc_auc, model_name)
                    with cols[idx % 2]:
                        st.plotly_chart(fig, use_container_width=True)
            except:
                pass
    
    with tabs[2]:
        st.markdown("### Confusion Matrices")
        cols = st.columns(2)
        
        for idx, (model_name, model) in enumerate(models.items()):
            y_pred = model.predict(X_test)
            cm = confusion_matrix(y_test, y_pred)
            
            fig = dashboard.create_confusion_matrix_heatmap(cm, model_name)
            with cols[idx % 2]:
                st.plotly_chart(fig, use_container_width=True)
    
    with tabs[3]:
        st.markdown("### Detailed Analysis")
        st.markdown("**Best Model**: " + max(results.items(), key=lambda x: x[1].get('f1', 0))[0])
        
        analysis_data = []
        for model_name, metrics in results.items():
            analysis_data.append({
                'Model': model_name,
                'Accuracy': f"{metrics.get('accuracy', 0):.4f}",
                'Precision': f"{metrics.get('precision', 0):.4f}",
                'Recall': f"{metrics.get('recall', 0):.4f}",
                'F1-Score': f"{metrics.get('f1', 0):.4f}",
                'ROC-AUC': f"{metrics.get('roc_auc', 0):.4f}"
            })
        
        st.dataframe(pd.DataFrame(analysis_data), use_container_width=True)


def page_powerbi_export(X_train, X_test, y_train, y_test):
    """Power BI export page."""
    st.markdown("## 💼 Power BI Integration")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Export Data for Power BI
        
        This feature exports your fraud detection data and model results in formats 
        compatible with Microsoft Power BI for advanced business intelligence and 
        real-time monitoring.
        
        **What Gets Exported:**
        - ✅ Model metrics and performance statistics
        - ✅ Predictions and fraud probabilities
        - ✅ Feature statistics and importance
        - ✅ Confusion matrices
        - ✅ Sample predictions for analysis
        """)
    
    with col2:
        if st.button("📤 Export to Power BI", key="export_powerbi"):
            with st.spinner("Exporting data..."):
                trainer = ModelTrainer()
                models = trainer.train_all_models(X_train, y_train)
                evaluator = ModelEvaluator()
                results = evaluator.evaluate_all_models(models, X_test, y_test)
                
                # Get best model predictions
                best_model = max(models.items(), key=lambda x: results[x[0]].get('f1', 0))[1]
                y_pred = best_model.predict(X_test)
                
                if hasattr(best_model, 'predict_proba'):
                    y_pred_proba = best_model.predict_proba(X_test)[:, 1]
                else:
                    y_pred_proba = best_model.decision_function(X_test)
                
                exporter = PowerBIExporter()
                feature_names = [f"V{i}" for i in range(1, 29)] + ['Time', 'Amount']
                exported = exporter.export_all(
                    results=results,
                    y_true=y_test,
                    y_pred=y_pred,
                    y_pred_proba=y_pred_proba,
                    X=X_test,
                    feature_names=feature_names,
                    cm=confusion_matrix(y_test, y_pred),
                    model_name="Best Model"
                )
                
                st.success("✅ Data exported successfully!")
                st.markdown("### Exported Files")
                for export_type, path in exported.items():
                    st.markdown(f"- **{export_type}**: `{path}`")


def page_settings():
    """Settings page."""
    st.markdown("## ⚙️ Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Configuration")
        st.markdown(f"**Dataset Path**: {config.DATASET_PATH}")
        st.markdown(f"**Output Directory**: {config.OUTPUT_DIR}")
        st.markdown(f"**Log Level**: {config.LOG_LEVEL}")
    
    with col2:
        st.markdown("### About")
        st.markdown("""
        **Fraud Detection System v1.0**
        
        An advanced machine learning system for detecting fraudulent financial transactions.
        
        **Features**:
        - Multiple ML algorithms
        - Interactive dashboards
        - Power BI integration
        - Real-time monitoring
        
        **Dataset**: Credit Card Fraud Detection (Kaggle)
        """)


if __name__ == "__main__":
    main()
