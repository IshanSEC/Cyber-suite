"""
Network Tab for CyberSuite
WiFi and network security testing
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QTextEdit, QComboBox,
                               QGroupBox, QFileDialog, QProgressBar)
from PySide6.QtCore import Qt

class NetworkTab(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.scan_thread = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the network testing UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("📡 Network & WiFi Security")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        # WiFi Testing
        wifi_group = QGroupBox("WiFi Security Testing (Aircrack-ng)")
        wifi_layout = QVBoxLayout()
        
        # Capture file
        capture_layout = QHBoxLayout()
        capture_layout.addWidget(QLabel("Capture File (.cap):"))
        self.capture_file = QLineEdit()
        self.capture_file.setPlaceholderText("Select a .cap file...")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_capture_file)
        capture_layout.addWidget(self.capture_file)
        capture_layout.addWidget(browse_btn)
        wifi_layout.addLayout(capture_layout)
        
        # Wordlist
        wordlist_layout = QHBoxLayout()
        wordlist_layout.addWidget(QLabel("Wordlist:"))
        self.wordlist_file = QLineEdit()
        self.wordlist_file.setPlaceholderText("Select wordlist file...")
        wordlist_btn = QPushButton("Browse")
        wordlist_btn.clicked.connect(self.browse_wordlist)
        wordlist_layout.addWidget(self.wordlist_file)
        wordlist_layout.addWidget(wordlist_btn)
        wifi_layout.addLayout(wordlist_layout)
        
        # Start button
        start_btn = QPushButton("Start WiFi Crack")
        start_btn.setObjectName("successButton")
        start_btn.clicked.connect(self.start_wifi_crack)
        wifi_layout.addWidget(start_btn)
        
        # Progress
        self.wifi_progress = QProgressBar()
        self.wifi_progress.setRange(0, 0)
        self.wifi_progress.hide()
        wifi_layout.addWidget(self.wifi_progress)
        
        # Results
        self.wifi_results = QTextEdit()
        self.wifi_results.setReadOnly(True)
        self.wifi_results.setPlaceholderText("WiFi cracking results will appear here...")
        wifi_layout.addWidget(self.wifi_results)
        
        wifi_group.setLayout(wifi_layout)
        layout.addWidget(wifi_group)
        
        # Info
        info_label = QLabel(
            "<b>⚠️ Important:</b> WiFi security testing requires proper authorization.<br>"
            "Only test networks you own or have explicit permission to test.<br><br>"
            "<b>Note:</b> Aircrack-ng requires a capture file (.cap) containing WPA handshake."
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        layout.addStretch()
        
    def browse_capture_file(self):
        """Browse for capture file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Capture File",
            "",
            "Capture Files (*.cap *.pcap);;All Files (*)"
        )
        if file_path:
            self.capture_file.setText(file_path)
    
    def browse_wordlist(self):
        """Browse for wordlist file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Wordlist",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            self.wordlist_file.setText(file_path)
    
    def start_wifi_crack(self):
        """Start WiFi password cracking"""
        from PySide6.QtWidgets import QMessageBox
        
        capture = self.capture_file.text().strip()
        wordlist = self.wordlist_file.text().strip()
        
        if not capture or not wordlist:
            QMessageBox.warning(
                self,
                "Input Error",
                "Please select both capture file and wordlist!"
            )
            return
        
        options = {
            'capture_file': capture,
            'wordlist': wordlist
        }
        
        self.wifi_progress.show()
        self.wifi_results.setText("Starting WiFi password cracking...\n")
        self.log_terminal(f"[Network] Starting Aircrack-ng against capture {capture}")
        
        from PySide6.QtCore import QThread, Signal, QObject
        
        class ScanThread(QObject):
            finished = Signal(str, dict)
            output = Signal(str)
            
            def __init__(self, controller, target, options):
                super().__init__()
                self.controller = controller
                self.target = target
                self.options = options
                self._is_running = True
                self.scan_id = None
                
            def start(self):
                def callback(scan_id, result):
                    if self._is_running:
                        self.finished.emit(scan_id, result)
                
                def stream_cb(line):
                    if self._is_running:
                        self.output.emit(line)
                
                self.scan_id = self.controller.start_scan('aircrack-ng', self.target, self.options, callback, stream_cb)
                
            def isRunning(self):
                return self._is_running

            def stop(self):
                self._is_running = False
                if hasattr(self, 'scan_id') and self.scan_id and hasattr(self.controller, 'stop_scan'):
                    self.controller.stop_scan(self.scan_id)
        
        # Stop previous thread if running
        if self.scan_thread and self.scan_thread.isRunning():
            self.scan_thread.stop()
        
        self.scan_thread = ScanThread(self.controller, capture, options)
        self.scan_thread.output.connect(self.append_results)
        self.scan_thread.finished.connect(self.on_scan_finished)
        self.scan_thread.start()
    
    def on_scan_finished(self, scan_id, result):
        """Handle scan completion"""
        self.wifi_progress.hide()
        
        if 'error' in result:
            result_text = f"❌ Error: {result['error']}\n"
        else:
            result_text = f"✅ Scan completed!\n\n"
            if 'output' in result:
                result_text += result['output']
            else:
                result_text += str(result)
        
        self.wifi_results.setText(result_text)

        target = self.capture_file.text().strip() or "capture"
        if 'error' in result:
            self.log_terminal(f"[Network] Aircrack-ng failed on {target}: {result['error']}")
        else:
            self.log_terminal(f"[Network] Aircrack-ng completed on {target}")
            output = result.get('output') if isinstance(result, dict) else None
            if output:
                for line in str(output).splitlines():
                    if line.strip():
                        self.log_terminal(line)
                        
    def append_results(self, message):
        self.wifi_results.append(message)
        from PySide6.QtGui import QTextCursor
        self.wifi_results.moveCursor(QTextCursor.MoveOperation.End) if hasattr(QTextCursor, 'MoveOperation') else None
    
    def closeEvent(self, event):
        """Clean up threads on close"""
        if self.scan_thread and self.scan_thread.isRunning():
            self.scan_thread.stop()
        event.accept()

    def log_terminal(self, message):
        """Send tool output to the shared dashboard terminal."""
        window = self.window()
        if hasattr(window, 'append_terminal'):
            window.append_terminal(message)
