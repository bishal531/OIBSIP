"""
Flask Web Application for Fraud Detection System
Modern interactive web interface with Power BI integration
"""

from pathlib import Path
from datetime import datetime
import json
import sys

from flask import Flask, render_template_string, jsonify, request
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

import config
from src.utils import setup_logging
from src.preprocessing import DataPreprocessor
from src.models import ModelTrainer
from src.evaluation import ModelEvaluator
from src.dashboard import InteractiveDashboard
from src.power_bi_export import PowerBIExporter


app = Flask(__name__)
logger = setup_logging(__name__)

# Cache for loaded data and models
_cache = {
    'data': None,
    'models': None,
    'results': None
}


def load_data_and_models():
    """Load data and train models if not already cached."""
    if _cache['data'] is None:
        logger.info("Loading data...")
        preprocessor = DataPreprocessor()
        if not config.DATASET_PATH.exists():
            return None
        X_train, X_test, y_train, y_test = preprocessor.prepare_data(config.DATASET_PATH)
        _cache['data'] = {
            'X_train': X_train, 'X_test': X_test,
            'y_train': y_train, 'y_test': y_test
        }
    
    if _cache['models'] is None:
        logger.info("Training models...")
        data = _cache['data']
        trainer = ModelTrainer()
        models = trainer.train_all_models(data['X_train'], data['y_train'])
        
        evaluator = ModelEvaluator()
        results = evaluator.evaluate_all_models(models, data['X_test'], data['y_test'])
        
        _cache['models'] = models
        _cache['results'] = results
    
    return _cache['data'], _cache['models'], _cache['results']


# HTML Templates

MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fraud Detection Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --primary: #3498db;
            --secondary: #2c3e50;
            --success: #2ecc71;
            --danger: #e74c3c;
            --warning: #f39c12;
            --info: #9b59b6;
            --light: #ecf0f1;
            --dark: #34495e;
            --bg: #1a1a2e;
            --card-bg: #16213e;
            --border: #0f3460;
        }
        
        html {
            scroll-behavior: smooth;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, var(--bg) 0%, var(--secondary) 100%);
            color: var(--light);
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        /* Header */
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        header p {
            font-size: 1.1em;
            opacity: 0.95;
        }
        
        /* Navigation */
        nav {
            background: var(--secondary);
            padding: 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            position: sticky;
            top: 0;
            z-index: 99;
        }
        
        nav ul {
            list-style: none;
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            flex-wrap: wrap;
        }
        
        nav a {
            display: block;
            padding: 15px 25px;
            color: var(--light);
            text-decoration: none;
            transition: all 0.3s ease;
            border-bottom: 3px solid transparent;
        }
        
        nav a:hover {
            background: rgba(52, 152, 219, 0.2);
            border-bottom-color: var(--primary);
        }
        
        nav a.active {
            background: rgba(52, 152, 219, 0.3);
            border-bottom-color: var(--primary);
        }
        
        /* Container */
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* Section */
        section {
            margin-bottom: 40px;
        }
        
        section h2 {
            font-size: 2em;
            margin-bottom: 30px;
            color: var(--primary);
            border-bottom: 3px solid var(--primary);
            padding-bottom: 10px;
        }
        
        /* Grid */
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .grid.cols-2 {
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
        }
        
        .grid.full {
            grid-template-columns: 1fr;
        }
        
        /* Card */
        .card {
            background: var(--card-bg);
            border-radius: 10px;
            padding: 20px;
            border: 1px solid var(--border);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(52, 152, 219, 0.2);
            border-color: var(--primary);
        }
        
        .card h3 {
            color: var(--primary);
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .card p {
            opacity: 0.8;
            line-height: 1.6;
        }
        
        /* Metric */
        .metric {
            background: linear-gradient(135deg, rgba(52, 152, 219, 0.2) 0%, rgba(46, 204, 113, 0.2) 100%);
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid var(--primary);
            transition: all 0.3s ease;
        }
        
        .metric:hover {
            transform: scale(1.05);
        }
        
        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            color: var(--success);
            margin: 10px 0;
        }
        
        .metric-label {
            font-size: 0.9em;
            opacity: 0.8;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Chart Container */
        .chart-container {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
            min-height: 400px;
        }
        
        .chart-container canvas,
        .chart-container svg {
            max-height: 100%;
            max-width: 100%;
        }
        
        /* Tabs */
        .tabs {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin-bottom: 20px;
            border-bottom: 2px solid var(--border);
        }
        
        .tab-btn {
            padding: 12px 20px;
            background: transparent;
            color: var(--light);
            border: none;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s ease;
            border-bottom: 3px solid transparent;
        }
        
        .tab-btn:hover {
            background: rgba(52, 152, 219, 0.1);
        }
        
        .tab-btn.active {
            color: var(--primary);
            border-bottom-color: var(--primary);
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        /* Button */
        .btn {
            padding: 12px 25px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }
        
        .btn-primary {
            background: var(--primary);
            color: white;
        }
        
        .btn-primary:hover {
            background: #2980b9;
            box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
        }
        
        .btn-success {
            background: var(--success);
            color: white;
        }
        
        .btn-success:hover {
            background: #27ae60;
        }
        
        .btn-warning {
            background: var(--warning);
            color: white;
        }
        
        .btn-warning:hover {
            background: #e67e22;
        }
        
        /* Loading */
        .loading {
            text-align: center;
            padding: 40px;
        }
        
        .spinner {
            display: inline-block;
            width: 40px;
            height: 40px;
            border: 4px solid rgba(52, 152, 219, 0.3);
            border-top-color: var(--primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* Footer */
        footer {
            background: var(--secondary);
            padding: 30px 20px;
            text-align: center;
            border-top: 1px solid var(--border);
            margin-top: 60px;
            opacity: 0.8;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            header h1 {
                font-size: 1.8em;
            }
            
            .grid {
                grid-template-columns: 1fr;
            }
            
            .grid.cols-2 {
                grid-template-columns: 1fr;
            }
            
            nav a {
                padding: 12px 15px;
                font-size: 0.9em;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <h1>🔍 Fraud Detection System</h1>
            <p>Advanced Machine Learning for Financial Transaction Monitoring</p>
        </div>
    </header>
    
    <nav>
        <ul>
            <li><a href="#overview" class="nav-link active" onclick="showSection('overview')">📊 Overview</a></li>
            <li><a href="#analysis" class="nav-link" onclick="showSection('analysis')">📈 Analysis</a></li>
            <li><a href="#models" class="nav-link" onclick="showSection('models')">🤖 Models</a></li>
            <li><a href="#powerbi" class="nav-link" onclick="showSection('powerbi')">💼 Power BI</a></li>
        </ul>
    </nav>
    
    <div class="container">
        <!-- Overview Section -->
        <section id="overview" class="section">
            <h2>📊 System Overview</h2>
            
            <div id="metrics-container" class="grid">
                <div class="loading"><div class="spinner"></div></div>
            </div>
            
            <div class="grid cols-2">
                <div class="card">
                    <h3>📋 Dataset Information</h3>
                    <div id="dataset-info"></div>
                </div>
                <div class="card">
                    <h3>🎯 Class Distribution</h3>
                    <div class="chart-container" id="distribution-chart"></div>
                </div>
            </div>
        </section>
        
        <!-- Analysis Section -->
        <section id="analysis" class="section" style="display: none;">
            <h2>📈 Data Analysis</h2>
            
            <div class="tabs">
                <button class="tab-btn active" onclick="switchTab('analysis', 'correlation')">Feature Correlation</button>
                <button class="tab-btn" onclick="switchTab('analysis', 'distributions')">Distributions</button>
                <button class="tab-btn" onclick="switchTab('analysis', 'patterns')">Fraud Patterns</button>
            </div>
            
            <div id="analysis-correlation" class="tab-content active">
                <div class="card">
                    <div class="chart-container" id="correlation-chart"></div>
                </div>
            </div>
            
            <div id="analysis-distributions" class="tab-content">
                <div class="grid cols-2">
                    <div class="card">
                        <h3>Amount Distribution</h3>
                        <div class="chart-container" id="amount-chart"></div>
                    </div>
                    <div class="card">
                        <h3>Time Distribution</h3>
                        <div class="chart-container" id="time-chart"></div>
                    </div>
                </div>
            </div>
            
            <div id="analysis-patterns" class="tab-content">
                <div class="card">
                    <h3>Fraud Patterns</h3>
                    <p>Analyzing temporal and monetary patterns in fraudulent transactions...</p>
                </div>
            </div>
        </section>
        
        <!-- Models Section -->
        <section id="models" class="section" style="display: none;">
            <h2>🤖 Model Performance</h2>
            
            <div class="tabs">
                <button class="tab-btn active" onclick="switchTab('models', 'comparison')">Comparison</button>
                <button class="tab-btn" onclick="switchTab('models', 'roc')">ROC Curves</button>
                <button class="tab-btn" onclick="switchTab('models', 'confusion')">Confusion Matrices</button>
            </div>
            
            <div id="models-comparison" class="tab-content active">
                <div class="grid">
                    <div class="card">
                        <h3>Model Comparison</h3>
                        <div class="chart-container" id="comparison-chart"></div>
                    </div>
                </div>
                <div class="card full">
                    <h3>Performance Metrics</h3>
                    <div id="metrics-table"></div>
                </div>
            </div>
            
            <div id="models-roc" class="tab-content">
                <div class="grid cols-2">
                    <div class="card" id="roc-container"></div>
                </div>
            </div>
            
            <div id="models-confusion" class="tab-content">
                <div class="grid cols-2">
                    <div class="card" id="confusion-container"></div>
                </div>
            </div>
        </section>
        
        <!-- Power BI Section -->
        <section id="powerbi" class="section" style="display: none;">
            <h2>💼 Power BI Integration</h2>
            
            <div class="grid">
                <div class="card">
                    <h3>📤 Export Data</h3>
                    <p>Export your fraud detection data and model results in formats compatible with Microsoft Power BI for advanced business intelligence and real-time monitoring.</p>
                    <button class="btn btn-success" onclick="exportPowerBI()">Download Power BI Data</button>
                </div>
                <div class="card">
                    <h3>📊 Available Exports</h3>
                    <ul style="list-style: none; padding: 0;">
                        <li>✅ Model metrics and performance statistics</li>
                        <li>✅ Predictions and fraud probabilities</li>
                        <li>✅ Feature statistics and importance</li>
                        <li>✅ Confusion matrices</li>
                        <li>✅ Sample predictions for analysis</li>
                    </ul>
                </div>
            </div>
        </section>
    </div>
    
    <footer>
        <p><strong>Fraud Detection System v1.0.0</strong></p>
        <p>Data-driven insights for financial security | Last Updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M") + """</p>
    </footer>
    
    <script>
        // Navigation
        function showSection(sectionId) {
            document.querySelectorAll('section').forEach(s => s.style.display = 'none');
            document.getElementById(sectionId).style.display = 'block';
            
            document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
            event.target.classList.add('active');
            
            loadSectionData(sectionId);
        }
        
        // Tab switching
        function switchTab(sectionId, tabName) {
            document.querySelectorAll(`#${sectionId} .tab-content`).forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll(`#${sectionId} .tab-btn`).forEach(btn => {
                btn.classList.remove('active');
            });
            
            document.getElementById(`${sectionId}-${tabName}`).classList.add('active');
            event.target.classList.add('active');
        }
        
        // Load section data
        function loadSectionData(sectionId) {
            if (sectionId === 'overview') {
                loadMetrics();
                loadDistribution();
            } else if (sectionId === 'analysis') {
                loadCorrelation();
                loadDistributions();
            } else if (sectionId === 'models') {
                loadModelComparison();
            }
        }
        
        // Load metrics
        function loadMetrics() {
            fetch('/api/metrics')
                .then(r => r.json())
                .then(data => {
                    const html = data.metrics.map(m => `
                        <div class="metric">
                            <div class="metric-label">${m.label}</div>
                            <div class="metric-value">${m.value}</div>
                        </div>
                    `).join('');
                    document.getElementById('metrics-container').innerHTML = html;
                })
                .catch(e => console.error('Error loading metrics:', e));
        }
        
        // Export Power BI
        function exportPowerBI() {
            const btn = event.target;
            btn.disabled = true;
            btn.textContent = '📤 Exporting...';
            
            fetch('/api/export-powerbi')
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        alert('✅ Data exported successfully!\\nFiles saved to: ' + data.path);
                        btn.textContent = '✅ Export Complete!';
                    } else {
                        alert('❌ Export failed: ' + data.error);
                        btn.textContent = '📤 Export Data';
                        btn.disabled = false;
                    }
                })
                .catch(e => {
                    console.error('Error:', e);
                    alert('❌ Error during export');
                    btn.textContent = '📤 Export Data';
                    btn.disabled = false;
                });
        }
        
        // Initialize
        window.addEventListener('DOMContentLoaded', () => {
            loadSectionData('overview');
        });
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Render main dashboard."""
    return render_template_string(MAIN_TEMPLATE)


@app.route('/api/metrics')
def api_metrics():
    """Get overview metrics."""
    data, _, _ = load_data_and_models()
    
    if data is None:
        return jsonify({'error': 'Dataset not found'}), 404
    
    X_test, y_test = data['X_test'], data['y_test']
    
    metrics = [
        {'label': '📦 Total Transactions', 'value': f"{len(X_test):,}"},
        {'label': '⚠️ Fraud Rate', 'value': f"{(y_test.sum() / len(y_test) * 100):.2f}%"},
        {'label': '✅ Legitimate', 'value': f"{(y_test == 0).sum():,}"},
        {'label': '❌ Fraudulent', 'value': f"{(y_test == 1).sum():,}"},
    ]
    
    return jsonify({'metrics': metrics})


@app.route('/api/export-powerbi')
def api_export_powerbi():
    """Export data for Power BI."""
    try:
        data, models, results = load_data_and_models()
        
        if data is None:
            return jsonify({'success': False, 'error': 'Dataset not found'}), 404
        
        X_test, y_test = data['X_test'], data['y_test']
        
        # Get best model predictions
        best_model_name = max(results.items(), key=lambda x: x[1].get('f1', 0))[0]
        best_model = models[best_model_name]
        
        y_pred = best_model.predict(X_test)
        
        if hasattr(best_model, 'predict_proba'):
            y_pred_proba = best_model.predict_proba(X_test)[:, 1]
        else:
            y_pred_proba = best_model.decision_function(X_test)
        
        # Export
        exporter = PowerBIExporter()
        feature_names = [f"V{i}" for i in range(1, 29)] + ['Time', 'Amount']
        cm = confusion_matrix(y_test, y_pred)
        
        exported = exporter.export_all(
            results=results,
            y_true=y_test,
            y_pred=y_pred,
            y_pred_proba=y_pred_proba,
            X=X_test,
            feature_names=feature_names,
            cm=cm,
            model_name=best_model_name
        )
        
        return jsonify({
            'success': True,
            'path': str(config.OUTPUT_DIR),
            'files': list(exported.keys())
        })
    
    except Exception as e:
        logger.error(f"Error exporting Power BI data: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


def run_flask_app():
    """Run Flask development server."""
    print("🚀 Starting Fraud Detection Web Dashboard...")
    print("📊 Open your browser and navigate to: http://localhost:5000")
    print("\n" + "="*60)
    app.run(debug=True, port=5000, use_reloader=True)


if __name__ == '__main__':
    run_flask_app()
