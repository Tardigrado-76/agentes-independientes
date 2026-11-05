"""
Script para generar el acceso directo en el Escritorio para el Agent Evaluation Framework.
"""

import os
import sys


def create_desktop_shortcut():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    bat_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "INICIAR_AGENT_EVALUATION.bat")
    shortcut_path = os.path.join(desktop, "IWAN - Agent Evaluation Framework.lnk")
    
    try:
        from win32com.client import Dispatch
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = bat_path
        shortcut.WorkingDirectory = os.path.dirname(bat_path)
        shortcut.IconLocation = sys.executable
        shortcut.save()
        print(f"[OK] Acceso directo creado en: {shortcut_path}")
    except (ImportError, OSError, RuntimeError):
        # Fallback via PowerShell with escaped quotes
        import subprocess
        ps_script = f"$s=(New-Object -COM WScript.Shell).CreateShortcut('{shortcut_path}');$s.TargetPath='{bat_path}';$s.WorkingDirectory='{os.path.dirname(bat_path)}';$s.Save()"
        cmd = ["powershell", "-NoProfile", "-Command", ps_script]
        subprocess.run(cmd, check=False)
        print(f"[OK] Acceso directo generado via PowerShell en: {shortcut_path}")

if __name__ == "__main__":
    create_desktop_shortcut()
