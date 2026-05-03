"""
Streamlit Fraud Detection Dashboard - Demo Version
Simplified version that works with minimal dependencies
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

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
        .main {
            background-color: #f8f9fa;
        }
        
        [data-testid="stSidebar"] {
            background-color: #2c3e50;
        }
        
        h1, h2, h3 {
            color: #2c3e50;
            font-weight: 700;
        }
        
        .stButton>button {
            border-radius: 5px;
            background-color: #3498db;
            color: white;
            font-weight: 600;
            transition: all 0.3s ease;
        }
    </style>
""", unsafe_allow_html=True)

# Generate sample data for demo
@st.cache_data
def generate_demo_data():
    """Generate demo fraud detection data."""
    np.random.seed(42)
    n_legit = 10000
    n_fraud = 200
    total = n_legit + n_fraud
    
    # Create sample data
    legit_amounts = np.random.normal(100, 30, n_legit)
    fraud_amounts = np.random.normal(250, 100, n_fraud)
    all_amounts = np.concatenate([legit_amounts, fraud_amounts])
    
    data = {
        'Transaction': range(total),
        'Amount': all_amounts,
        'Class': np.concatenate([np.zeros(n_legit), np.ones(n_fraud)]),
        'Time': np.random.randint(0, 86400, total)
    }
    
    return pd.DataFrame(data)

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
            ["🏠 Overview", "📈 Data Analysis", "📊 Model Comparison", "💼 Power BI Export"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### 📁 Project Info")
        st.info(
            f"**Dataset**: Credit Card Fraud (Demo)\n"
            f"**Sample Transactions**: 10,200\n"
            f"**Fraudulent Cases**: 200\n"
            f"**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
    
    # Load demo data
    df = generate_demo_data()
    
    # Page routing
    if page == "🏠 Overview":
        page_overview(df)
    elif page == "📈 Data Analysis":
        page_data_analysis(df)
    elif page == "📊 Model Comparison":
        page_model_comparison()
    elif page == "💼 Power BI Export":
        page_powerbi_export()

def page_overview(df):
    """Overview page with key metrics."""
    st.markdown("## 📊 System Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    legit_count = (df['Class'] == 0).sum()
    fraud_count = (df['Class'] == 1).sum()
    fraud_rate = (fraud_count / len(df) * 100)
    
    with col1:
        st.metric("📦 Total Transactions", f"{len(df):,}")
    
    with col2:
        st.metric("⚠️ Fraud Rate", f"{fraud_rate:.2f}%")
    
    with col3:
        st.metric("✅ Legitimate", f"{legit_count:,}")
    
    with col4:
        st.metric("❌ Fraudulent", f"{fraud_count:,}")
    
    st.markdown("---")
    
    # Class distribution chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Dataset Split")
        split_data = {
            'Class': ['Legitimate', 'Fraudulent'],
            'Count': [legit_count, fraud_count],
            'Percentage': [f"{legit_count/len(df)*100:.1f}%", f"{fraud_count/len(df)*100:.1f}%"]
        }
        st.dataframe(pd.DataFrame(split_data), use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Class Distribution")
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
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

def page_data_analysis(df):
    """Data analysis page."""
    st.markdown("## 📈 Data Analysis & Exploration")
    
    tabs = st.tabs(["📊 Distributions", "📈 Amount Analysis", "🔍 Summary Statistics"])
    
    with tabs[0]:
        st.markdown("### Transaction Amount Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            legit_amounts = df[df['Class'] == 0]['Amount']
            fig1 = px.histogram(legit_amounts, nbins=50, title="Legitimate Transactions", 
                               labels={'value': 'Amount ($)', 'count': 'Frequency'})
            fig1.update_layout(template='plotly_dark', height=400)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fraud_amounts = df[df['Class'] == 1]['Amount']
            fig2 = px.histogram(fraud_amounts, nbins=50, title="Fraudulent Transactions",
                               labels={'value': 'Amount ($)', 'count': 'Frequency'})
            fig2.update_layout(template='plotly_dark', height=400)
            st.plotly_chart(fig2, use_container_width=True)
    
    with tabs[1]:
        st.markdown("### Amount Analysis by Class")
        
        amount_stats = pd.DataFrame({
            'Metric': ['Mean', 'Median', 'Std Dev', 'Min', 'Max'],
            'Legitimate': [
                f"${df[df['Class']==0]['Amount'].mean():.2f}",
                f"${df[df['Class']==0]['Amount'].median():.2f}",
                f"${df[df['Class']==0]['Amount'].std():.2f}",
                f"${df[df['Class']==0]['Amount'].min():.2f}",
                f"${df[df['Class']==0]['Amount'].max():.2f}",
            ],
            'Fraudulent': [
                f"${df[df['Class']==1]['Amount'].mean():.2f}",
                f"${df[df['Class']==1]['Amount'].median():.2f}",
                f"${df[df['Class']==1]['Amount'].std():.2f}",
                f"${df[df['Class']==1]['Amount'].min():.2f}",
                f"${df[df['Class']==1]['Amount'].max():.2f}",
            ]
        })
        st.dataframe(amount_stats, use_container_width=True)
    
    with tabs[2]:
        st.markdown("### Summary Statistics")
        st.dataframe(df.describe(), use_container_width=True)

def page_model_comparison():
    """Model comparison page."""
    st.markdown("## 📊 Model Performance Comparison")
    
    # Sample model metrics
    metrics = {
        'Model': ['Logistic Regression', 'Decision Tree', 'Random Forest', 'Gradient Boosting', 'Neural Network'],
        'Accuracy': [0.9832, 0.9715, 0.9876, 0.9901, 0.9845],
        'Precision': [0.9150, 0.8920, 0.9345, 0.9520, 0.9280],
        'Recall': [0.8730, 0.8450, 0.8920, 0.9120, 0.8850],
        'F1-Score': [0.8932, 0.8680, 0.9128, 0.9318, 0.9062],
        'ROC-AUC': [0.9654, 0.9421, 0.9756, 0.9834, 0.9705]
    }
    
    df_metrics = pd.DataFrame(metrics)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("### Model Performance Metrics")
        st.dataframe(df_metrics, use_container_width=True)
    
    with col2:
        st.markdown("### Best Performers")
        st.markdown(f"""
        ⭐ **F1-Score**: {df_metrics.loc[df_metrics['F1-Score'].idxmax(), 'Model']}
        
        ⭐ **ROC-AUC**: {df_metrics.loc[df_metrics['ROC-AUC'].idxmax(), 'Model']}
        
        ⭐ **Accuracy**: {df_metrics.loc[df_metrics['Accuracy'].idxmax(), 'Model']}
        """)
    
    st.markdown("---")
    
    # F1 Score Comparison
    col1, col2 = st.columns(2)
    
    with col1:
        fig_f1 = go.Figure(data=[
            go.Bar(x=df_metrics['Model'], y=df_metrics['F1-Score'],
                  marker=dict(color='#3498db'),
                  text=[f'{x:.4f}' for x in df_metrics['F1-Score']],
                  textposition='auto')
        ])
        fig_f1.update_layout(title='F1-Score Comparison', template='plotly_dark', height=400)
        st.plotly_chart(fig_f1, use_container_width=True)
    
    with col2:
        fig_roc = go.Figure(data=[
            go.Bar(x=df_metrics['Model'], y=df_metrics['ROC-AUC'],
                  marker=dict(color='#2ecc71'),
                  text=[f'{x:.4f}' for x in df_metrics['ROC-AUC']],
                  textposition='auto')
        ])
        fig_roc.update_layout(title='ROC-AUC Comparison', template='plotly_dark', height=400)
        st.plotly_chart(fig_roc, use_container_width=True)

def page_powerbi_export():
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
            st.success("✅ Demo export - In production this would generate Excel files!")
            st.info("""
            **Files that would be generated:**
            - model_metrics.xlsx
            - predictions.xlsx
            - feature_statistics.xlsx
            - confusion_matrix_best_model.xlsx
            """)

if __name__ == "__main__":
    main()
