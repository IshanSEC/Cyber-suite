"""
Tool Check Dialog for CyberSuite
"""
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, 
                               QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt

class ToolCheckDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Tool Installation Status")
        self.setMinimumSize(600, 400)
        self.init_ui()
        self.check_tools()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Installed Penetration Testing Tools")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Tool", "Status", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.table)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.check_tools)
        layout.addWidget(refresh_btn)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
    def check_tools(self):
        """Check which tools are installed"""
        tools_info = {
            'nmap': ('Nmap', 'Network scanner and security auditing tool'),
            'subfinder': ('Subfinder', 'In-depth subdomain enumeration tool'),
            'whatweb': ('whatweb', 'Next generation web scanner'),
            'sqlmap': ('SQLMap', 'Automatic SQL injection and database takeover tool'),
            'dirsearch': ('Dirsearch', 'Web path scanner and directory brute-forcer'),
            'nikto': ('Nikto', 'Web server vulnerability scanner'),
            'hydra': ('Hydra', 'Network logon cracker supporting many protocols'),
            'aircrack-ng': ('Aircrack-ng', 'WiFi security auditing tool suite'),
            'msfconsole': ('Metasploit', 'Metasploit Framework exploitation platform')
        }
        
        tools_status = self.controller.get_all_tools_status()
        
        self.table.setRowCount(len(tools_info))
        
        row = 0
        for tool, value in tools_info.items():
            display_name, description = value
            # Tool name
            self.table.setItem(row, 0, QTableWidgetItem(display_name))
            
            # Status
            installed = tools_status.get(tool, False)
            status_item = QTableWidgetItem("✅ Installed" if installed else "❌ Not Found")
            if installed:
                status_item.setForeground(Qt.green)
            else:
                status_item.setForeground(Qt.red)
            self.table.setItem(row, 1, status_item)
            
            # Description
            self.table.setItem(row, 2, QTableWidgetItem(description))
            
            row += 1
