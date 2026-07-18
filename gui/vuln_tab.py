"""
Vulnerability Scanner Tab for CyberSuite
"""
from typing import Any, Dict, List, Tuple
from PySide6.QtWidgets import (QAbstractItemView, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QTableWidget, QTableWidgetItem, QPushButton,
                               QGroupBox, QHeaderView)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor

from core.controller import Controller

class VulnTab(QWidget):
    def __init__(self, controller: Controller) -> None:
        super().__init__()
        self.controller = controller
        self.init_ui()
        
    def init_ui(self):
        """Initialize the vulnerability scanner UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("🛡️ Vulnerability Assessment")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        # Summary cards
        summary_layout = QHBoxLayout()
        
        self.critical_card, self.critical_card_value_label = self.create_severity_card("Critical", "0", "#f38ba8")
        self.high_card, self.high_card_value_label = self.create_severity_card("High", "0", "#fab387")
        self.medium_card, self.medium_card_value_label = self.create_severity_card("Medium", "0", "#f9e2af")
        self.low_card, self.low_card_value_label = self.create_severity_card("Low", "0", "#a6e3a1")
        
        summary_layout.addWidget(self.critical_card)
        summary_layout.addWidget(self.high_card)
        summary_layout.addWidget(self.medium_card)
        summary_layout.addWidget(self.low_card)
        
        layout.addLayout(summary_layout)
        
        # Vulnerabilities table
        table_group = QGroupBox("Discovered Vulnerabilities")
        table_layout = QVBoxLayout()
        
        self.vuln_table = QTableWidget()
        self.vuln_table.setColumnCount(5)
        self.vuln_table.setHorizontalHeaderLabels(["Severity", "Title", "Description", "Recommendation", "Date"])
        self.vuln_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.vuln_table.setAlternatingRowColors(True)
        self.vuln_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        table_layout.addWidget(self.vuln_table)
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh Vulnerabilities")
        refresh_btn.clicked.connect(self.load_vulnerabilities)
        
        export_btn = QPushButton("Export to Report")
        export_btn.clicked.connect(self.export_vulnerabilities)
        
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(export_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Auto-refresh setup
        self._last_vuln_count = -1
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.check_for_updates)
        self.update_timer.start(2000)
        self.check_for_updates()
        
    def check_for_updates(self):
        """Check for database changes and auto-refresh the table when a new vulnerability is discovered"""
        try:
            stats = self.controller.db_manager.get_statistics()
            current_count = stats.get('total_vulnerabilities', 0)
            if current_count != self._last_vuln_count:
                self._last_vuln_count = current_count
                self.load_vulnerabilities()
        except Exception as e:
            print(f"Error checking for vulnerability updates: {e}")

    def create_severity_card(self, title: str, value: str, color: str) -> Tuple[QGroupBox, QLabel]:
        """Create a severity card"""
        group = QGroupBox(title)
        layout = QVBoxLayout()
        
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet(f"font-size: 24pt; font-weight: bold; color: {color};")
        
        layout.addWidget(value_label)
        group.setLayout(layout)
        
        return group, value_label
    
    def load_vulnerabilities(self):
        """Load vulnerabilities from database"""
        try:
            vulns: List[Dict[str, Any]] = self.controller.get_vulnerabilities()
            
            # Update summary cards
            severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
            for vuln in vulns:
                severity = str(vuln.get('severity', 'low')).lower()
                if severity in severity_counts:
                    severity_counts[severity] += 1
            
            self.critical_card_value_label.setText(str(severity_counts['critical']))
            self.high_card_value_label.setText(str(severity_counts['high']))
            self.medium_card_value_label.setText(str(severity_counts['medium']))
            self.low_card_value_label.setText(str(severity_counts['low']))
            
            # Update table
            self.vuln_table.setRowCount(len(vulns))
            
            for row, vuln in enumerate(vulns):
                # Severity
                severity_item = QTableWidgetItem(vuln.get('severity', 'Unknown'))
                severity = vuln.get('severity', '').lower()
                if severity == 'critical':
                    severity_item.setBackground(QColor("#f38ba8"))
                elif severity == 'high':
                    severity_item.setBackground(QColor("#fab387"))
                elif severity == 'medium':
                    severity_item.setBackground(QColor("#f9e2af"))
                else:
                    severity_item.setBackground(QColor("#a6e3a1"))
                
                self.vuln_table.setItem(row, 0, severity_item)
                self.vuln_table.setItem(row, 1, QTableWidgetItem(vuln.get('title', '')))
                self.vuln_table.setItem(row, 2, QTableWidgetItem(str(vuln.get('description', ''))))
                self.vuln_table.setItem(row, 3, QTableWidgetItem(str(vuln.get('recommendation', ''))))
                self.vuln_table.setItem(row, 4, QTableWidgetItem(str(vuln.get('date', ''))))

        except Exception as e:
            print(f"Error loading vulnerabilities: {e}")
    
    def export_vulnerabilities(self):
        """Export vulnerabilities to report"""
        from PySide6.QtWidgets import QMessageBox
        
        QMessageBox.information(
            self,
            "Export",
            "Vulnerability export feature will be available in the Reports tab.\n"
            "Please navigate to the Reports tab to generate a full report."
        )
