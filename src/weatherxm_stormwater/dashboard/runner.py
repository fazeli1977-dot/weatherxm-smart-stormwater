import subprocess
import sys
from pathlib import Path

def main():
    dashboard_app = Path(__file__).parent / "app.py"
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(dashboard_app)])

if __name__ == "__main__":
    main()
