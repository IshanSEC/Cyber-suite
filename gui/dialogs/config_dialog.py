"""
Configuration Dialog for CyberSuite
"""
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QGroupBox, QTabWidget,
                               QWidget, QCheckBox)
from PySide6.QtCore import Qt

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CyberSuite Configuration")
        self.setMinimumSize(600, 400)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the configuration UI"""
        layout = QVBoxLayout(self)
        
        # Tabs for different config sections
        tabs = QTabWidget()
        
        # General settings
        general_widget = QWidget()
        general_layout = QVBoxLayout(general_widget)
        
        general_group = QGroupBox("General Settings")
        general_group_layout = QVBoxLayout()
        
        self.auto_save = QCheckBox("Auto-save scan results")
        self.auto_save.setChecked(True)
        general_group_layout.addWidget(self.auto_save)
        
        self.show_warnings = QCheckBox("Show security warnings")
        self.show_warnings.setChecked(True)
        general_group_layout.addWidget(self.show_warnings)
        
        general_group.setLayout(general_group_layout)
        general_layout.addWidget(general_group)
        general_layout.addStretch()
        
        tabs.addTab(general_widget, "General")
        
        # Tool paths
        tools_widget = QWidget()
        tools_layout = QVBoxLayout(tools_widget)
        
        tools_group = QGroupBox("Tool Paths (Optional)")
        tools_group_layout = QVBoxLayout()
        
        tools_info = QLabel("Leave empty to use system PATH")
        tools_info.setStyleSheet("color: #a6adc8;")
        tools_group_layout.addWidget(tools_info)
        
        # Nmap path
        nmap_layout = QHBoxLayout()
        nmap_layout.addWidget(QLabel("Nmap:"))
        self.nmap_path = QLineEdit()
        self.nmap_path.setPlaceholderText("/usr/bin/nmap")
        nmap_layout.addWidget(self.nmap_path)
        tools_group_layout.addLayout(nmap_layout)
        
        # Metasploit path
        msf_layout = QHBoxLayout()
        msf_layout.addWidget(QLabel("Metasploit:"))
        self.msf_path = QLineEdit()
        self.msf_path.setPlaceholderText("/usr/bin/msfconsole")
        msf_layout.addWidget(self.msf_path)
        tools_group_layout.addLayout(msf_layout)
        
        tools_group.setLayout(tools_group_layout)
        tools_layout.addWidget(tools_group)
        tools_layout.addStretch()
        
        tabs.addTab(tools_widget, "Tool Paths")
        
        layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.setObjectName("successButton")
        save_btn.clicked.connect(self.save_config)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
    def save_config(self):
        """Save configuration"""
        # In a real implementation, save to config file
        self.accept()
