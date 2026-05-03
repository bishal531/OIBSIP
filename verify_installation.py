#!/usr/bin/env python
"""
🎨 Fraud Detection System - UI & Power BI Integration Verification
Verifies all components are properly installed and configured
"""

import sys
from pathlib import Path
import importlib.util

def check_file(file_path, description):
    """Check if a file exists."""
    exists = Path(file_path).exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {file_path}")
    return exists

def check_module(module_name, description):
    """Check if a Python module is installed."""
    try:
        importlib.import_module(module_name)
        print(f"✅ {description}: {module_name}")
        return True
    except ImportError:
        print(f"❌ {description}: {module_name}")
        return False

def main():
    """Run verification checks."""
    print("\n" + "="*70)
    print(" 🔍 FRAUD DETECTION SYSTEM - Installation Verification")
    print("="*70 + "\n")
    
    base_path = Path(__file__).parent
    
    # Check Python version
    print("📦 System Check")
    print("-" * 70)
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    py_ok = sys.version_info >= (3, 8)
    status = "✅" if py_ok else "❌"
    print(f"{status} Python Version: {py_version} (Required: 3.8+)\n")
    
    # Check UI Files
    print("🎨 UI Files")
    print("-" * 70)
    ui_files = [
        ("app.py", "Streamlit Dashboard"),
        ("web_app.py", "Flask Web Application"),
        ("run_dashboard.py", "Dashboard Runner Script"),
        ("setup_ui.py", "Interactive Setup Menu"),
        ("generate_dashboards.py", "HTML Dashboard Generator"),
    ]
    
    ui_ok = all(check_file(base_path / f, desc) for f, desc in ui_files)
    print()
    
    # Check Documentation Files
    print("📚 Documentation")
    print("-" * 70)
    docs = [
        ("GETTING_STARTED.md", "Getting Started Guide"),
        ("UI_GUIDE.md", "UI Features Guide"),
        ("POWERBI_GUIDE.md", "Power BI Integration Guide"),
        ("POWERBI_SETUP.md", "Power BI Setup Tutorial"),
        ("UI_INTEGRATION_SUMMARY.md", "Integration Summary"),
    ]
    
    docs_ok = all(check_file(base_path / f, desc) for f, desc in docs)
    print()
    
    # Check Dependencies
    print("📦 Python Dependencies")
    print("-" * 70)
    packages = [
        ("streamlit", "Streamlit"),
        ("flask", "Flask"),
        ("plotly", "Plotly"),
        ("pandas", "Pandas"),
        ("numpy", "NumPy"),
        ("sklearn", "Scikit-Learn"),
        ("openpyxl", "OpenPyXL (Excel export)"),
    ]
    
    deps_ok = all(check_module(pkg, desc) for pkg, desc in packages)
    print()
    
    # Check Data
    print("📂 Data Files")
    print("-" * 70)
    dataset_path = base_path / "data" / "raw" / "creditcard.csv"
    dataset_ok = check_file(dataset_path, "Kaggle Dataset")
    print()
    
    # Check Output Directory
    print("📁 Output Directory")
    print("-" * 70)
    output_dir = base_path / "output"
    output_ok = output_dir.exists()
    status = "✅" if output_ok else "❌"
    print(f"{status} Output Directory: {output_dir}")
    print()
    
    # Summary
    print("="*70)
    print(" ✅ VERIFICATION SUMMARY")
    print("="*70)
    
    all_ok = py_ok and ui_ok and docs_ok and output_ok
    
    print(f"✅ Python Version: {'Pass' if py_ok else 'Fail'}")
    print(f"{'✅' if ui_ok else '❌'} UI Files: {'Pass' if ui_ok else 'Fail'}")
    print(f"{'✅' if docs_ok else '❌'} Documentation: {'Pass' if docs_ok else 'Fail'}")
    print(f"{'✅' if deps_ok else '❌'} Dependencies: {'Pass' if deps_ok else 'Fail'}")
    print(f"{'⚠️ ' if not dataset_ok else '✅'} Dataset: {'Ready' if dataset_ok else 'Download from Kaggle'}")
    print(f"✅ Output Directory: {'Pass' if output_ok else 'Fail'}")
    print()
    
    if all_ok:
        print("🎉 All systems ready! Choose your interface:")
        print("   1. Streamlit:    streamlit run app.py")
        print("   2. Flask:        python web_app.py")
        print("   3. Setup Menu:   python setup_ui.py")
        print()
        print("📚 Start here: GETTING_STARTED.md")
    elif dataset_ok:
        print("⚠️  Some dependencies missing. Install with:")
        print("   pip install -r requirements.txt")
    else:
        print("❌ Please download the dataset from Kaggle first:")
        print("   https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud")
        print("   Save to: data/raw/creditcard.csv")
    
    print()
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
