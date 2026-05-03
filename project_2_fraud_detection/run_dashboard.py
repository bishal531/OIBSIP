"""
Run the interactive Streamlit application
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Start the Streamlit application."""
    app_path = Path(__file__).parent / "app.py"
    
    print("🚀 Starting Fraud Detection Dashboard...")
    print(f"📊 Opening Streamlit app from {app_path}")
    print("\n" + "="*60)
    print("The dashboard will open in your default browser.")
    print("If it doesn't open, navigate to: http://localhost:8501")
    print("="*60 + "\n")
    
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        str(app_path),
        "--theme.base", "dark",
        "--theme.primaryColor", "#3498db",
        "--theme.secondaryBackgroundColor", "#2c3e50",
        "--theme.textColor", "#ecf0f1"
    ])

if __name__ == "__main__":
    main()
