"""
Web Testing Tab for CyberSuite
Includes SQLMap, Dirsearch, and Nikto with a unified interface
"""
from typing import Any, Dict, Optional
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLayout, QLabel, 
                               QLineEdit, QPushButton, QTextEdit, QComboBox,
                               QGroupBox, QCheckBox, QProgressBar,
                               QSpinBox, QMessageBox)
from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtGui import QCloseEvent, QFont, QTextCursor

class ScanThread(QObject):
    # Explicitly typed signal to satisfy Pylance
    finished = Signal(str, dict)
    output = Signal(str)
    
    def __init__(self, controller: Any, tool: str, target: str, options: Dict[str, Any]):
        super().__init__()
        self.controller = controller
        self.tool = tool
        self.target = target
        self.options = options
        self._is_running = True
        self.scan_id = None
        
    def start(self) -> None:
        def callback(scan_id: str, result: Dict[str, Any]) -> None:
            if self._is_running:
                self.finished.emit(scan_id, result)

        def stream_cb(line: str) -> None:
            if self._is_running:
                self.output.emit(line)

        # Verify controller has the required method
        if hasattr(self.controller, 'start_scan'):
            self.scan_id = self.controller.start_scan(self.tool, self.target, self.options, callback, stream_cb)

    def isRunning(self) -> bool:
        return self._is_running

    def stop(self) -> None:
        self._is_running = False
        if self.scan_id and hasattr(self.controller, 'stop_scan'):
            self.controller.stop_scan(self.scan_id)

class WebTab(QWidget):
    def __init__(self, controller: Any):
        super().__init__()
        self.controller = controller
        self.scan_thread: Optional[ScanThread] = None
        self.init_ui()
        
    def init_ui(self) -> None:
        """Initialize the web testing UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)
        
        # Title
        title = QLabel("🌐 Web Application Testing")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        target_group = QGroupBox("Target Configuration")
        target_layout = QHBoxLayout(target_group)
        target_layout.addWidget(QLabel("Target URL/Host:"))
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("e.g., http://example.com/page.php?id=1 or ctuuniversity.in")
        target_layout.addWidget(self.target_input)
        layout.addWidget(target_group)

        tool_group = QGroupBox("Tool Selection")
        tool_layout = QHBoxLayout(tool_group)
        tool_layout.addWidget(QLabel("Scan Tool:"))
        self.tool_combo = QComboBox()
        self.tool_combo.addItems(["SQLMap", "Dirsearch", "Nikto", "Nuclei", "FFuF"])
        self.tool_combo.currentIndexChanged.connect(self.on_tool_changed)
        tool_layout.addWidget(self.tool_combo)
        layout.addWidget(tool_group)

        self.options_group = QGroupBox("Scan Options")
        self.options_layout = QVBoxLayout(self.options_group)
        layout.addWidget(self.options_group)

        self.create_sqlmap_options()

        controls_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start Scan")
        self.start_btn.setObjectName("successButton")
        self.start_btn.clicked.connect(self.start_scan)
        controls_layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("Stop Scan")
        self.stop_btn.setObjectName("dangerButton")
        self.stop_btn.clicked.connect(self.stop_scan)
        controls_layout.addWidget(self.stop_btn)
        controls_layout.addStretch()
        layout.addLayout(controls_layout)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.hide()
        layout.addWidget(self.progress)

        terminal_group = QGroupBox("Live Terminal")
        terminal_layout = QVBoxLayout(terminal_group)
        self.web_terminal = QTextEdit()
        self.web_terminal.setReadOnly(True)
        self.web_terminal.setFont(QFont("Consolas", 10))
        self.web_terminal.setStyleSheet(
            "QTextEdit { background-color: #0d1117; color: #c9d1d9; border: 1px solid #30363d; padding: 8px; }"
        )
        self.web_terminal.setPlaceholderText("Live terminal output will appear here...")
        terminal_layout.addWidget(self.web_terminal)
        layout.addWidget(terminal_group)

        self.log_terminal("Web testing live terminal ready.")
        
    def on_tool_changed(self, index: int) -> None:
        self.clear_layout(self.options_layout)

        tool = self.tool_combo.currentText().lower()
        if tool == 'sqlmap':
            self.create_sqlmap_options()
        elif tool == 'dirsearch':
            self.create_dirsearch_options()
        elif tool == 'nuclei':
            self.create_nuclei_options()
        elif tool == 'ffuf':
            self.create_ffuf_options()
        else:
            self.create_nikto_options()

    def clear_layout(self, layout: QLayout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            if item is None:
                continue

            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
                continue

            child_layout = item.layout()
            if child_layout:
                self.clear_layout(child_layout)
                child_layout.deleteLater()

            spacer = item.spacerItem()
            if spacer is not None:
                continue

    def create_sqlmap_options(self) -> None:
        risk_layout = QHBoxLayout()
        risk_layout.addWidget(QLabel("Risk Level (1-3):"))
        self.sqlmap_risk = QSpinBox()
        self.sqlmap_risk.setRange(1, 3)
        risk_layout.addWidget(self.sqlmap_risk)
        self.options_layout.addLayout(risk_layout)

        level_layout = QHBoxLayout()
        level_layout.addWidget(QLabel("Level (1-5):"))
        self.sqlmap_level = QSpinBox()
        self.sqlmap_level.setRange(1, 5)
        level_layout.addWidget(self.sqlmap_level)
        self.options_layout.addLayout(level_layout)

        self.sqlmap_enumerate_dbs = QCheckBox("Enumerate Databases")
        self.options_layout.addWidget(self.sqlmap_enumerate_dbs)

    def create_dirsearch_options(self) -> None:
        ext_layout = QHBoxLayout()
        ext_layout.addWidget(QLabel("Extensions:"))
        self.dirsearch_extensions = QLineEdit("php,html,js,txt")
        ext_layout.addWidget(self.dirsearch_extensions)
        self.options_layout.addLayout(ext_layout)

        threads_layout = QHBoxLayout()
        threads_layout.addWidget(QLabel("Threads:"))
        self.dirsearch_threads = QSpinBox()
        self.dirsearch_threads.setRange(1, 50)
        self.dirsearch_threads.setValue(10)
        threads_layout.addWidget(self.dirsearch_threads)
        self.options_layout.addLayout(threads_layout)

    def create_nikto_options(self) -> None:
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Port:"))
        self.nikto_port = QSpinBox()
        self.nikto_port.setRange(1, 65535)
        self.nikto_port.setValue(80)
        port_layout.addWidget(self.nikto_port)
        self.options_layout.addLayout(port_layout)

        self.nikto_ssl = QCheckBox("Use SSL/HTTPS")
        self.options_layout.addWidget(self.nikto_ssl)

    def create_nuclei_options(self) -> None:
        template_layout = QHBoxLayout()
        template_layout.addWidget(QLabel("Templates:"))
        self.nuclei_templates = QLineEdit()
        self.nuclei_templates.setPlaceholderText("e.g. cves,vulnerabilities (leave empty for default)")
        template_layout.addWidget(self.nuclei_templates)
        self.options_layout.addLayout(template_layout)

        sev_layout = QHBoxLayout()
        sev_layout.addWidget(QLabel("Severity:"))
        self.nuclei_severity = QComboBox()
        self.nuclei_severity.addItems(["all", "critical,high", "medium", "low", "info"])
        sev_layout.addWidget(self.nuclei_severity)
        self.options_layout.addLayout(sev_layout)

    def create_ffuf_options(self) -> None:
        ext_layout = QHBoxLayout()
        ext_layout.addWidget(QLabel("Extensions:"))
        self.ffuf_extensions = QLineEdit("php,html,txt,json")
        ext_layout.addWidget(self.ffuf_extensions)
        self.options_layout.addLayout(ext_layout)

    def build_options(self, tool: str) -> Dict[str, Any]:
        if tool == 'sqlmap':
            return {
                'risk': self.sqlmap_risk.value(),
                'level': self.sqlmap_level.value(),
                'enumerate_dbs': self.sqlmap_enumerate_dbs.isChecked()
            }
        elif tool == 'dirsearch':
            return {
                'extensions': self.dirsearch_extensions.text(),
                'threads': self.dirsearch_threads.value()
            }
        elif tool == 'nuclei':
            severity = self.nuclei_severity.currentText()
            opts = {}
            if severity != "all":
                opts["severity"] = severity
            if self.nuclei_templates.text().strip():
                opts["templates"] = self.nuclei_templates.text().strip()
            return opts
        elif tool == 'ffuf':
            return {
                'extensions': self.ffuf_extensions.text()
            }
        else: # nikto
            return {
                'port': self.nikto_port.value(),
                'ssl': self.nikto_ssl.isChecked()
            }

    def start_scan(self) -> None:
        target = self.target_input.text().strip()
        if not target:
            QMessageBox.warning(self, "Input Error", "Please enter a target URL/Host!")
            return

        tool = self.tool_combo.currentText().lower()
        options: Dict[str, Any] = self.build_options(tool)

        self.web_terminal.clear()
        self.append_terminal(f"[{tool}] Starting scan on {target}...")
        self.progress.show()

        if self.scan_thread and self.scan_thread.isRunning():
            self.scan_thread.stop()

        self.scan_thread = ScanThread(self.controller, tool, target, options)
        self.scan_thread.output.connect(self.append_terminal)
        self.scan_thread.finished.connect(self.on_scan_finished)
        self.scan_thread.start()

    def stop_scan(self) -> None:
        if self.scan_thread and self.scan_thread.isRunning():
            self.scan_thread.stop()
            self.append_terminal("[web] Scan stopped by user.")
            self.progress.hide()

    def on_scan_finished(self, scan_id: str, result: Dict[str, Any]) -> None:
        self.progress.hide()
        self.append_terminal(f"[web] Scan finished: {scan_id}")

        tool = self.tool_combo.currentText().lower()
        target = self.target_input.text().strip()

        if result.get('error'):
            self.append_terminal(f"[ERROR] {result['error']}")
            self.log_terminal(f"[Web] {tool} failed on {target}: {result['error']}")
        else:
            output = result.get('output', '')
            if output:
                self.append_terminal(output)
            else:
                self.append_terminal(str(result))
            self.log_terminal(f"[Web] {tool} completed on {target}")

    def append_terminal(self, message: str) -> None:
        self.web_terminal.append(message)
        self.web_terminal.moveCursor(QTextCursor.MoveOperation.End)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Clean up threads on window close"""
        if self.scan_thread and self.scan_thread.isRunning():
            self.scan_thread.stop()
        event.accept()

    def log_terminal(self, message: str) -> None:
        """Send tool output to the shared dashboard terminal"""
        window: Optional[QObject] = self.window()
        if window and hasattr(window, 'append_terminal'):
            getattr(window, 'append_terminal')(message)