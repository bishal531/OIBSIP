# Interactive Dashboard & Power BI Guide

## 🎨 Interactive Dashboards

The fraud detection system now includes interactive Plotly dashboards that provide real-time insights into your fraud detection models.

### Features

✨ **Interactive Visualizations**
- Hover over charts to see detailed information
- Zoom, pan, and download charts as PNG
- Filter and explore data dynamically
- Mobile-responsive design

📊 **Available Charts**
1. **Class Distribution** - Transaction count by fraud/legitimate
2. **Feature Correlation** - Top features affecting fraud detection
3. **Model Comparison** - Performance across all trained models
4. **ROC Curves** - Model discrimination ability
5. **Confusion Matrices** - Prediction breakdown
6. **Amount Distribution** - Transaction amount patterns
7. **Time Distribution** - Fraud patterns by time of day

### Generating Dashboards

#### Option 1: Automatic Generation
```bash
python generate_dashboards.py
```

This will:
- Train all models
- Evaluate performance
- Generate interactive HTML dashboards
- Export data for Power BI

#### Option 2: Manual in Python
```python
from src.dashboard import InteractiveDashboard
import pandas as pd

dashboard = InteractiveDashboard()

# Create a chart
fig = dashboard.create_class_distribution_chart(y_test)

# Save to HTML
dashboard.save_interactive_html(fig, "my_chart.html")
```

### Viewing Dashboards

1. **Open in Browser**
   ```bash
   # Open the main dashboard
   output/dashboard.html
   
   # Or individual charts
   output/01_class_distribution.html
   output/02_feature_correlation.html
   output/03_model_comparison_f1.html
   ```

2. **Interactive Features**
   - **Hover**: See exact values
   - **Click Legend**: Toggle series on/off
   - **Double-click**: Isolate one series
   - **Download**: Camera icon to save as PNG
   - **Zoom**: Box select to zoom, double-click to reset

---

## 📊 Power BI Integration

Export fraud detection data directly to Power BI for advanced analytics and real-time monitoring.

### What Gets Exported

**1. Model Metrics** (`model_metrics.xlsx`)
- All evaluation metrics for each model
- Accuracy, Precision, Recall, F1-Score, ROC-AUC
- Side-by-side comparison

**2. Predictions** (`predictions.xlsx`)
- Individual predictions for each transaction
- True labels vs predicted labels
- Fraud probability scores
- Correctness indicator

**3. Feature Statistics** (`feature_statistics.xlsx`)
- Statistical comparison of features
- Legitimate vs Fraudulent patterns
- Mean, Std, Min, Max values
- Feature importance ranking

**4. Confusion Matrix** (`confusion_matrix_*.xlsx`)
- True positives, false positives, etc.
- Percentage breakdowns
- Color-coded visualization

### Generating Power BI Exports

#### Option 1: Automatic Export
```bash
python generate_dashboards.py
```

All exports automatically saved to `output/` folder

#### Option 2: Manual Export
```python
from src.power_bi_export import PowerBIExporter

exporter = PowerBIExporter()

# Export individual items
exporter.export_model_metrics(results)
exporter.export_predictions(y_true, y_pred, y_pred_proba, feature_names)
exporter.export_feature_statistics(X, y)
exporter.export_confusion_matrix(cm, model_name)

# Or export everything at once
exported_files = exporter.export_all(
    results, y_true, y_pred, y_pred_proba, X, feature_names, cm
)
```

### Importing into Power BI Desktop

#### Step-by-Step Guide

1. **Open Power BI Desktop**
   - Download from: https://powerbi.microsoft.com/downloads/

2. **Get Data → Excel**
   - File → Get data → Excel
   - Select the first Excel file (e.g., `model_metrics.xlsx`)

3. **Load Tables**
   - Select all sheets you want
   - Click "Load"

4. **Repeat for Other Files**
   - Import `predictions.xlsx`
   - Import `feature_statistics.xlsx`
   - Import `confusion_matrix_*.xlsx`

5. **Create Relationships**
   - Model → Manage relationships
   - Link prediction tables if needed
   - Set up foreign keys

6. **Create Visualizations**
   - Click Insert → Choose visualization
   - Drag fields to axes
   - Create interactive reports

### Sample Power BI Dashboard

Create these visualizations:

**Page 1: Model Performance**
- Clustered bar chart: Model comparison by F1-Score
- KPI cards: Best model's key metrics
- Gauge charts: Model performance indicators
- Table: Detailed metrics for all models

**Page 2: Predictions Analysis**
- Clustered bar chart: Prediction correctness
- Card: Total predictions
- Card: Accuracy percentage
- Card: Fraud detection rate
- Pie chart: Correct vs Incorrect predictions

**Page 3: Feature Insights**
- Table: Feature statistics
- Scatter plot: Legitimate vs Fraudulent means
- Clustered column chart: Mean differences
- Slicer: Filter by feature importance

**Page 4: Model Details**
- Matrix: Confusion matrix values
- Gauge: Precision
- Gauge: Recall
- Gauge: F1-Score

### Power BI Features

✨ **Interactive Filtering**
- Drill-through reports
- Cross-filtering between pages
- Dynamic slicers

📊 **Real-time Updates**
- Refresh data from source
- Scheduled refreshes
- Direct Query (if connected to database)

🔐 **Sharing & Collaboration**
- Publish to Power BI Service
- Share with team members
- Set up access levels

### Advanced Power BI Tips

#### 1. Data Modeling
```
Use Power Query to:
- Clean and transform data
- Remove duplicates
- Create calculated columns
- Combine multiple sources
```

#### 2. DAX Formulas
```powerbi
# Example: Calculate fraud detection rate
Fraud_Rate = 
    DIVIDE(
        SUMX(Predictions, Predictions[Predicted]),
        COUNTA(Predictions[Index])
    )

# Example: Model accuracy
Accuracy = 
    DIVIDE(
        SUMX(Predictions, Predictions[Is_Correct]),
        COUNTA(Predictions[Index])
    )
```

#### 3. Custom Visuals
- Download from Power BI Marketplace
- Add advanced charts
- Enhance interactivity

---

## 🚀 Combining Interactive Dashboards and Power BI

**For Quick Analysis:** Use interactive HTML dashboards
- Instant generation
- No software installation
- Easy sharing via email/web

**For Enterprise Reporting:** Use Power BI
- Advanced analytics
- Team collaboration
- Real-time monitoring
- Professional dashboards

### Workflow

```
Fraud Detection Model
         ↓
    Evaluation
         ↓
  ┌─────┴─────┐
  ↓           ↓
HTML Dash   Power BI
(Quick)     (Enterprise)
```

---

## 📁 Output Files Structure

```
output/
├── dashboard.html                    # Main dashboard
├── 01_class_distribution.html        # Class distribution chart
├── 02_feature_correlation.html       # Feature correlation chart
├── 03_model_comparison_f1.html       # Model comparison by F1
├── 04_model_comparison_roc_auc.html # Model comparison by ROC-AUC
├── roc_curve_*.html                 # ROC curves for each model
├── confusion_matrix_*.html          # Confusion matrices
├── 05_amount_distribution.html      # Amount distribution
├── 06_time_distribution.html        # Time distribution
│
├── model_metrics.xlsx               # For Power BI
├── predictions.xlsx                 # For Power BI
├── feature_statistics.xlsx          # For Power BI
└── confusion_matrix_*.xlsx          # For Power BI
```

---

## 🎯 Best Practices

### Dashboard Design
1. **Clarity**: Use clear titles and labels
2. **Color**: Use consistent color schemes
3. **Interactivity**: Enable drill-downs
4. **Performance**: Optimize for fast loading

### Power BI Dashboards
1. **Hierarchy**: Follow logical flow
2. **Storytelling**: Create narrative
3. **Updates**: Refresh on schedule
4. **Security**: Implement row-level security

---

## 🔗 Resources

- **Plotly Documentation**: https://plotly.com/python/
- **Power BI Documentation**: https://learn.microsoft.com/power-bi/
- **Power BI Desktop**: https://powerbi.microsoft.com/downloads/
- **Power BI Community**: https://community.powerbi.com/

---

## 💡 Tips & Tricks

### For Interactive Dashboards
- Use `-` in titles to add descriptive subtitles
- Color-code by category (green=good, red=bad)
- Add annotations for key insights
- Export charts as images for presentations

### For Power BI
- Create bookmarks for different views
- Use buttons for navigation
- Implement tooltips for additional context
- Set up alerts for anomalies

---

**Happy Analyzing! 📊**
