"""
Reconnaissance Tab for CyberSuite
Nmap, Subfinder, and WhatWeb with live terminal output
"""
from typing import Any, Dict, Optional
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLayout, QLabel,
                               QLineEdit, QPushButton, QTextEdit, QComboBox,
                               QGroupBox, QCheckBox, QProgressBar, QMessageBox)
from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtGui import QCloseEvent, QFont, QTextCursor


class ScanThread(QObject):
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

        if hasattr(self.controller, 'start_scan'):
            self.scan_id = self.controller.start_scan(self.tool, self.target, self.options, callback, stream_cb)

    def isRunning(self) -> bool:
        return self._is_running

    def stop(self) -> None:
        self._is_running = False
        if self.scan_id and hasattr(self.controller, 'stop_scan'):
            self.controller.stop_scan(self.scan_id)


class ReconTab(QWidget):
    def __init__(self, controller: Any):
        super().__init__()
        self.controller = controller
        self.scan_thread: Optional[ScanThread] = None
        self.init_ui()

    def init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)

        title = QLabel("🔍 Reconnaissance Module")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        target_group = QGroupBox("Target Configuration")
        target_layout = QHBoxLayout(target_group)
        target_layout.addWidget(QLabel("Target (IP/Domain/Network):"))
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("e.g., 192.168.1.1 or example.com or 192.168.1.0/24")
        target_layout.addWidget(self.target_input)
        layout.addWidget(target_group)

        tool_group = QGroupBox("Tool Selection")
        tool_layout = QHBoxLayout(tool_group)
        tool_layout.addWidget(QLabel("Scan Tool:"))
        self.tool_tabs = QComboBox()
        self.tool_tabs.addItems(["Nmap", "Subfinder", "WhatWeb"])
        self.tool_tabs.currentIndexChanged.connect(self.on_tool_changed)
        tool_layout.addWidget(self.tool_tabs)
        layout.addWidget(tool_group)

        self.options_group = QGroupBox("Scan Options")
        self.options_layout = QVBoxLayout(self.options_group)
        layout.addWidget(self.options_group)

        self.create_nmap_options()

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
        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setFont(QFont("Consolas", 10))
        self.terminal_output.setStyleSheet(
            "QTextEdit { background-color: #0d1117; color: #c9d1d9; border: 1px solid #30363d; padding: 8px; }"
        )
        self.terminal_output.setPlaceholderText("Live terminal output will appear here...")
        terminal_layout.addWidget(self.terminal_output)
        layout.addWidget(terminal_group)

        self.log_terminal("Reconnaissance live terminal ready.")

    def on_tool_changed(self, index: int) -> None:
        self.clear_layout(self.options_layout)

        tool = self.tool_tabs.currentText().lower()
        if tool == 'nmap':
            self.create_nmap_options()
        elif tool == 'subfinder':
            self.create_subfinder_options()
        else:
            self.create_whatweb_options()

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
                # Spacer items are removed automatically when layout is cleared.
                continue

    def create_nmap_options(self) -> None:
        scan_type_layout = QHBoxLayout()
        scan_type_layout.addWidget(QLabel("Scan Type:"))
        self.nmap_scan_type = QComboBox()
        self.nmap_scan_type.addItems(["Quick Scan (-F)", "Full Scan (-p-)", "Stealth Scan (-sS)"])
        scan_type_layout.addWidget(self.nmap_scan_type)
        self.options_layout.addLayout(scan_type_layout)

        self.nmap_service = QCheckBox("Service Version Detection (-sV)")
        self.nmap_os = QCheckBox("OS Detection (-O)")
        self.nmap_script = QCheckBox("Script Scan (-sC)")
        self.options_layout.addWidget(self.nmap_service)
        self.options_layout.addWidget(self.nmap_os)
        self.options_layout.addWidget(self.nmap_script)

    def create_subfinder_options(self) -> None:
        self.subfinder_all = QCheckBox("Use all sources (-all)")
        self.subfinder_silent = QCheckBox("Silent mode (-silent)")
        self.options_layout.addWidget(self.subfinder_all)
        self.options_layout.addWidget(self.subfinder_silent)

    def create_whatweb_options(self) -> None:
        aggression_layout = QHBoxLayout()
        aggression_layout.addWidget(QLabel("Aggression Level:"))
        self.whatweb_aggression = QComboBox()
        self.whatweb_aggression.addItems(["1 (Stealthy)", "3 (Aggressive)", "4 (Heavy)"])
        self.whatweb_aggression.setCurrentText("1 (Stealthy)")
        aggression_layout.addWidget(self.whatweb_aggression)
        self.options_layout.addLayout(aggression_layout)

        verbosity_layout = QHBoxLayout()
        verbosity_layout.addWidget(QLabel("Verbosity:"))
        self.whatweb_verbosity = QComboBox()
        self.whatweb_verbosity.addItems(["Normal", "Verbose (-v)"])
        self.whatweb_verbosity.setCurrentText("Normal")
        verbosity_layout.addWidget(self.whatweb_verbosity)
        self.options_layout.addLayout(verbosity_layout)

    def start_scan(self) -> None:
        target = self.target_input.text().strip()
        if not target:
            QMessageBox.warning(self, "Input Error", "Please enter a target for reconnaissance.")
            return

        tool = self.tool_tabs.currentText().lower()
        options: Dict[str, Any] = self.build_options(tool)

        self.terminal_output.clear()
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
            self.append_terminal("[recon] Scan stopped by user.")
            self.progress.hide()

    def build_options(self, tool: str) -> Dict[str, Any]:
        if tool == 'nmap':
            return {
                'scan_type': 'quick' if self.nmap_scan_type.currentIndex() == 0 else 'full' if self.nmap_scan_type.currentIndex() == 1 else 'stealth',
                'service_detection': self.nmap_service.isChecked(),
                'os_detection': self.nmap_os.isChecked(),
                'script_scan': self.nmap_script.isChecked()
            }

        if tool == 'subfinder':
            return {
                'all_sources': self.subfinder_all.isChecked(),
                'silent': self.subfinder_silent.isChecked()
            }

        verbosity_text = self.whatweb_verbosity.currentText()
        verbosity = 2 if verbosity_text == "Verbose (-v)" else 1
        
        agg_val = 1
        if "3" in self.whatweb_aggression.currentText(): agg_val = 3
        elif "4" in self.whatweb_aggression.currentText(): agg_val = 4
        
        return {
            'verbosity': verbosity,
            'aggression': agg_val
        }

    def on_scan_finished(self, scan_id: str, result: Dict[str, Any]) -> None:
        self.progress.hide()
        self.append_terminal(f"[recon] Scan finished: {scan_id}")

        if result.get('error'):
            self.append_terminal(f"[ERROR] {result['error']}")
        else:
            output = result.get('output', '')
            if output:
                self.append_terminal(output)
            else:
                self.append_terminal(str(result))

        self.log_terminal(f"[Recon] Scan {scan_id} completed.")

    def append_terminal(self, message: str) -> None:
        if '\x1b[' in message:
            import re, html
            escaped = html.escape(message)
            ansi_colors = {
                '30': 'black', '31': '#ff5555', '32': '#50fa7b', '33': '#f1fa8c',
                '34': '#8be9fd', '35': '#ff79c6', '36': '#8be9fd', '37': '#f8f8f2',
                '90': 'gray', '91': '#ff5555', '92': '#50fa7b', '93': '#f1fa8c',
                '94': '#8be9fd', '95': '#ff79c6', '96': '#8be9fd', '97': '#ffffff'
            }
            ansi_escape = re.compile(r'\x1b\[([0-9;]+)m')
            res = ""
            last_end = 0
            span_open = False
            bold_open = False
            
            for match in ansi_escape.finditer(escaped):
                res += escaped[last_end:match.start()]
                last_end = match.end()
                for code in match.group(1).split(';'):
                    if code == '0':
                        if span_open: res += "</span>"; span_open = False
                        if bold_open: res += "</b>"; bold_open = False
                    elif code == '1':
                        if not bold_open: res += "<b>"; bold_open = True
                    elif code == '22':
                        if bold_open: res += "</b>"; bold_open = False
                    elif code in ansi_colors:
                        if span_open: res += "</span>"
                        res += f'<span style="color: {ansi_colors[code]}">'
                        span_open = True
            res += escaped[last_end:]
            if span_open: res += "</span>"
            if bold_open: res += "</b>"
            self.terminal_output.append(res.replace('\n', '<br>'))
        else:
            self.terminal_output.append(message)
            
        self.terminal_output.moveCursor(QTextCursor.MoveOperation.End)

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.scan_thread and self.scan_thread.isRunning():
            self.scan_thread.stop()
        event.accept()

    def log_terminal(self, message: str) -> None:
        window = self.window()
        if window and hasattr(window, 'append_terminal'):
            getattr(window, 'append_terminal')(message)