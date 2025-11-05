@echo off
setlocal

REM Activate venv or create if missing, then run Streamlit
if exist .\.venv\Scripts\python.exe (
  call .\.venv\Scripts\activate.bat
) else (
  echo [setup] Creating virtual environment in .venv ...
  python -m venv .venv
  call .\.venv\Scripts\activate.bat
  echo [setup] Upgrading pip and installing requirements ...
  python -m pip install --upgrade pip
  if exist requirements.txt (
    python -m pip install -r requirements.txt
  ) else (
    echo [warn] requirements.txt not found, continuing...
  )
)

REM Run the app
python -m streamlit run main.py

endlocal
