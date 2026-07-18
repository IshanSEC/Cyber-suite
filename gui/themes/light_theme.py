"""
Light Theme for CyberSuite
Clean, professional light mode
"""

def apply_light_theme(app):
    """Apply light theme to the application"""
    light_stylesheet = """
    QMainWindow {
        background-color: #ffffff;
    }
    
    QWidget {
        background-color: #ffffff;
        color: #333333;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 10pt;
    }
    
    QTabWidget::pane {
        border: 1px solid #cccccc;
        background-color: #f5f5f5;
        border-radius: 5px;
    }
    
    QTabBar::tab {
        background-color: #e0e0e0;
        color: #333333;
        padding: 10px 20px;
        margin: 2px;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
        min-width: 100px;
    }
    
    QTabBar::tab:selected {
        background-color: #4a90e2;
        color: #ffffff;
        font-weight: bold;
    }
    
    QTabBar::tab:hover {
        background-color: #d0d0d0;
    }
    
    QPushButton {
        background-color: #4a90e2;
        color: #ffffff;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        min-width: 100px;
    }
    
    QPushButton:hover {
        background-color: #357abd;
    }
    
    QPushButton:pressed {
        background-color: #2d5fa3;
    }
    
    QPushButton:disabled {
        background-color: #cccccc;
        color: #999999;
    }
    
    QPushButton#dangerButton {
        background-color: #e74c3c;
    }
    
    QPushButton#dangerButton:hover {
        background-color: #c0392b;
    }
    
    QPushButton#successButton {
        background-color: #27ae60;
    }
    
    QPushButton#successButton:hover {
        background-color: #229954;
    }
    
    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QComboBox {
        background-color: #ffffff;
        color: #333333;
        border: 2px solid #cccccc;
        border-radius: 5px;
        padding: 8px;
    }
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
        border: 2px solid #4a90e2;
    }
    
    QComboBox::drop-down {
        border: none;
        padding-right: 10px;
    }
    
    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid #333333;
        margin-right: 5px;
    }
    
    QComboBox QAbstractItemView {
        background-color: #ffffff;
        color: #333333;
        selection-background-color: #4a90e2;
        selection-color: #ffffff;
        border: 1px solid #cccccc;
    }
    
    QGroupBox {
        border: 2px solid #cccccc;
        border-radius: 5px;
        margin-top: 10px;
        padding-top: 10px;
        font-weight: bold;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 5px 10px;
        color: #4a90e2;
    }
    
    QLabel {
        background-color: transparent;
        color: #333333;
    }
    
    QLabel#titleLabel {
        font-size: 14pt;
        font-weight: bold;
        color: #4a90e2;
    }
    
    QLabel#subtitleLabel {
        font-size: 11pt;
        color: #666666;
    }
    
    QProgressBar {
        border: 2px solid #cccccc;
        border-radius: 5px;
        background-color: #f0f0f0;
        text-align: center;
        height: 20px;
    }
    
    QProgressBar::chunk {
        background-color: #4a90e2;
    }
    
    QScrollBar:vertical {
        background-color: #f5f5f5;
        width: 12px;
        border: none;
    }
    
    QScrollBar::handle:vertical {
        background-color: #cccccc;
        border-radius: 6px;
        min-height: 20px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #999999;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }
    
    QTableWidget {
        background-color: #ffffff;
        gridline-color: #e0e0e0;
        border: 1px solid #cccccc;
        border-radius: 5px;
    }
    
    QTableWidget::item {
        padding: 5px;
        border: none;
        background-color: #ffffff;
        color: #333333;
    }
    
    QTableWidget::item:selected {
        background-color: #e3f2fd;
        color: #333333;
    }
    
    QHeaderView::section {
        background-color: #e8e8e8;
        color: #333333;
        padding: 5px;
        border: none;
        font-weight: bold;
    }
    
    QMenuBar {
        background-color: #f5f5f5;
        color: #333333;
        border-bottom: 1px solid #cccccc;
    }
    
    QMenuBar::item:selected {
        background-color: #4a90e2;
        color: #ffffff;
    }
    
    QMenu {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #cccccc;
    }
    
    QMenu::item:selected {
        background-color: #4a90e2;
        color: #ffffff;
    }
    
    QCheckBox, QRadioButton {
        color: #333333;
        background-color: transparent;
    }
    
    QCheckBox:hover, QRadioButton:hover {
        color: #4a90e2;
    }
    """
    
    app.setStyleSheet(light_stylesheet)
