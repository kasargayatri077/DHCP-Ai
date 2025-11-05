#!/usr/bin/env python3
"""
One-click runner for the Streamlit app.
- Ensures a virtual environment exists in .venv/
- Installs requirements if needed
- Launches: streamlit run main.py

Usage: Double-click this file (on Windows it opens with pythonw/python)
       or run: python run.py
"""
import os
import sys
import subprocess
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
VENV_DIR = PROJECT_DIR / ".venv"
IS_WINDOWS = os.name == "nt"
PYTHON_EXE = VENV_DIR / ("Scripts/python.exe" if IS_WINDOWS else "bin/python")


def ensure_venv():
    if PYTHON_EXE.exists():
        return
    print("[setup] Creating virtual environment in .venv ...")
    subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])


def pip_install(requirements_file: Path):
    print("[setup] Upgrading pip ...")
    subprocess.check_call([str(PYTHON_EXE), "-m", "pip", "install", "--upgrade", "pip"]) 
    if requirements_file.exists():
        print("[setup] Installing requirements ...")
        subprocess.check_call([str(PYTHON_EXE), "-m", "pip", "install", "-r", str(requirements_file)])
    else:
        print("[setup] requirements.txt not found, skipping.")


def run_streamlit():
    print("[run] Starting Streamlit app ...")
    # Use -m to avoid PATH issues
    cmd = [str(PYTHON_EXE), "-m", "streamlit", "run", "main.py"]
    subprocess.call(cmd, cwd=str(PROJECT_DIR))


def main():
    try:
        ensure_venv()
        pip_install(PROJECT_DIR / "requirements.txt")
        run_streamlit()
    except subprocess.CalledProcessError as e:
        print(f"[error] A setup command failed with exit code {e.returncode}.")
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()
