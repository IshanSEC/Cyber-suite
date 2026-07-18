"""
Dashboard Tab for CyberSuite
Shows overview, statistics, and quick actions
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QGroupBox, QGridLayout, QPushButton, QTableWidget,
                               QTableWidgetItem, QHeaderView, QComboBox, QFileDialog, QMessageBox, QScrollArea, QApplication, QFrame, QTextEdit, QLineEdit)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, QSize
from PySide6.QtGui import QFont, QColor, QTextCursor
import csv
from datetime import datetime
from gui.themes.dark_theme import apply_dark_theme
from gui.themes.light_theme import apply_light_theme
from PySide6.QtGui import QPainter, QPainterPath, QPen, QBrush
from PySide6.QtCore import QRectF
import html

class SeverityDonutChart(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(150, 150)
        self.data = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        self.colors = {
            'critical': QColor("#f38ba8"), # Red
            'high': QColor("#fab387"),     # Orange
            'medium': QColor("#f9e2af"),   # Yellow
            'low': QColor("#89b4fa")       # Blue
        }
        
    def update_data(self, stats):
        if 'vulnerabilities_by_severity' in stats:
            by_sev = stats['vulnerabilities_by_severity']
            self.data['critical'] = by_sev.get('critical', 0)
            self.data['high'] = by_sev.get('high', 0)
            self.data['medium'] = by_sev.get('medium', 0)
            self.data['low'] = by_sev.get('low', 0)
            self.update()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        size = min(rect.width(), rect.height()) - 30
        chart_rect = QRectF(rect.center().x() - size/2, rect.center().y() - size/2, size, size)
        
        total = sum(self.data.values())
        if total == 0:
            painter.setPen(QPen(QColor("#313244"), 20))
            painter.drawArc(chart_rect, 0, 360 * 16)
            painter.setPen(QColor("#cdd6f4"))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "No Vulns")
            return
            
        start_angle = 90 * 16
        for sev, count in self.data.items():
            if count == 0: continue
            span_angle = -(count / total) * 360 * 16
            
            pen = QPen(self.colors[sev], 20)
            painter.setPen(pen)
            painter.drawArc(chart_rect, int(start_angle), int(span_angle))
            start_angle += span_angle
            
        painter.setPen(QColor("#cdd6f4"))
        font = painter.font()
        font.setBold(True)
        font.setPointSize(16)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(total))

from PySide6.QtWidgets import QGraphicsDropShadowEffect

def apply_shadow(widget):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(15)
    shadow.setColor(QColor(0, 0, 0, 80))
    shadow.setOffset(0, 4)
    widget.setGraphicsEffect(shadow)

class StatCard(QFrame):
    """Wrapper class for stat card with typed value_label attribute"""
    def __init__(self, title: str, color: str):
        super().__init__()
        self.setObjectName("StatCard")
        self.setStyleSheet(f"""
            QFrame#StatCard {{
                background-color: #1e293b;
                border-radius: 12px;
            }}
        """)
        apply_shadow(self)
        self.value_label: QLabel = None

class DashboardTab(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.button_animations = {}  # Store button animations by id
        self.init_ui()
        
        # Auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_stats)
        self.refresh_timer.start(5000)  # Refresh every 5 seconds
        
    def init_ui(self):
        """Initialize the dashboard UI with flexible, scrollable layout"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        # Container widget for scrollable content
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(20)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title section
        title_layout = QVBoxLayout()
        title_layout.setSpacing(5)
        
        title = QLabel("CyberSuite Dashboard")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title)
        
        subtitle = QLabel("All-in-One Penetration Testing Suite")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(subtitle)
        
        layout.addLayout(title_layout)
        
        # Target Scope Manager
        scope_group = QGroupBox("Global Target Scope")
        scope_layout = QHBoxLayout()
        scope_layout.addWidget(QLabel("🎯 Current Target:"))
        self.global_target_input = QLineEdit()
        self.global_target_input.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        self.global_target_input.setPlaceholderText("e.g., example.com or 192.168.1.0/24")
        scope_layout.addWidget(self.global_target_input)
        scope_group.setLayout(scope_layout)
        layout.addWidget(scope_group)
        
        # Controls section
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setMaximumWidth(120)
        refresh_btn.clicked.connect(self.refresh_stats)
        controls_layout.addWidget(refresh_btn)
        
        controls_layout.addStretch()
        
        theme_combo = QComboBox()
        theme_combo.addItems(["Light", "Dark"])
        theme_combo.setMaximumWidth(100)
        theme_combo.currentTextChanged.connect(self.change_theme)
        controls_layout.addWidget(theme_combo)
        
        layout.addLayout(controls_layout)
        
        # Statistics cards - responsive grid
        stats_group = QGroupBox("Statistics Overview")
        stats_layout = QGridLayout()
        stats_layout.setSpacing(10)
        stats_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create stat cards
        self.total_scans_label = self.create_stat_card("Total Scans", "0", "#38bdf8", "↑ +12%", "#22c55e")
        self.total_targets_label = self.create_stat_card("Targets", "0", "#a6e3a1")
        self.active_scans_label = self.create_stat_card("Active Scans", "0", "#fab387")
        self.avg_time_label = self.create_stat_card("Avg Scan Time", "0s", "#cba6f7")
        
        # Donut chart inside a styled card
        self.donut_chart = SeverityDonutChart()
        vuln_dist_group = QFrame()
        vuln_dist_group.setStyleSheet("background-color: #1e293b; border-radius: 12px;")
        apply_shadow(vuln_dist_group)
        vd_layout = QVBoxLayout(vuln_dist_group)
        
        vd_title = QLabel("Vulnerability Distribution")
        vd_title.setStyleSheet("color: #94a3b8; font-size: 13px; font-weight: bold;")
        vd_layout.addWidget(vd_title)
        vd_layout.addWidget(self.donut_chart)
        
        stats_layout.addWidget(self.total_scans_label, 0, 0)
        stats_layout.addWidget(self.total_targets_label, 0, 1)
        stats_layout.addWidget(self.active_scans_label, 1, 0)
        stats_layout.addWidget(self.avg_time_label, 1, 1)
        stats_layout.addWidget(vuln_dist_group, 0, 2, 2, 1)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Quick Actions
        quick_actions_group = QWidget()
        quick_actions_layout = QGridLayout(quick_actions_group)
        quick_actions_layout.setSpacing(15)
        quick_actions_layout.setContentsMargins(5, 5, 5, 5)
        
        nmap_btn = self.create_action_btn("🔍", "Quick Nmap Scan", "Scan open ports instantly", lambda: self.quick_action('nmap'))
        web_btn = self.create_action_btn("🌐", "Web Vulnerability", "Find XSS & SQLi flaws", lambda: self.quick_action('web'))
        network_btn = self.create_action_btn("📡", "Network Scan", "Discover network devices", lambda: self.quick_action('network'))
        password_btn = self.create_action_btn("🔐", "Password Attack", "Test weak credentials", lambda: self.quick_action('password'))
        exploit_btn = self.create_action_btn("💣", "Exploit Check", "Search Exploit-DB", lambda: self.quick_action('exploit'))
        full_btn = self.create_action_btn("💥", "Full Pentest", "Automated attack chain", lambda: self.quick_action('full'))
        
        quick_actions_layout.addWidget(nmap_btn, 0, 0)
        quick_actions_layout.addWidget(web_btn, 0, 1)
        quick_actions_layout.addWidget(network_btn, 0, 2)
        quick_actions_layout.addWidget(password_btn, 1, 0)
        quick_actions_layout.addWidget(exploit_btn, 1, 1)
        quick_actions_layout.addWidget(full_btn, 1, 2)
        
        layout.addWidget(quick_actions_group)

        terminal_group = QFrame()
        terminal_group.setStyleSheet("background-color: #1e293b; border-radius: 12px;")
        apply_shadow(terminal_group)
        terminal_layout = QVBoxLayout(terminal_group)
        
        term_title = QLabel("Activity Feed")
        term_title.setStyleSheet("color: #94a3b8; font-size: 13px; font-weight: bold;")
        terminal_layout.addWidget(term_title)

        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setMinimumHeight(180)
        self.terminal_output.setPlaceholderText("Tool output from all running modules will appear here...")
        self.terminal_output.setStyleSheet("""
            QTextEdit {
                background-color: #0f172a;
                color: #cbd5e1;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-family: Consolas, 'Courier New', monospace;
                font-size: 12px;
            }
        """)
        terminal_layout.addWidget(self.terminal_output)
        layout.addWidget(terminal_group)
        
        # Recent Scans
        recent_scans_group = QGroupBox("Recent Activity")
        recent_scans_layout = QVBoxLayout()
        recent_scans_layout.setSpacing(10)
        recent_scans_layout.setContentsMargins(10, 10, 10, 10)
        
        # Header with title and export button
        header_layout = QHBoxLayout()
        activity_label = QLabel("Last 10 Scans")
        activity_font = QFont()
        activity_font.setPointSize(11)
        activity_font.setBold(True)
        activity_label.setFont(activity_font)
        header_layout.addWidget(activity_label)
        header_layout.addStretch()
        
        export_btn = QPushButton("📥 Export CSV")
        export_btn.setMaximumWidth(120)
        export_btn.clicked.connect(self.export_scans)
        header_layout.addWidget(export_btn)
        
        recent_scans_layout.addLayout(header_layout)
        
        # Table with improved styling
        self.recent_scans_table = QTableWidget()
        self.recent_scans_table.setColumnCount(5)
        self.recent_scans_table.setHorizontalHeaderLabels(["Target", "Tool", "Date", "Status", "Action"])
        self.recent_scans_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.recent_scans_table.horizontalHeader().setStretchLastSection(True)
        self.recent_scans_table.setAlternatingRowColors(True)
        self.recent_scans_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.recent_scans_table.setSortingEnabled(True)
        self.recent_scans_table.setMinimumHeight(250)
        self.recent_scans_table.setMaximumHeight(350)
        self.recent_scans_table.verticalHeader().setVisible(False)
        self.apply_table_styling(self.recent_scans_table)
        
        recent_scans_layout.addWidget(self.recent_scans_table)
        recent_scans_group.setLayout(recent_scans_layout)
        layout.addWidget(recent_scans_group)

        # Tool Installation Status
        tools_group = QFrame()
        tools_group.setStyleSheet("background-color: #1e293b; border-radius: 12px;")
        apply_shadow(tools_group)
        tools_layout = QVBoxLayout(tools_group)
        tools_layout.setContentsMargins(15, 15, 15, 15)
        
        tools_title = QLabel("Tool Installation Status")
        tools_title.setStyleSheet("color: #94a3b8; font-size: 13px; font-weight: bold;")
        tools_layout.addWidget(tools_title)
        
        self.tool_status_label = QLabel()
        self.tool_status_label.setStyleSheet("font-size: 13px;")
        tools_layout.addWidget(self.tool_status_label)
        
        layout.addWidget(tools_group)
        
        # Add stretch to push content to top
        layout.addStretch()
        
        # Set container as scroll area widget
        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)
        
        # Initial data load
        self.refresh_stats()
        self.load_recent_scans()
        self.check_tools()
        self.log_terminal("Dashboard terminal ready.")
        
    def create_stat_card(self, title: str, value: str, color: str, trend: str = "", trend_color: str = "") -> StatCard:
        """Create a flexible statistics card"""
        card = StatCard(title, color)
        card.setMinimumSize(160, 110)
        card.setMaximumSize(240, 140)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Value label (BIG)
        value_label = QLabel(value)
        value_label.setStyleSheet(f"color: {color}; font-size: 32px; font-weight: 800; border: none;")
        
        # Title and Trend
        title_layout = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #94a3b8; font-size: 13px; font-weight: 600; border: none;")
        title_layout.addWidget(title_label)
        
        if trend:
            trend_label = QLabel(trend)
            trend_label.setStyleSheet(f"color: {trend_color}; font-size: 12px; font-weight: bold; border: none;")
            title_layout.addWidget(trend_label)
            
        title_layout.addStretch()
            
        layout.addWidget(value_label)
        layout.addLayout(title_layout)
        
        card.setLayout(layout)
        card.value_label = value_label
        return card

    def create_action_btn(self, icon: str, title: str, desc: str, action) -> QPushButton:
        btn = QPushButton()
        btn.setMinimumHeight(65)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                border: none;
                border-radius: 12px;
                text-align: left;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #334155;
            }
        """)
        apply_shadow(btn)
        
        # Internal layout
        l = QHBoxLayout(btn)
        l.setContentsMargins(10, 5, 10, 5)
        
        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet("font-size: 24px; color: #38bdf8; background: transparent;")
        
        text_l = QVBoxLayout()
        text_l.setSpacing(2)
        t = QLabel(title)
        t.setStyleSheet("font-weight: 800; font-size: 14px; color: #f8fafc; background: transparent;")
        d = QLabel(desc)
        d.setStyleSheet("color: #94a3b8; font-size: 11px; background: transparent;")
        text_l.addWidget(t)
        text_l.addWidget(d)
        
        l.addWidget(icon_lbl)
        l.addLayout(text_l)
        l.addStretch()
        
        btn.clicked.connect(action)
        return btn
    
    def refresh_stats(self) -> None:
        """Refresh dashboard statistics"""
        try:
            stats: dict = self.controller.db_manager.get_statistics()
            
            self.total_scans_label.value_label.setText(str(stats.get('total_scans', 0)))
            self.total_targets_label.value_label.setText(str(stats.get('total_targets', 0)))
            self.active_scans_label.value_label.setText(str(self.controller.get_active_scans_count()))
            self.avg_time_label.value_label.setText(str(stats.get('avg_scan_time', '0s')))
            self.donut_chart.update_data(stats)
            self.check_tools()
        except Exception as e:
            print(f"Error refreshing stats: {e}")
        self.load_recent_scans()
    
    def load_recent_scans(self):
        """Load recent scans into the table"""
        try:
            scans = self.controller.get_scan_history(limit=10)
            
            self.recent_scans_table.setRowCount(len(scans))
            
            for row, scan in enumerate(scans):
                # Target
                target_item = QTableWidgetItem(scan['target'])
                self.recent_scans_table.setItem(row, 0, target_item)
                
                # Tool
                tool_item = QTableWidgetItem(scan['tool'])
                self.recent_scans_table.setItem(row, 1, tool_item)
                
                # Date
                date_item = QTableWidgetItem(scan['date'])
                self.recent_scans_table.setItem(row, 2, date_item)
                
                # Status with color coding
                status = scan['status'].lower()
                if status == 'completed':
                    status_text = "🟢 Completed"
                    color = "#22c55e" # Green
                elif status == 'failed':
                    status_text = "🔴 Failed"
                    color = "#ef4444" # Red
                elif status == 'running':
                    status_text = "🟡 Running"
                    color = "#f59e0b" # Orange
                else:
                    status_text = f"🟣 {status.capitalize()}"
                    color = "#cba6f7" # Purple
                
                status_item = QTableWidgetItem(status_text)
                status_item.setForeground(QColor(color))
                self.recent_scans_table.setItem(row, 3, status_item)
                
                # Action button
                view_btn = QPushButton("View")
                view_btn.setMaximumWidth(50)
                view_btn.setMaximumHeight(30)
                view_btn.clicked.connect(lambda sid=scan['scan_id']: self.view_scan(sid))
                self.recent_scans_table.setCellWidget(row, 4, view_btn)
                
                # Set row height
                self.recent_scans_table.setRowHeight(row, 35)
                
        except Exception as e:
            print(f"Error loading recent scans: {e}")
    
    def check_tools(self):
        """Check installed tools"""
        tools_status = self.controller.get_all_tools_status()
        
        status_html = '<table width="100%"><tr>'
        col = 0
        for tool, installed in tools_status.items():
            icon = "✅" if installed else "❌"
            color = "#a6e3a1" if installed else "#f38ba8" 
            status_html += f'<td style="color: {color}; font-weight: bold; padding: 5px;">{icon} {tool.upper()}</td>'
            col += 1
            if col >= 4:
                status_html += '</tr><tr>'
                col = 0
        status_html += '</tr></table>'
        
        self.tool_status_label.setText(status_html)
    
    def quick_action(self, action_type):
        """Handle quick action buttons"""
        from PySide6.QtWidgets import QMessageBox
        
        if action_type == 'nmap':
            # Switch to Recon tab
            parent = self.parent()
            while parent and not hasattr(parent, 'tabs'):
                parent = parent.parent()
            if parent:
                parent.tabs.setCurrentIndex(1)
        elif action_type == 'web':
            parent = self.parent()
            while parent and not hasattr(parent, 'tabs'):
                parent = parent.parent()
            if parent:
                parent.tabs.setCurrentIndex(2)
        elif action_type == 'password':
            parent = self.parent()
            while parent and not hasattr(parent, 'tabs'):
                parent = parent.parent()
            if parent:
                parent.tabs.setCurrentIndex(5)
        elif action_type == 'network':
            parent = self.parent()
            while parent and not hasattr(parent, 'tabs'):
                parent = parent.parent()
            if parent:
                parent.tabs.setCurrentIndex(3)  # Assuming network tab is index 3
        elif action_type == 'exploit':
            parent = self.parent()
            while parent and not hasattr(parent, 'tabs'):
                parent = parent.parent()
            if parent:
                parent.tabs.setCurrentIndex(4)  # Assuming exploit tab is index 4
        elif action_type == 'full':
            target = self.global_target_input.text().strip()
            if not target:
                QMessageBox.warning(self, "Missing Target", "Please set a target in the Global Target Scope to run a full pentest.")
                return
                
            reply = QMessageBox.question(
                self,
                "Start Full Pentest",
                f"Are you sure you want to run an automated pentest against {target}?\n"
                "This will sequence Nmap, WhatWeb, and Nuclei automatically.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.log_terminal(f"🚀 Starting full automated pentest against: {target}")
                self.controller.start_full_pentest(
                    target,
                    callback=self._full_pentest_done,
                    stream_cb=self._append_feed
                )
                
    def _append_feed(self, msg: str) -> None:
        self.log_terminal(msg)
        
    def _full_pentest_done(self, scan_id: str, result: dict) -> None:
        self.log_terminal("✅ Full automated pentest completed.")
        self.refresh_stats()

    def view_scan(self, scan_id):
        """View scan details"""
        from PySide6.QtWidgets import QMessageBox
        
        scan_details = self.controller.db_manager.get_scan_details(scan_id)
        if scan_details:
            details_text = f"""
            <b>Scan ID:</b> {scan_details['scan_id']}<br>
            <b>Target:</b> {scan_details['target']}<br>
            <b>Tool:</b> {scan_details['tool']}<br>
            <b>Date:</b> {scan_details['date']}<br>
            <b>Status:</b> {scan_details['status']}<br>
            """
            
            QMessageBox.information(self, "Scan Details", details_text)
    
    
    def export_scans(self):
        """Export recent scans to CSV"""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Target", "Tool", "Date", "Status"])
                    
                    for row in range(self.recent_scans_table.rowCount()):
                        row_data: list[str] = []
                        for col in range(4):  # Skip Action column
                            item = self.recent_scans_table.item(row, col)
                            row_data.append(item.text() if item else "")
                        writer.writerow(row_data)
                        
                QMessageBox.information(self, "Export Successful", f"Scans exported to {file_path}")
            except Exception as e:
                QMessageBox.warning(self, "Export Failed", f"Error: {str(e)}")
    
    def change_theme(self, theme: str) -> None:
        """Change the application theme"""
        app = QApplication.instance()
        if app:
            if theme == "Light":
                apply_light_theme(app)
            elif theme == "Dark":
                apply_dark_theme(app)
    
    def setup_button_animation(self, button: QPushButton) -> None:
        """Setup click animation for button"""
        button.clicked.connect(lambda: self.animate_button_click(button))
        # Store animation reference to prevent garbage collection
        self.button_animations[id(button)] = None
    
    def set_button_style(self, button: QPushButton) -> None:
        """Set animated stylesheet for button"""
        button.setStyleSheet("""
            QPushButton {
                background-color: #e8f0ff;
                color: #333333;
                border: 2px solid #b0d0f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: 500;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #d4e4f7;
                border: 2px solid #8ab4e0;
            }
            QPushButton:pressed {
                background-color: #c0d9f7;
                border: 2px solid #5a7fbf;
                padding: 6px 10px;
            }
        """)
    
    def animate_button_click(self, button: QPushButton) -> None:
        """Create click animation for button with visual feedback"""
        # Stop any existing animation
        button_id = id(button)
        if button_id in self.button_animations and self.button_animations[button_id]:
            self.button_animations[button_id].stop()
        
        # Store original stylesheet
        original_style = button.styleSheet()
        
        # Apply pressed effect
        pressed_style = """
            QPushButton {
                background-color: #c0d9f7 !important;
                border: 2px solid #5a7fbf !important;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 12px;
                font-weight: bold;
            }
        """
        button.setStyleSheet(pressed_style)
        
        # Create timer to restore style with animation
        def restore_style():
            # Animated transition back
            hover_style = """
                QPushButton {
                    background-color: #d4e4f7 !important;
                    border: 2px solid #8ab4e0 !important;
                    border-radius: 8px;
                    padding: 8px 12px;
                    font-size: 12px;
                    transition: all 150ms ease-out;
                }
            """
            button.setStyleSheet(hover_style)
            
            # Restore original after transition
            QTimer.singleShot(100, lambda: button.setStyleSheet(original_style))
        
        # Apply restoration with delay
        QTimer.singleShot(100, restore_style)
    
    def apply_table_styling(self, table):
        """Apply styling to the table"""
        table.setStyleSheet("""
            QTableWidget {
                background-color: transparent;
                gridline-color: transparent;
                border: none;
            }
            QTableWidget::item {
                padding: 10px;
                border: none;
                border-bottom: 1px solid #334155;
            }
            QTableWidget::item:hover {
                background-color: #334155;
            }
            QTableWidget::item:selected {
                background-color: #38bdf8;
                color: #0f172a;
            }
            QPushButton {
                background-color: #1e293b;
                color: #38bdf8;
                border: 1px solid #38bdf8;
                border-radius: 4px;
                padding: 4px 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #38bdf8;
                color: #0f172a;
            }
        """)

    def log_terminal(self, message: str) -> None:
        """Append a message to the shared dashboard terminal with activity feed icons."""
        if not hasattr(self, 'terminal_output'):
            return

        icon = "🔹"
        upper = message.upper()
        if "NMAP" in upper: icon = "🔍"
        elif "WHATWEB" in upper: icon = "🕷️"
        elif "NUCLEI" in upper: icon = "☢️"
        elif "SQLMAP" in upper: icon = "💉"
        color = "#cbd5e1"
        if "ERROR" in upper or "FAILED" in upper or "❌" in upper: 
            icon = "✖"
            color = "#ef4444"
        elif "CRITICAL" in upper: 
            icon = "🚨"
            color = "#ef4444"
        elif "COMPLETED" in upper or "SUCCESS" in upper or "✅" in upper:
            icon = "✔"
            color = "#22c55e"
        elif "START" in upper or "🚀" in upper:
            icon = "🚀"
            color = "#38bdf8"
        elif "⚠" in upper or "WARNING" in upper:
            icon = "⚠"
            color = "#f59e0b"

        safe_msg = html.escape(message.replace("🕷️", "").replace("✅", "").replace("🚀", "").replace("❌", "").replace("🚨", "").strip())
        line = f"<span style='color:#64748b; font-size:11px;'>[{datetime.now().strftime('%H:%M:%S')}]</span> <span style='color:{color}; font-weight:bold;'>{icon}</span> <span style='color:{color};'>{safe_msg}</span>"
        self.terminal_output.append(line)
        self.terminal_output.moveCursor(QTextCursor.MoveOperation.End)
