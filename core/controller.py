"""
Core Controller for CyberSuite
Manages tool execution, database operations, and scan coordination
"""

import threading
from typing import Any, Callable, Dict, List, Optional

from core.tool_runner import ToolRunner, ToolOptions, ToolResult
from database.db_manager import DatabaseManager
from core.parser import OutputParser


class Controller:
    def __init__(self) -> None:
        self.tool_runner = ToolRunner()
        self.db_manager = DatabaseManager()
        self.active_scans: Dict[str, threading.Thread] = {}
        self.scan_results: Dict[str, Dict[str, Any]] = {}

    def start_scan(
        self,
        tool_name: str,
        target: str,
        options: ToolOptions,
        callback: Optional[Callable[[str, ToolResult], None]] = None,
        output_callback: Optional[Callable[[str], None]] = None
    ) -> str:
        """Start a new scan in a background thread."""
        scan_id = self.db_manager.create_scan(tool_name, target, options)
        options['__scan_id'] = scan_id
        if output_callback:
            options['__output_callback'] = output_callback

        def run_scan() -> None:
            try:
                result = self.tool_runner.run_tool(tool_name, target, options)
                self.scan_results[scan_id] = result

                # Parse and store vulnerabilities
                raw_output = result.get('output', '')
                if raw_output:
                    parsed_data = {}
                    if tool_name == 'nmap':
                        parsed_data = OutputParser.parse_nmap(raw_output)
                    elif tool_name == 'sqlmap':
                        parsed_data = OutputParser.parse_sqlmap(raw_output)
                    elif tool_name == 'nikto':
                        parsed_data = OutputParser.parse_nikto(raw_output)
                    elif tool_name == 'hydra':
                        parsed_data = OutputParser.parse_hydra(raw_output)
                    elif tool_name == 'whatweb':
                        parsed_data = OutputParser.parse_whatweb(raw_output)
                    elif tool_name == 'nuclei':
                        parsed_data = OutputParser.parse_nuclei(raw_output)
                    elif tool_name == 'ffuf':
                        parsed_data = OutputParser.parse_ffuf(raw_output)
                    elif tool_name == 'searchsploit':
                        parsed_data = OutputParser.parse_searchsploit(raw_output)
                    elif tool_name == 'dirsearch':
                        parsed_data = OutputParser.parse_dirsearch(raw_output)
                    else:
                        parsed_data = OutputParser.parse_generic(raw_output)
                        
                    vulns = OutputParser.extract_vulnerabilities(parsed_data, tool_name)
                    for v in vulns:
                        self.db_manager.add_vulnerability(
                            scan_id=scan_id,
                            severity=v['severity'],
                            title=v['title'],
                            description=v['description'],
                            recommendation=v['recommendation']
                        )

                status = 'completed' if result.get('success', False) else 'failed'
                self.db_manager.update_scan_result(scan_id, result, status)

                if callback:
                    callback(scan_id, result)
            except Exception as exc:
                error_result: Dict[str, Any] = {
                    'success': False,
                    'error': str(exc),
                }
                self.scan_results[scan_id] = error_result
                self.db_manager.update_scan_result(scan_id, error_result, 'failed')

                if callback:
                    callback(scan_id, error_result)
            finally:
                self.active_scans.pop(scan_id, None)

        thread = threading.Thread(target=run_scan, daemon=True)
        self.active_scans[scan_id] = thread
        thread.start()

        return scan_id

    def start_full_pentest(
        self,
        target: str,
        callback: Optional[Callable[[str, ToolResult], None]] = None,
        stream_cb: Optional[Callable[[str], None]] = None
    ) -> str:
        """Start an orchestrated full pentest sequence."""
        # Create a unified scan ID for the entire pentest
        scan_id = self.db_manager.create_scan('Full Pentest Pipeline', target, {})
        
        def run_pentest() -> None:
            tools_chain = [
                ('amass', {}),
                ('nmap', {'scan_type': 'quick', 'port_range': '1-1000'}),
                ('whatweb', {'verbosity': 1}),
                ('nuclei', {'severity': 'critical,high'})
            ]
            
            overall_result: Dict[str, Any] = {'success': True, 'output': 'Full Pentest Log:\n\n'}
            
            for tool_name, options in tools_chain:
                options['__scan_id'] = scan_id
                if stream_cb:
                    stream_cb(f"\n[{tool_name.upper()}] Starting automated step...")
                    options['__output_callback'] = stream_cb
                
                try:
                    result = self.tool_runner.run_tool(tool_name, target, options)
                    raw_output = result.get('output', '')
                    
                    if raw_output:
                        overall_result['output'] += f"\n--- {tool_name.upper()} ---\n{raw_output}\n"
                        
                        # Parse and store vulnerabilities
                        parse_func = getattr(OutputParser, f"parse_{tool_name}", OutputParser.parse_generic)
                        parsed_data = parse_func(raw_output)
                        vulns = OutputParser.extract_vulnerabilities(parsed_data, tool_name)
                        for v in vulns:
                            self.db_manager.add_vulnerability(
                                scan_id=scan_id,
                                severity=v['severity'],
                                title=v['title'],
                                description=v['description'],
                                recommendation=v['recommendation']
                            )
                except Exception as e:
                    if stream_cb: stream_cb(f"[{tool_name.upper()}] Error: {e}")
                    overall_result['output'] += f"\n[ERROR] {tool_name} failed: {e}\n"
                    
            status = 'completed' if overall_result['success'] else 'failed'
            self.db_manager.update_scan_result(scan_id, overall_result, status)

            if callback:
                callback(scan_id, overall_result)
            
            self.active_scans.pop(scan_id, None)

        thread = threading.Thread(target=run_pentest, daemon=True)
        self.active_scans[scan_id] = thread
        thread.start()

        return scan_id

    def stop_scan(self, scan_id: str) -> None:
        """Attempt to stop a running scan."""
        if scan_id in self.active_scans:
            self.tool_runner.stop_tool(scan_id)

    def get_scan_result(self, scan_id: str) -> Optional[Dict[str, Any]]:
        """Get cached scan result."""
        return self.scan_results.get(scan_id)

    def get_active_scans_count(self) -> int:
        return len(self.active_scans)

    def get_scan_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self.db_manager.get_scan_history(limit)

    def get_vulnerabilities(self, scan_id: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.db_manager.get_vulnerabilities(scan_id)

    def clear_database(self) -> None:
        self.db_manager.clear_all()

    def check_tool_installed(self, tool_name: str) -> bool:
        return self.tool_runner.check_tool_installed(tool_name)

    def get_all_tools_status(self) -> Dict[str, bool]:
        tools = [
            'nmap', 'subfinder', 'whatweb', 'sqlmap',
            'dirsearch', 'nikto', 'hydra', 'aircrack-ng', 'msfconsole'
        ]
        return {tool: self.check_tool_installed(tool) for tool in tools}
