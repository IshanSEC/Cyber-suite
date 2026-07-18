"""
Report Tab for CyberSuite
Generate and export penetration testing reports
"""
from typing import Any, Dict, List, Optional

from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QAbstractItemView, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QTableWidget, QTableWidgetItem, QPushButton,
                               QGroupBox, QHeaderView, QFileDialog, QComboBox,
                               QTextEdit, QMessageBox)

from core.controller import Controller

class ReportTab(QWidget):
    def __init__(self, controller: Controller) -> None:
        super().__init__()
        self.controller = controller
        self.init_ui()
        
    def init_ui(self):
        """Initialize the report UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("📊 Reports & Export")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        # Report generation
        gen_group = QGroupBox("Generate Report")
        gen_layout = QVBoxLayout()
        
        # Report type
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Report Type:"))
        self.report_type = QComboBox()
        self.report_type.addItems(["Full Penetration Test Report", "Vulnerability Assessment", "Scan Summary"])
        type_layout.addWidget(self.report_type)
        gen_layout.addLayout(type_layout)
        
        # Export format
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Export Format:"))
        self.export_format = QComboBox()
        self.export_format.addItems(["PDF", "HTML", "JSON", "CSV"])
        format_layout.addWidget(self.export_format)
        gen_layout.addLayout(format_layout)
        
        # Generate button
        generate_btn = QPushButton("Generate Report")
        generate_btn.setObjectName("successButton")
        generate_btn.clicked.connect(self.generate_report)
        gen_layout.addWidget(generate_btn)
        
        gen_group.setLayout(gen_layout)
        layout.addWidget(gen_group)
        
        # Scan history
        history_group = QGroupBox("Scan History")
        history_layout = QVBoxLayout()
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels(["Scan ID", "Target", "Tool", "Date", "Status", "Action"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        history_layout.addWidget(self.history_table)
        
        # History controls
        history_controls = QHBoxLayout()
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_scan_history)
        export_history_btn = QPushButton("Export Selected")
        export_history_btn.clicked.connect(self.export_selected_scan)
        
        history_controls.addWidget(refresh_btn)
        history_controls.addWidget(export_history_btn)
        history_controls.addStretch()
        
        history_layout.addLayout(history_controls)
        history_group.setLayout(history_layout)
        layout.addWidget(history_group)
        
        # Report preview
        preview_group = QGroupBox("Report Preview")
        preview_layout = QVBoxLayout()
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setPlaceholderText("Report preview will appear here...")
        
        preview_layout.addWidget(self.preview_text)
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)
        
        # Load initial data
        self.load_scan_history()
        
    def load_scan_history(self) -> None:
        """Load scan history into table"""
        try:
            scans: List[Dict[str, Any]] = self.controller.get_scan_history(limit=50)
            
            self.history_table.setRowCount(len(scans))
            
            for row, scan in enumerate(scans):
                self.history_table.setItem(row, 0, QTableWidgetItem(scan['scan_id'][:8] + '...'))
                self.history_table.setItem(row, 1, QTableWidgetItem(scan['target']))
                self.history_table.setItem(row, 2, QTableWidgetItem(scan['tool']))
                self.history_table.setItem(row, 3, QTableWidgetItem(scan['date']))
                
                status_item = QTableWidgetItem(scan['status'])
                if scan['status'] == 'completed':
                    status_item.setForeground(QColor('green'))
                elif scan['status'] == 'failed':
                    status_item.setForeground(QColor('red'))
                self.history_table.setItem(row, 4, status_item)
                
                def create_view_handler(scan_id: str):
                    def handler(checked: bool = False) -> None:
                        self.view_scan_details(scan_id)
                    return handler

                view_btn = QPushButton("View")
                view_btn.clicked.connect(create_view_handler(scan['scan_id']))
                self.history_table.setCellWidget(row, 5, view_btn)
                
        except Exception as e:
            print(f"Error loading scan history: {e}")
    
    def view_scan_details(self, scan_id: str) -> None:
        """View detailed scan information"""
        scan_details: Optional[Dict[str, Any]] = self.controller.db_manager.get_scan_details(scan_id)
        if scan_details:
            preview_text = f"""
<h2>Scan Details</h2>
<p><b>Scan ID:</b> {scan_details['scan_id']}</p>
<p><b>Target:</b> {scan_details['target']}</p>
<p><b>Tool:</b> {scan_details['tool']}</p>
<p><b>Date:</b> {scan_details['date']}</p>
<p><b>Status:</b> {scan_details['status']}</p>

<h3>Output:</h3>
<pre>{scan_details.get('output', {}).get('output', 'No output available')}</pre>
            """
            self.preview_text.setHtml(preview_text)
    
    def generate_report(self):
        """Generate a penetration testing report"""
        report_type = self.report_type.currentText()
        export_format = self.export_format.currentText().lower()
        
        # Get file path
        file_filter = {
            'pdf': 'PDF Files (*.pdf)',
            'html': 'HTML Files (*.html)',
            'json': 'JSON Files (*.json)',
            'csv': 'CSV Files (*.csv)'
        }
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Report",
            f"pentest_report.{export_format}",
            file_filter.get(export_format, 'All Files (*)')
        )
        
        if not file_path:
            return
        
        try:
            from core.report_generator import ReportGenerator
            
            generator = ReportGenerator(self.controller.db_manager)
            
            if export_format == 'pdf':
                generator.generate_pdf_report(file_path, report_type)
            elif export_format == 'html':
                generator.generate_html_report(file_path, report_type)
            elif export_format == 'json':
                generator.generate_json_report(file_path)
            elif export_format == 'csv':
                generator.generate_csv_report(file_path)
            
            QMessageBox.information(
                self,
                "Report Generated",
                f"Report successfully generated:\n{file_path}"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to generate report:\n{str(e)}"
            )
    
    def export_selected_scan(self):
        """Export selected scan"""
        selected_rows = self.history_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a scan to export!")
            return
        
        QMessageBox.information(
            self,
            "Export",
            "Use the 'Generate Report' feature to export scan data."
        )
