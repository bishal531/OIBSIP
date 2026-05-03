"""
Interactive setup script to choose and run the UI
"""

import subprocess
import sys
import os
from pathlib import Path


def print_header():
    """Print welcome header."""
    print("\n" + "="*70)
    print(" 🔍 FRAUD DETECTION SYSTEM - Interactive UI Setup")
    print("="*70 + "\n")


def print_options():
    """Print available options."""
    print("Choose your UI preference:")
    print()
    print("1️⃣  Streamlit Dashboard (Recommended)")
    print("   ✨ Most interactive and feature-rich")
    print("   📱 Professional dark theme")
    print("   🚀 Easiest to use\n")
    
    print("2️⃣  Flask Web Application")
    print("   🌐 Modern web interface")
    print("   ⚡ Advanced customization")
    print("   📊 Real-time updates\n")
    
    print("3️⃣  Generate HTML Dashboards")
    print("   📄 Standalone HTML files")
    print("   🔗 No server required")
    print("   💾 Easy to share\n")
    
    print("4️⃣  Jupyter Notebook Analysis")
    print("   📓 Interactive notebook")
    print("   🔬 Detailed exploration")
    print("   📈 Step-by-step analysis\n")
    
    print("5️⃣  Install Dependencies & Exit")
    print("   📦 Only install packages\n")


def check_dependencies():
    """Check if required packages are installed."""
    required = ['streamlit', 'flask', 'plotly', 'pandas', 'scikit-learn']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"⚠️  Missing packages: {', '.join(missing)}")
        install = input("Install now? (y/n): ").lower()
        if install == 'y':
            install_dependencies()
    
    return len(missing) == 0


def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], check=True)
        print("✅ Dependencies installed successfully!\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}\n")
        return False
    
    return True


def run_streamlit():
    """Run Streamlit app."""
    app_path = Path(__file__).parent / "app.py"
    
    print("\n🚀 Starting Streamlit Dashboard...")
    print("📊 The dashboard will open in your browser at http://localhost:8501")
    print("💡 Tip: Press Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", str(app_path),
            "--theme.base", "dark",
            "--theme.primaryColor", "#3498db"
        ])
    except KeyboardInterrupt:
        print("\n\n✅ Streamlit server stopped.")


def run_flask():
    """Run Flask app."""
    app_path = Path(__file__).parent / "web_app.py"
    
    print("\n🚀 Starting Flask Web Application...")
    print("🌐 The app will open in your browser at http://localhost:5000")
    print("💡 Tip: Press Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([sys.executable, str(app_path)])
    except KeyboardInterrupt:
        print("\n\n✅ Flask server stopped.")


def generate_html_dashboards():
    """Generate HTML dashboards."""
    print("\n📊 Generating HTML dashboards...")
    dashboard_script = Path(__file__).parent / "generate_dashboards.py"
    
    try:
        subprocess.run([sys.executable, str(dashboard_script)], check=True)
        print("\n✅ Dashboards generated successfully!")
        
        output_dir = Path(__file__).parent / "output"
        if output_dir.exists():
            print(f"\n📁 Dashboards saved to: {output_dir}")
            print("\nGenerated files:")
            for file in sorted(output_dir.glob("*.html")):
                print(f"  📄 {file.name}")
            
            open_html = input("\nOpen main dashboard in browser? (y/n): ").lower()
            if open_html == 'y':
                main_dashboard = output_dir / "dashboard.html"
                if main_dashboard.exists():
                    import webbrowser
                    webbrowser.open(f"file:///{main_dashboard}")
                    print(f"\n🌐 Opening: {main_dashboard}")
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating dashboards: {e}")


def run_jupyter():
    """Run Jupyter notebook."""
    print("\n📓 Starting Jupyter Lab...")
    print("🔬 Interactive analysis environment\n")
    
    try:
        subprocess.run([sys.executable, "-m", "jupyter", "lab"])
    except KeyboardInterrupt:
        print("\n\n✅ Jupyter Lab stopped.")


def main():
    """Main menu loop."""
    print_header()
    
    # Check dependencies
    if not check_dependencies():
        print("⚠️  Some dependencies are missing.")
        print("Please install them using option 5.\n")
    
    while True:
        print_options()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                print()
                run_streamlit()
            elif choice == '2':
                print()
                run_flask()
            elif choice == '3':
                print()
                generate_html_dashboards()
            elif choice == '4':
                print()
                run_jupyter()
            elif choice == '5':
                print()
                if install_dependencies():
                    print("✅ Setup complete!")
                    break
            else:
                print("\n❌ Invalid choice. Please enter 1-5.\n")
                continue
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
        
        again = input("\nRun again? (y/n): ").lower()
        if again != 'y':
            print("\n👋 Goodbye!")
            break
        
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled.")
