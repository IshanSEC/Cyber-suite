"""
CyberSuite - All-in-One GUI Penetration Testing Suite
Main Entry Point
"""
import sys
import os

# Suppress common Qt/Linux warnings (DBus, Fontconfig, etc.)
os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.qpa.*=false"

# Explicitly initialize Fontconfig to suppress "using without calling FcInit()"
try:
    import ctypes
    ctypes.CDLL("libfontconfig.so.1").FcInit()
except Exception:
    pass

# pyrefly: ignore [missing-import]
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("CyberSuite")
    app.setOrganizationName("CyberSec")
    app.setStyle("Fusion")  # Modern cross-platform style
    
    # Apply dark theme
    from gui.themes.dark_theme import apply_dark_theme
    apply_dark_theme(app)
    
    window = MainWindow()
    window.showMaximized()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
