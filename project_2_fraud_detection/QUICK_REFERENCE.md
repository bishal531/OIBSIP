# 🎯 Quick Reference Card

## 🚀 Start the Dashboard (Pick One)

```bash
# 1️⃣  Recommended - Streamlit (Easiest)
streamlit run app.py

# 2️⃣  Flask Web App (Advanced)
python web_app.py

# 3️⃣  Setup Menu (Guided)
python setup_ui.py

# 4️⃣  HTML Dashboards (Standalone)
python generate_dashboards.py
```

**Streamlit opens at**: http://localhost:8501  
**Flask opens at**: http://localhost:5000

---

## 📋 First Time Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Verify installation
python verify_installation.py

# 3. Launch dashboard
streamlit run app.py
```

---

## 📚 Documentation Quick Links

| Document | Purpose | Time |
|----------|---------|------|
| [GETTING_STARTED.md](GETTING_STARTED.md) | 👶 First-time users | 5 min |
| [UI_GUIDE.md](UI_GUIDE.md) | 🎨 UI features | 10 min |
| [POWERBI_SETUP.md](POWERBI_SETUP.md) | 💼 Power BI setup | 20 min |
| [WHATS_NEW.md](WHATS_NEW.md) | 📦 What's included | 5 min |
| [README.md](README.md) | 📖 Full overview | 15 min |

---

## 🎨 Streamlit Dashboard Pages

1. **🏠 Overview** - Key metrics & dataset info
2. **📈 Data Analysis** - Correlations & patterns
3. **🤖 Model Training** - Train ML models
4. **📊 Model Comparison** - Compare performance
5. **💼 Power BI Export** - Export to Excel
6. **⚙️ Settings** - Configuration

---

## 💼 Power BI Export

**In Streamlit Dashboard**:
1. Go to "💼 Power BI Export"
2. Click "📤 Download Power BI Data"
3. Files saved to `output/` folder

**Files Generated**:
- `model_metrics.xlsx` - Performance data
- `predictions.xlsx` - Predictions
- `feature_statistics.xlsx` - Feature stats
- `confusion_matrix_*.xlsx` - Matrices

**Import to Power BI**:
1. Open Power BI Desktop
2. Get Data → Excel
3. Select `.xlsx` files
4. Load and visualize

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Port already in use" | `streamlit run app.py --server.port 8502` |
| "Module not found" | `pip install -r requirements.txt` |
| "Dataset not found" | Download from [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) |
| "Charts not showing" | `streamlit cache clear` then restart |
| "Slow performance" | Close other apps, restart server |

---

## 📱 Dashboard Features

### Interactive Controls
- ✨ **Hover** over charts for details
- 🔄 **Click legend** to toggle series
- 🔍 **Zoom** into specific regions
- 📥 **Download** charts as PNG
- 🎚️ **Slide filters** to adjust data

### Data Visualizations
- 📊 Bar charts
- 📈 Line charts
- 🥧 Pie charts
- 🔥 Heatmaps
- 🎛️ KPI cards
- 📋 Data tables

---

## 🎯 Common Tasks

### View Model Performance
```
Navigate to: 📊 Model Comparison
Select Tab: Metrics or ROC Curves
View: Performance metrics for all models
```

### Analyze Fraud Patterns
```
Navigate to: 📈 Data Analysis
Select Tab: Fraud Patterns
View: Temporal and monetary patterns
```

### Export for Stakeholders
```
Navigate to: 💼 Power BI Export
Click: Download Power BI Data
Use: Create Power BI reports
Share: Professional dashboards
```

### Train New Models
```
Navigate to: 🤖 Model Training
Click: Train All Models
View: Training progress
Results: Model metrics table
```

---

## 📊 Key Metrics

**Displayed in Overview**:
- 📦 Total Transactions
- ⚠️ Fraud Rate (%)
- ✅ Legitimate Count
- ❌ Fraudulent Count

**Model Performance**:
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC

---

## 💡 Tips & Tricks

### Performance
- Use light computations first (Overview tab)
- Data Analysis loads faster with fewer features
- Model Comparison caches results

### Sharing
- Use HTML dashboards for quick sharing
- Power BI for stakeholder reports
- Screenshots for email/presentations

### Customization
- Edit theme in `.streamlit/config.toml`
- Modify colors in `web_app.py`
- Add new metrics in dashboard code

---

## 🆘 Quick Help

### Can't Find Something?
1. Check sidebar navigation
2. Look in documentation files
3. Run `verify_installation.py`

### Dashboard Won't Start?
1. Check Python version: `python --version`
2. Verify dependencies: `pip install -r requirements.txt`
3. Clear cache: `streamlit cache clear`
4. Try different port: `streamlit run app.py --server.port 8502`

### Data Not Loading?
1. Check dataset path: `data/raw/creditcard.csv`
2. Verify dataset size and format
3. Check available disk space
4. Restart dashboard

---

## 📞 Support Resources

**Built-in Help**:
- Verification tool: `python verify_installation.py`
- Documentation: Multiple `.md` files
- Error messages: Check console output

**External Resources**:
- [Streamlit Community](https://discuss.streamlit.io/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/streamlit)
- [Power BI Community](https://community.powerbi.com/)

---

## 🎓 Learning Paths

### Beginner (30 min)
1. Read GETTING_STARTED.md
2. Run `python setup_ui.py`
3. Explore Overview tab
4. View Data Analysis

### Intermediate (1 hour)
1. Train models
2. Compare performance
3. Export to Power BI
4. Create visualizations

### Advanced (2+ hours)
1. Customize dashboards
2. Create Power BI reports
3. Deploy to cloud
4. Set up monitoring

---

## 📋 File Locations

```
Dashboard Output:       output/dashboard.html
Power BI Exports:       output/*.xlsx
Trained Models:         models/
Application Logs:       logs/
Configuration:          config.py
Main Script:            main.py
```

---

## ✅ Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Dataset downloaded to `data/raw/creditcard.csv`
- [ ] Dashboard opens: `streamlit run app.py`
- [ ] Charts display correctly
- [ ] Can export to Power BI
- [ ] Read GETTING_STARTED.md

---

## 🚀 One-Liner Quick Start

```bash
pip install -r requirements.txt && streamlit run app.py
```

**Browser opens automatically at http://localhost:8501**

---

## 📞 Emergency Contact

If everything fails:
1. Run `python verify_installation.py`
2. Check error messages
3. Review GETTING_STARTED.md
4. Reinstall: `pip install -r requirements.txt --force-reinstall`

---

**Version**: 1.0.0  
**Status**: ✅ Ready to Use  
**Last Updated**: April 2026

Print this card for quick reference! 📝
