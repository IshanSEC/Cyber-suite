"""
Main Window for CyberSuite
Contains the tab interface and main layout
"""
from typing import Any

from PySide6.QtWidgets import (QMainWindow, QTabWidget, QVBoxLayout, 
                               QWidget, QStatusBar, QMessageBox)
from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction
from gui.dashboard import DashboardTab
from gui.recon_tab import ReconTab
from gui.web_tab import WebTab
from gui.vuln_tab import VulnTab
from gui.network_tab import NetworkTab
from gui.password_tab import PasswordTab
from gui.exploit_tab import ExploitTab
from gui.report_tab import ReportTab
from core.controller import Controller

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = Controller()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("CyberSuite - All-in-One Penetration Testing Suite")
        self.setMinimumSize(1024, 768)
        self.showMaximized()
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setMovable(False)
        
        # Add tabs
        self.dashboard_tab = DashboardTab(self.controller)
        self.recon_tab = ReconTab(self.controller)
        self.web_tab = WebTab(self.controller)
        self.vuln_tab = VulnTab(self.controller)
        self.network_tab = NetworkTab(self.controller)
        self.password_tab = PasswordTab(self.controller)
        self.exploit_tab = ExploitTab(self.controller)
        self.report_tab = ReportTab(self.controller)
        
        self.tabs.addTab(self.dashboard_tab, "🏠 Dashboard")
        self.tabs.addTab(self.recon_tab, "🔍 Reconnaissance")
        self.tabs.addTab(self.web_tab, "🌐 Web Testing")
        self.tabs.addTab(self.vuln_tab, "🛡️ Vulnerability Scan")
        self.tabs.addTab(self.network_tab, "📡 Network")
        self.tabs.addTab(self.password_tab, "🔐 Password Attack")
        self.tabs.addTab(self.exploit_tab, "💥 Exploit")
        self.tabs.addTab(self.report_tab, "📊 Reports")
        
        layout.addWidget(self.tabs)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Update status periodically
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(1000)  # Update every second
        
    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_scan_action = QAction("&New Scan", self)
        new_scan_action.setShortcut("Ctrl+N")
        new_scan_action.triggered.connect(self.new_scan)
        file_menu.addAction(new_scan_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        config_action = QAction("&Configuration", self)
        config_action.triggered.connect(self.show_config)
        tools_menu.addAction(config_action)
        
        tools_menu.addSeparator()
        
        check_tools_action = QAction("Check &Installed Tools", self)
        check_tools_action.triggered.connect(self.check_tools)
        tools_menu.addAction(check_tools_action)
        
        # Database menu
        db_menu = menubar.addMenu("&Database")
        
        view_history_action = QAction("View Scan &History", self)
        view_history_action.triggered.connect(self.view_history)
        db_menu.addAction(view_history_action)
        
        clear_history_action = QAction("&Clear History", self)
        clear_history_action.triggered.connect(self.clear_history)
        db_menu.addAction(clear_history_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        docs_action = QAction("&Documentation", self)
        docs_action.triggered.connect(self.show_docs)
        help_menu.addAction(docs_action)
        
    def new_scan(self):
        """Start a new scan"""
        self.tabs.setCurrentIndex(1)  # Switch to Recon tab
        
    def show_config(self):
        """Show configuration dialog"""
        from gui.dialogs.config_dialog import ConfigDialog
        dialog = ConfigDialog(self)
        dialog.exec()
        
    def check_tools(self):
        """Check which tools are installed"""
        from gui.dialogs.tool_check_dialog import ToolCheckDialog
        dialog = ToolCheckDialog(self.controller, self)
        dialog.exec()
        
    def view_history(self):
        """View scan history"""
        self.tabs.setCurrentIndex(7)  # Switch to Reports tab
        
    def clear_history(self):
        """Clear scan history"""
        reply = QMessageBox.question(
            self, 
            "Clear History",
            "Are you sure you want to clear all scan history?\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.clear_database()
            self.status_bar.showMessage("Scan history cleared", 3000)
            
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About CyberSuite",
            "<h2>CyberSuite v1.0</h2>"
            "<p>All-in-One GUI Penetration Testing Suite</p>"
            "<p>Integrates major penetration testing tools into one powerful interface.</p>"
            "<p><b>Tools Integrated:</b></p>"
            "<ul>"
            "<li>Nmap - Network Scanner</li>"
            "<li>Subfinder - Subdomain Enumeration</li>"
            "<li>whatweb - Next Generation Web Scanner</li>"
            "<li>SQLMap - SQL Injection</li>"
            "<li>Dirsearch - Directory Brute Force</li>"
            "<li>Nikto - Web Scanner</li>"
            "<li>Hydra - Password Cracker</li>"
            "<li>Aircrack-ng - WiFi Security</li>"
            "<li>Metasploit - Exploitation Framework</li>"
            "</ul>"
            "<p><b>⚠️ For Educational and Authorized Testing Only</b></p>"
            "<p>© 2026 CyberSec Team</p>"
        )
        
    def show_docs(self):
        """Show documentation"""
        QMessageBox.information(
            self,
            "Documentation",
            "<h3>CyberSuite Documentation</h3>"
            "<p><b>Getting Started:</b></p>"
            "<ol>"
            "<li>Select a module from the tabs</li>"
            "<li>Enter target information</li>"
            "<li>Configure scan options</li>"
            "<li>Click 'Start Scan'</li>"
            "<li>View results in real-time</li>"
            "<li>Generate reports from the Reports tab</li>"
            "</ol>"
            "<p><b>Important:</b> Ensure you have permission to test the target systems.</p>"
            "<p>For detailed documentation, visit the Help menu.</p>"
        )
        
    def update_status(self):
        """Update status bar with current information"""
        active_scans = self.controller.get_active_scans_count()
        if active_scans > 0:
            self.status_bar.showMessage(f"Active scans: {active_scans} | Ready")
        else:
            self.status_bar.showMessage("Ready")

    def append_terminal(self, message: str) -> None:
        """Append message to the global dashboard terminal"""
        if hasattr(self, 'dashboard_tab'):
            self.dashboard_tab.log_terminal(message)

    def closeEvent(self, event: Any) -> None:
        """Handle window close event"""
        active_scans = self.controller.get_active_scans_count()
        if active_scans > 0:
            reply = QMessageBox.question(
                self,
                "Active Scans",
                f"There are {active_scans} active scan(s) running.\nAre you sure you want to exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
                
        event.accept()
