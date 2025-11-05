"""
Create a Desktop shortcut to run the Streamlit app with one double-click.
- Shortcut target: run_app.bat in the project root
- No extra Python packages required (uses Windows Script Host via VBScript)

Usage:
  python create_shortcut.py
This will place "DiabetesApp.lnk" on your Desktop.
"""
import os
from pathlib import Path
import subprocess
import tempfile


def create_shortcut(shortcut_name: str = "DiabetesApp.lnk"):
    desktop = Path(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
    project_dir = Path(__file__).resolve().parent
    bat_path = project_dir / "run_app.bat"

    if not bat_path.exists():
        raise FileNotFoundError(f"{bat_path} not found. Please make sure run_app.bat exists in the project root.")

    # Use a temporary VBScript to create the shortcut without extra dependencies
    vbs_content = f"""
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{str((desktop / shortcut_name)).replace('\\', r'\\')}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{str(bat_path).replace('\\', r'\\')}"
oLink.WorkingDirectory = "{str(project_dir).replace('\\', r'\\')}"
oLink.IconLocation = "{str(bat_path).replace('\\', r'\\')}, 0"
oLink.Save
"""

    with tempfile.TemporaryDirectory() as tmpdir:
        vbs_path = Path(tmpdir) / "make_shortcut.vbs"
        vbs_path.write_text(vbs_content, encoding="utf-8")
        # Run cscript to execute the VBScript silently
        subprocess.check_call(["cscript", "//NoLogo", str(vbs_path)])
    print(f"Shortcut created on Desktop: {desktop / shortcut_name}")


if __name__ == "__main__":
    try:
        create_shortcut()
    except Exception as e:
        print(f"Failed to create shortcut: {e}")
