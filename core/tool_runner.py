"""
Tool Runner for CyberSuite
Executes penetration testing tools via subprocess
"""
import os
import importlib.util
import subprocess
import shutil
import sys
from typing import Any, Dict, Optional

ToolOptions = Dict[str, Any]
ToolResult = Dict[str, Any]

class ToolRunner:
    def __init__(self):
        self.running_processes: Dict[str, subprocess.Popen[str]] = {}
        
        # Ensure ~/.local/bin is in PATH for newly installed tools
        local_bin = os.path.expanduser("~/.local/bin")
        if local_bin not in os.environ.get("PATH", ""):
            os.environ["PATH"] = os.environ.get("PATH", "") + os.pathsep + local_bin

        
    def check_tool_installed(self, tool_name: str) -> bool:
        """Check if a tool is installed and available in PATH"""
        # Map tool names to their executable names
        tool_executables = {
            'nmap': 'nmap',
            'amass': 'subfinder',
            'subfinder': 'subfinder',
            'whatweb': 'whatweb',
            'sqlmap': 'sqlmap',
            'dirsearch': 'dirsearch',
            'nikto': 'nikto',
            'hydra': 'hydra',
            'aircrack-ng': 'aircrack-ng',
            'msfconsole': 'msfconsole',
            'nuclei': 'nuclei',
            'ffuf': 'ffuf',
            'searchsploit': 'searchsploit'
        }

        executable = tool_executables.get(tool_name, tool_name)
        if shutil.which(executable) is not None:
            return True

        if tool_name == 'sqlmap':
            return self._is_python_module_installed('sqlmap')
        if tool_name == 'dirsearch':
            return (
                self._is_python_module_installed('dirsearch') or
                self._is_python_module_installed('dirsearch.dirsearch')
            )
        if tool_name == 'whatweb':
            return shutil.which('whatweb') is not None

        return False

    def _is_python_module_installed(self, module_name: str) -> bool:
        try:
            return importlib.util.find_spec(module_name) is not None
        except (ModuleNotFoundError, Exception):
            return False
    
    def run_tool(self, tool_name: str, target: str, options: ToolOptions) -> ToolResult:
        """Run a penetration testing tool"""
        if not self.check_tool_installed(tool_name):
            return {
                'success': False,
                'error': f'{tool_name} is not installed or not in PATH',
                'output': ''
            }
        
        # Route to specific tool handler
        handlers = {
            'nmap': self._run_nmap,
            'amass': self._run_subfinder,
            'subfinder': self._run_subfinder,
            'whatweb': self._run_whatweb,
            'sqlmap': self._run_sqlmap,
            'dirsearch': self._run_dirsearch,
            'nikto': self._run_nikto,
            'hydra': self._run_hydra,
            'aircrack-ng': self._run_aircrack,
            'msfconsole': self._run_metasploit,
            'nuclei': self._run_nuclei,
            'ffuf': self._run_ffuf,
            'searchsploit': self._run_searchsploit
        }
        
        handler = handlers.get(tool_name)
        if handler:
            return handler(target, options)
        else:
            return {
                'success': False,
                'error': f'No handler for tool: {tool_name}',
                'output': ''
            }
    
    def _run_command(self, command: list[str], timeout: int = 300, options: Optional[ToolOptions] = None) -> ToolResult:
        """Execute a command and return the result"""
        process: Optional[subprocess.Popen[str]] = None
        scan_id = options.get('__scan_id') if options else None
        output_callback = options.get('__output_callback') if options else None
        
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                shell=False,
                bufsize=1
            )
            
            if scan_id:
                self.running_processes[scan_id] = process
            
            import re
            
            output_lines = []
            if process.stdout:
                for line in iter(process.stdout.readline, ''):
                    if not line:
                        break
                    
                    # Store original line for internal representation
                    output_lines.append(line)
                    
                    if output_callback:
                        # Split by carriage returns since progress bars use them
                        chunks = line.split('\r')
                        for chunk in chunks:
                            # Strip ANSI codes completely
                            clean_chunk = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', chunk)
                            
                            # Strip dirsearch progress bars: "[### ] 40% 41/1000 8/s job:1/1 errors:0"
                            clean_chunk = re.sub(r'\[[\s#]*\]\s+\d+%\s+\d+/\d+\s+(?:\d+/s|\d+.\d+/s|\d+M/s|\d+K/s|\d+\s*/s|[\d\.]+(?:[kKmM])?(?:B|/s)?)\s+job:\d+/\d+\s+errors:\d+', '', clean_chunk)
                            
                            # Only callback if the line contains actual non-whitespace output
                            if clean_chunk.strip():
                                output_callback(clean_chunk.rstrip('\n'))
            
            process.wait(timeout=timeout)
            
            if scan_id and scan_id in self.running_processes:
                del self.running_processes[scan_id]
                
            stdout_data = "".join(output_lines)
            return {
                'success': process.returncode == 0,
                'output': stdout_data,
                'error': stdout_data if process.returncode != 0 else '',
                'return_code': process.returncode
            }
            
        except subprocess.TimeoutExpired:
            if process is not None:
                process.kill()
            if scan_id and scan_id in self.running_processes:
                del self.running_processes[scan_id]
            return {
                'success': False,
                'output': '',
                'error': f'Command timed out after {timeout} seconds'
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e)
            }
    
    def _run_nmap(self, target: str, options: ToolOptions) -> ToolResult:
        """Run Nmap scan"""
        command = ['nmap']
        
        # Add scan type
        scan_type = options.get('scan_type', 'quick')
        if scan_type == 'quick':
            command.append('-F')
        elif scan_type == 'full':
            command.append('-p-')
        elif scan_type == 'stealth':
            command.extend(['-sS', '-T2'])
        
        # Add service detection
        if options.get('service_detection', False):
            command.append('-sV')
        
        # Add OS detection
        if options.get('os_detection', False):
            command.append('-O')
        
        # Add script scanning
        if options.get('script_scan', False):
            command.append('-sC')
        
        # Add output format
        if options.get('output_file'):
            command.extend(['-oN', options['output_file']])
        
        command.append(target)
        
        return self._run_command(command, timeout=600, options=options)
    
    def _run_subfinder(self, target: str, options: ToolOptions) -> ToolResult:
        """Run Subfinder subdomain enumeration"""
        command = ['subfinder', '-d', target]

        if options.get('all_sources', False):
            command.append('-all')

        if options.get('silent', False):
            command.append('-silent')

        # Preserve legacy amass-style options if provided
        if options.get('passive', False):
            command.append('-silent')
        if options.get('brute', False):
            command.append('-all')

        return self._run_command(command, timeout=900, options=options)
    
    def _run_whatweb(self, target: str, options: ToolOptions) -> ToolResult:
        """Run WhatWeb scanner"""
        command = ['whatweb', '--no-errors', target]
        
        # Verbosity
        verbosity = options.get('verbosity', 1)
        command.extend(['-v'] if verbosity > 1 else [])
        
        # Aggression level
        aggression = options.get('aggression', 1)
        command.extend(['-a', str(aggression)])
        
        return self._run_command(command, timeout=600, options=options)
    
    def _run_sqlmap(self, target: str, options: ToolOptions) -> ToolResult:
        """Run SQLMap"""
        command = ['sqlmap', '-u', target]

        if shutil.which('sqlmap') is None and self._is_python_module_installed('sqlmap'):
            command = [sys.executable, '-m', 'sqlmap', '-u', target]

        # Batch mode (non-interactive)
        command.append('--batch')

        # Risk level
        risk = options.get('risk', 1)
        command.extend(['--risk', str(risk)])

        # Level
        level = options.get('level', 1)
        command.extend(['--level', str(level)])

        # Database enumeration
        if options.get('enumerate_dbs', False):
            command.append('--dbs')

        return self._run_command(command, timeout=900, options=options)
    
    def _run_dirsearch(self, target: str, options: ToolOptions) -> ToolResult:
        """Run Dirsearch"""
        command = ['dirsearch', '-u', target]

        # Extensions
        extensions = options.get('extensions', 'php,html,js')
        command.extend(['-e', extensions])
        
        # Wordlist
        if options.get('wordlist'):
            command.extend(['-w', options['wordlist']])
        
        # Threads
        threads = options.get('threads', 10)
        command.extend(['-t', str(threads)])

        result = self._run_command(command, timeout=600, options=options)
        if result.get('success'):
            return result

        error_output = str(result.get('error', ''))
        can_use_module = (
            self._is_python_module_installed('dirsearch') or
            self._is_python_module_installed('dirsearch.dirsearch')
        )

        # Newer Python environments may have a broken `dirsearch` console script
        # if setuptools/pkg_resources is missing. Fall back to the module entrypoint.
        if can_use_module and "No module named 'pkg_resources'" in error_output:
            module_command = [sys.executable, '-m', 'dirsearch.dirsearch', '-u', target]
            module_command.extend(['-e', extensions, '-t', str(threads)])

            if options.get('wordlist'):
                module_command.extend(['-w', options['wordlist']])

            fallback_result = self._run_command(module_command, timeout=600, options=options)
            if fallback_result.get('success'):
                return fallback_result

            fallback_error = str(fallback_result.get('error', ''))
            if "No module named 'pkg_resources'" in fallback_error:
                fallback_result['error'] = (
                    "dirsearch requires setuptools/pkg_resources in the active Python "
                    "environment. Install it with: pip install setuptools\n\n"
                    f"{fallback_error}"
                )
            return fallback_result

        if "No module named 'pkg_resources'" in error_output:
            result['error'] = (
                "dirsearch requires setuptools/pkg_resources in the active Python "
                "environment. Install it with: pip install setuptools\n\n"
                f"{error_output}"
            )

        return result
    
    def _run_nikto(self, target: str, options: ToolOptions) -> ToolResult:
        """Run Nikto web scanner"""
        is_ssl = options.get('ssl', False)
        port = options.get('port', 80)
        
        # Clean target and adjust port/ssl if full URI is provided
        if target.startswith('https://'):
            target = target[8:].split('/')[0]  # Get just the host, strip path
            is_ssl = True
            if port == 80:
                port = 443
        elif target.startswith('http://'):
            target = target[7:].split('/')[0]
            if port == 443: # if it was mistakenly set
                port = 80
        
        # Add port 443 if SSL is checked but port is left as default 80
        if is_ssl and port == 80:
            port = 443

        command = ['nikto', '-h', target]
        
        if is_ssl:
            command.append('-ssl')
            
        command.extend(['-p', str(port)])
        
        return self._run_command(command, timeout=900, options=options)
    
    def _run_hydra(self, target: str, options: ToolOptions) -> ToolResult:
        """Run Hydra password attack"""
        protocol = options.get('protocol', 'ssh')
        username = options.get('username', 'admin')
        
        command = ['hydra']
        
        # Username
        if options.get('username_list'):
            command.extend(['-L', options['username_list']])
        else:
            command.extend(['-l', username])
        
        # Password
        if options.get('password_list'):
            command.extend(['-P', options['password_list']])
        else:
            return {
                'success': False,
                'error': 'Password list is required',
                'output': ''
            }
        
        # Threads
        threads = options.get('threads', 4)
        command.extend(['-t', str(threads)])
        
        # Target and protocol
        command.extend([target, protocol])
        
        return self._run_command(command, timeout=1800, options=options)
    
    def _run_aircrack(self, target: str, options: ToolOptions) -> ToolResult:
        """Run Aircrack-ng"""
        # This is a simplified version - actual WiFi attacks require more setup
        command = ['aircrack-ng']
        
        if options.get('capture_file'):
            command.append(options['capture_file'])
        
        if options.get('wordlist'):
            command.extend(['-w', options['wordlist']])
        
        return self._run_command(command, timeout=1800, options=options)
    
    def _run_metasploit(self, target: str, options: ToolOptions) -> ToolResult:
        """Run Metasploit Framework"""
        # This is a simplified version - actual Metasploit usage is more complex
        exploit = options.get('exploit', '')
        
        if not exploit:
            return {
                'success': False,
                'error': 'Exploit module is required',
                'output': ''
            }
        
        # Create resource file for automated execution
        resource_content = f"""
use {exploit}
set RHOSTS {target}
set LHOST {options.get('lhost', '127.0.0.1')}
set LPORT {options.get('lport', '4444')}
exploit
"""
        
        resource_file = '/tmp/msf_resource.rc'
        with open(resource_file, 'w') as f:
            f.write(resource_content)
        
        command = ['msfconsole', '-q', '-r', resource_file]
        
        return self._run_command(command, timeout=1800, options=options)
        
    def _run_nuclei(self, target: str, options: ToolOptions) -> ToolResult:
        """Run Nuclei vulnerability scanner"""
        command = ['nuclei', '-target', target, '-no-color']
        
        if options.get('templates'):
            command.extend(['-t', options['templates']])
        
        if options.get('severity'):
            command.extend(['-severity', options['severity']])
            
        return self._run_command(command, timeout=1200, options=options)

    def _run_ffuf(self, target: str, options: ToolOptions) -> ToolResult:
        """Run ffuf directory fuzzer"""
        command = ['ffuf', '-u', f'{target}/FUZZ']
        
        wordlist = options.get('wordlist', '/usr/share/wordlists/dirb/common.txt')
        command.extend(['-w', wordlist])
        
        if options.get('extensions'):
            command.extend(['-e', options['extensions']])
            
        return self._run_command(command, timeout=900, options=options)

    def _run_searchsploit(self, target: str, options: ToolOptions) -> ToolResult:
        """Run searchsploit"""
        # Searchsploit target is a query string, e.g. "wordpress 5.8"
        command = ['searchsploit', target]
        return self._run_command(command, timeout=60, options=options)
    
    def stop_tool(self, scan_id: str):
        """Stop a running tool"""
        if scan_id in self.running_processes:
            process = self.running_processes[scan_id]
            process.terminate()
            del self.running_processes[scan_id]
