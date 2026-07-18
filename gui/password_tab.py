"""
Password Attack Tab for CyberSuite
Hydra password cracking
"""
from typing import Any, Dict, Optional
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QTextEdit, QComboBox,
                               QGroupBox, QFileDialog, QSpinBox, QProgressBar,
                               QRadioButton, QButtonGroup, QMessageBox)
from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtGui import QCloseEvent, QTextCursor

class ScanThread(QObject):
    finished = Signal(str, dict)
    output = Signal(str)
    
    def __init__(self, controller: Any, target: str, options: Dict[str, Any]):
        super().__init__()
        self.controller = controller
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
        
        # Ensure the controller has the start_scan method before calling
        if hasattr(self.controller, 'start_scan'):
            self.scan_id = self.controller.start_scan('hydra', self.target, self.options, callback, stream_cb)

    def isRunning(self) -> bool:
        return self._is_running
        
    def stop(self) -> None:
        self._is_running = False
        if self.scan_id and hasattr(self.controller, 'stop_scan'):
            self.controller.stop_scan(self.scan_id)

class PasswordTab(QWidget):
    def __init__(self, controller: Any):
        super().__init__()
        self.controller = controller
        self.scan_thread: Optional[ScanThread] = None
        self.init_ui()
        
    def init_ui(self) -> None:
        """Initialize the password attack UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("🔐 Password Attack Module")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        # Target configuration
        target_group = QGroupBox("Target Configuration")
        target_layout = QVBoxLayout()
        
        # Target IP/Host
        target_ip_layout = QHBoxLayout()
        target_ip_layout.addWidget(QLabel("Target IP/Host:"))
        self.target_ip = QLineEdit()
        self.target_ip.setPlaceholderText("e.g., 192.168.1.1 or example.com")
        target_ip_layout.addWidget(self.target_ip)
        target_layout.addLayout(target_ip_layout)
        
        # Protocol
        protocol_layout = QHBoxLayout()
        protocol_layout.addWidget(QLabel("Protocol:"))
        self.protocol = QComboBox()
        self.protocol.addItems(["ssh", "ftp", "telnet", "http-get", "http-post", "mysql", "rdp", "smb"])
        protocol_layout.addWidget(self.protocol)
        target_layout.addLayout(protocol_layout)
        
        target_group.setLayout(target_layout)
        layout.addWidget(target_group)
        
        # Credentials configuration
        creds_group = QGroupBox("Credentials Configuration")
        creds_layout = QVBoxLayout()
        
        # Username mode
        username_mode_layout = QHBoxLayout()
        self.username_single_radio = QRadioButton("Single Username")
        self.username_list_radio = QRadioButton("Username List")
        self.username_single_radio.setChecked(True)
        
        username_mode_group = QButtonGroup(self)
        username_mode_group.addButton(self.username_single_radio)
        username_mode_group.addButton(self.username_list_radio)
        
        username_mode_layout.addWidget(self.username_single_radio)
        username_mode_layout.addWidget(self.username_list_radio)
        creds_layout.addLayout(username_mode_layout)
        
        # Username input
        username_layout = QHBoxLayout()
        username_layout.addWidget(QLabel("Username:"))
        self.username = QLineEdit()
        self.username.setPlaceholderText("e.g., admin")
        username_layout.addWidget(self.username)
        
        self.username_list_btn = QPushButton("Browse List")
        self.username_list_btn.setEnabled(False)
        self.username_list_btn.clicked.connect(self.browse_username_list)
        username_layout.addWidget(self.username_list_btn)
        creds_layout.addLayout(username_layout)
        
        # Password list
        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("Password List:"))
        self.password_list = QLineEdit()
        self.password_list.setPlaceholderText("Select password wordlist...")
        password_btn = QPushButton("Browse")
        password_btn.clicked.connect(self.browse_password_list)
        password_layout.addWidget(self.password_list)
        password_layout.addWidget(password_btn)
        creds_layout.addLayout(password_layout)
        
        creds_group.setLayout(creds_layout)
        layout.addWidget(creds_group)
        
        # Connect radio buttons
        self.username_single_radio.toggled.connect(self.on_username_mode_changed)
        
        # Attack options
        options_group = QGroupBox("Attack Options")
        options_layout = QVBoxLayout()
        
        threads_layout = QHBoxLayout()
        threads_layout.addWidget(QLabel("Threads:"))
        self.threads = QSpinBox()
        self.threads.setRange(1, 64)
        self.threads.setValue(4)
        threads_layout.addWidget(self.threads)
        threads_layout.addStretch()
        options_layout.addLayout(threads_layout)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start Attack")
        self.start_btn.setObjectName("dangerButton")
        self.start_btn.clicked.connect(self.start_attack)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Stop Attack")
        self.stop_btn.setObjectName("dangerButton")
        self.stop_btn.clicked.connect(self.stop_attack)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Progress
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.hide()
        layout.addWidget(self.progress)
        
        # Results
        results_group = QGroupBox("Attack Results")
        results_layout = QVBoxLayout()
        
        self.results = QTextEdit()
        self.results.setReadOnly(True)
        self.results.setPlaceholderText("Attack results will appear here...")
        
        results_layout.addWidget(self.results)
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        # Warning
        warning_label = QLabel(
            "<b>⚠️ WARNING:</b> Password attacks should only be performed on systems you own "
            "or have explicit written permission to test. Unauthorized access is illegal."
        )
        warning_label.setWordWrap(True)
        warning_label.setStyleSheet("color: #f38ba8; font-weight: bold;")
        layout.addWidget(warning_label)
        
    def on_username_mode_changed(self) -> None:
        """Handle username mode change"""
        if self.username_single_radio.isChecked():
            self.username.setEnabled(True)
            self.username_list_btn.setEnabled(False)
            self.username.setPlaceholderText("e.g., admin")
        else:
            self.username.setEnabled(False)
            self.username_list_btn.setEnabled(True)
            self.username.setPlaceholderText("Username list file selected")
    
    def browse_username_list(self) -> None:
        """Browse for username list"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Username List",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            self.username.setText(file_path)
    
    def browse_password_list(self) -> None:
        """Browse for password list"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Password List",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            self.password_list.setText(file_path)
    
    def start_attack(self) -> None:
        """Start password attack"""
        target = self.target_ip.text().strip()
        password_list = self.password_list.text().strip()
        
        if not target or not password_list:
            QMessageBox.warning(
                self,
                "Input Error",
                "Please enter target and select password list!"
            )
            return
        
        # Confirm attack - Updated to PySide6 enum paths
        reply = QMessageBox.question(
            self,
            "Confirm Attack",
            f"Are you sure you want to start a password attack on {target}?\n\n"
            "Make sure you have authorization to test this system.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.No:
            return
        
        options: Dict[str, Any] = {
            'protocol': self.protocol.currentText(),
            'password_list': password_list,
            'threads': self.threads.value()
        }
        
        if self.username_single_radio.isChecked():
            options['username'] = self.username.text().strip()
        else:
            options['username_list'] = self.username.text().strip()
        
        self.progress.show()
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.results.setText("Starting password attack...\n")
        self.log_terminal(f"[Password] Starting Hydra attack on {target} via {options['protocol']}")
        
        # Stop previous thread if running
        if self.scan_thread and self.scan_thread.isRunning():
            self.scan_thread.stop()
        
        self.scan_thread = ScanThread(self.controller, target, options)
        self.scan_thread.output.connect(self.append_results)
        self.scan_thread.finished.connect(self.on_attack_finished)
        self.scan_thread.start()
    
    def on_attack_finished(self, scan_id: str, result: Dict[str, Any]) -> None:
        """Handle attack completion"""
        self.progress.hide()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        if 'error' in result:
            result_text = f"❌ Error: {result['error']}\n"
        else:
            result_text = "✅ Attack completed!\n\n"
            output = result.get('output', str(result))
            result_text += str(output)
        
        self.results.setText(result_text)

        target = self.target_ip.text().strip() or "target"
        if 'error' in result:
            self.log_terminal(f"[Password] Hydra failed on {target}: {result['error']}")
        else:
            self.log_terminal(f"[Password] Hydra completed on {target}")
            raw_output = result.get('output')
            if raw_output:
                for line in str(raw_output).splitlines():
                    if line.strip():
                        self.log_terminal(line)
                        
    def stop_attack(self) -> None:
        """Stop the running password attack"""
        if self.scan_thread and self.scan_thread.isRunning():
            self.scan_thread.stop()
            self.results.append("\n[!] Attack stopped by user.")
            self.log_terminal("[Password] Attack stopped by user")
            self.progress.hide()
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
                        
    def append_results(self, message: str) -> None:
        self.results.append(message)
        self.results.moveCursor(QTextCursor.MoveOperation.End) if hasattr(QTextCursor, 'MoveOperation') else None
    
    def closeEvent(self, event: QCloseEvent) -> None:
        """Clean up threads on close"""
        if self.scan_thread and self.scan_thread.isRunning():
            self.scan_thread.stop()
        event.accept()

    def log_terminal(self, message: str) -> None:
        """Send tool output to the shared dashboard terminal."""
        window: Optional[QObject] = self.window()
        if window and hasattr(window, 'append_terminal'):
            # Use getattr to satisfy Pylance about the dynamic method
            getattr(window, 'append_terminal')(message)