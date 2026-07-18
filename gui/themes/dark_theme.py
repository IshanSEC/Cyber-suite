"""
Dark Theme for CyberSuite
Professional cybersecurity-themed dark mode
"""

def apply_dark_theme(app):
    """Apply dark theme to the application"""
    dark_stylesheet = """
    QMainWindow {
        background-color: #0f172a;
    }
    
    QWidget {
        background-color: #0f172a;
        color: #f8fafc;
        font-family: 'Inter', 'Poppins', 'Segoe UI', sans-serif;
        font-size: 10pt;
    }
    
    QTabWidget::pane {
        border: none;
        background-color: #0f172a;
    }
    
    QTabBar::tab {
        background-color: #1e293b;
        color: #94a3b8;
        padding: 10px 20px;
        margin: 2px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        min-width: 100px;
    }
    
    QTabBar::tab:selected {
        background-color: #38bdf8;
        color: #0f172a;
        font-weight: bold;
    }
    
    QTabBar::tab:hover {
        background-color: #334155;
    }
    
    QPushButton {
        background-color: #1e293b;
        color: #f8fafc;
        border: none;
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: bold;
        min-width: 100px;
    }
    
    QPushButton:hover {
        background-color: #38bdf8;
        color: #0f172a;
    }
    
    QPushButton:pressed {
        background-color: #0284c7;
    }
    
    QPushButton:disabled {
        background-color: #1e293b;
        color: #475569;
    }
    
    QPushButton#dangerButton {
        background-color: #ef4444;
        color: white;
    }
    
    QPushButton#dangerButton:hover {
        background-color: #f87171;
    }
    
    QPushButton#successButton {
        background-color: #22c55e;
        color: white;
    }
    
    QPushButton#successButton:hover {
        background-color: #4ade80;
    }
    
    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QComboBox {
        background-color: #1e293b;
        color: #f8fafc;
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 8px;
    }
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
        border: 1px solid #38bdf8;
    }
    
    QComboBox::drop-down {
        border: none;
        padding-right: 10px;
    }
    
    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid #cdd6f4;
        margin-right: 5px;
    }
    
    QComboBox QAbstractItemView {
        background-color: #1e293b;
        color: #f8fafc;
        selection-background-color: #38bdf8;
        selection-color: #0f172a;
        border: 1px solid #334155;
    }
    
    QGroupBox {
        border: none;
        background-color: transparent;
        margin-top: 25px;
        font-weight: bold;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0px 5px;
        color: #94a3b8;
        font-size: 11pt;
    }
    
    QLabel {
        background-color: transparent;
        color: #cbd5e1;
    }
    
    QLabel#titleLabel {
        font-size: 18pt;
        font-weight: 800;
        color: #f8fafc;
        letter-spacing: 1px;
    }
    
    QLabel#subtitleLabel {
        font-size: 11pt;
        color: #94a3b8;
        font-weight: 400;
    }
    
    QProgressBar {
        border: none;
        border-radius: 4px;
        text-align: center;
        background-color: #1e293b;
        color: #f8fafc;
    }
    
    QProgressBar::chunk {
        background-color: #38bdf8;
        border-radius: 4px;
    }
    
    QStatusBar {
        background-color: #0f172a;
        color: #94a3b8;
        border-top: 1px solid #1e293b;
    }
    
    QMenuBar {
        background-color: #0f172a;
        color: #f8fafc;
        border-bottom: 1px solid #1e293b;
    }
    
    QMenuBar::item:selected {
        background-color: #1e293b;
    }
    
    QMenu {
        background-color: #1e293b;
        color: #f8fafc;
        border: 1px solid #334155;
    }
    
    QMenu::item:selected {
        background-color: #38bdf8;
        color: #0f172a;
    }
    
    QScrollBar:vertical {
        background-color: #0f172a;
        width: 10px;
        border-radius: 5px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #334155;
        border-radius: 5px;
        min-height: 20px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #475569;
    }
    
    QScrollBar:horizontal {
        background-color: #0f172a;
        height: 10px;
        border-radius: 5px;
    }
    
    QScrollBar::handle:horizontal {
        background-color: #334155;
        border-radius: 5px;
        min-width: 20px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: #475569;
    }
    
    QScrollBar::add-line, QScrollBar::sub-line {
        border: none;
        background: none;
    }
    
    QTableWidget {
        background-color: #1e293b;
        alternate-background-color: #0f172a;
        gridline-color: transparent;
        border: none;
        border-radius: 8px;
    }
    
    QTableWidget::item {
        padding: 5px;
        color: #cbd5e1;
        border-bottom: 1px solid #334155;
    }
    
    QTableWidget::item:selected {
        background-color: #38bdf8;
        color: #0f172a;
    }
    
    QHeaderView::section {
        background-color: #0f172a;
        color: #94a3b8;
        padding: 10px;
        border: none;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    QCheckBox {
        spacing: 8px;
        color: #cdd6f4;
    }
    
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border: 2px solid #45475a;
        border-radius: 3px;
        background-color: #313244;
    }
    
    QCheckBox::indicator:checked {
        background-color: #89b4fa;
        border-color: #89b4fa;
    }
    
    QRadioButton {
        spacing: 8px;
        color: #cdd6f4;
    }
    
    QRadioButton::indicator {
        width: 18px;
        height: 18px;
        border: 2px solid #45475a;
        border-radius: 9px;
        background-color: #313244;
    }
    
    QRadioButton::indicator:checked {
        background-color: #89b4fa;
        border-color: #89b4fa;
    }
    
    QToolTip {
        background-color: #313244;
        color: #cdd6f4;
        border: 1px solid #89b4fa;
        padding: 5px;
        border-radius: 3px;
    }
    """
    
    app.setStyleSheet(dark_stylesheet)
