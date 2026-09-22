"""Launcher script for Dune Character Generator Streamlit app."""

import sys
import subprocess
from pathlib import Path

if __name__ == "__main__":
    app_path = Path(__file__).parent / "src" / "app.py"
    cmd = [sys.executable, "-m", "streamlit", "run", str(app_path)]
    print(f"Launching Dune Character Generator web app: {' '.join(cmd)}")
    subprocess.run(cmd)
