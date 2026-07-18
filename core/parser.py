"""
Output Parser for CyberSuite
Parses tool outputs and extracts structured information
"""
import re
from typing import Any, cast, Dict, List

class OutputParser:
    @staticmethod
    def parse_nmap(output: str) -> Dict[str, Any]:
        """Parse Nmap output"""
        result: Dict[str, Any] = {
            'open_ports': [],
            'services': [],
            'os_info': '',
            'hosts_up': 0
        }
        
        # Parse open ports
        port_pattern = r'(\d+)/(\w+)\s+open\s+(\S+)'
        for match in re.finditer(port_pattern, output):
            port, protocol, service = match.groups()
            result['open_ports'].append({
                'port': port,
                'protocol': protocol,
                'service': service
            })
        
        # Parse OS detection
        os_pattern = r'OS details: (.+)'
        os_match = re.search(os_pattern, output)
        if os_match:
            result['os_info'] = os_match.group(1)
        
        # Parse hosts up
        hosts_pattern = r'(\d+) host[s]? up'
        hosts_match = re.search(hosts_pattern, output)
        if hosts_match:
            result['hosts_up'] = int(hosts_match.group(1))
        
        return result
    
    @staticmethod
    def parse_amass(output: str) -> Dict[str, Any]:
        """Parse Amass output (legacy support)"""
        subdomains: List[str] = []
        for line in output.split('\n'):
            line = line.strip()
            if line and not line.startswith('['):
                subdomains.append(line)
        
        return {
            'subdomains': subdomains,
            'count': len(subdomains)
        }

    @staticmethod
    def parse_subfinder(output: str) -> Dict[str, Any]:
        """Parse Subfinder output"""
        subdomains: List[str] = []
        for line in output.split('\n'):
            line = line.strip()
            if line and not line.startswith('['):
                subdomains.append(line)
        
        return {
            'subdomains': subdomains,
            'count': len(subdomains)
        }
    
    @staticmethod
    def parse_sqlmap(output: str) -> Dict[str, Any]:
        """Parse SQLMap output"""
        result: Dict[str, Any] = {
            'vulnerable': False,
            'databases': [],
            'injection_type': '',
            'payload': ''
        }
        
        # Check if vulnerable
        if 'is vulnerable' in output.lower():
            result['vulnerable'] = True
        
        # Parse databases
        db_pattern = r'available databases \[(\d+)\]:'
        if re.search(db_pattern, output):
            # Extract database names
            db_list_pattern = r'\[\*\] (\w+)'
            result['databases'] = re.findall(db_list_pattern, output)
        
        # Parse injection type
        injection_pattern = r'Type: (.+)'
        injection_match = re.search(injection_pattern, output)
        if injection_match:
            result['injection_type'] = injection_match.group(1)
        
        return result
    
    @staticmethod
    def parse_nikto(output: str) -> Dict[str, Any]:
        """Parse Nikto output"""
        vulnerabilities: List[str] = []
        
        # Parse findings
        finding_pattern = r'\+ (.+)'
        for match in re.finditer(finding_pattern, output):
            finding = match.group(1)
            if finding and not finding.startswith('Target'):
                vulnerabilities.append(finding)
        
        return {
            'vulnerabilities': vulnerabilities,
            'count': len(vulnerabilities)
        }
    
    @staticmethod
    def parse_hydra(output: str) -> Dict[str, Any]:
        """Parse Hydra output"""
        result: Dict[str, Any] = {
            'credentials_found': [],
            'attempts': 0,
            'success': False
        }
        
        # Parse found credentials
        cred_pattern = r'\[(\d+)\]\[(\w+)\] host: (.+)\s+login: (.+)\s+password: (.+)'
        for match in re.finditer(cred_pattern, output):
            port, protocol, host, login, password = match.groups()
            result['credentials_found'].append({
                'host': host,
                'port': port,
                'login': login,
                'password': password,
                'protocol': protocol
            })
            result['success'] = True
        
        # Parse attempts
        attempts_pattern = r'(\d+) valid password'
        attempts_match = re.search(attempts_pattern, output)
        if attempts_match:
            result['attempts'] = int(attempts_match.group(1))
        
        return result
    
    @staticmethod
    def parse_whatweb(output: str) -> Dict[str, Any]:
        """Parse WhatWeb output"""
        findings = []
        for line in output.split('\n'):
            line = line.strip()
            # remove ansi colors for parsing
            clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
            if clean_line and ('[' in clean_line):
                findings.append(clean_line)
        return {
            'findings': findings,
            'count': len(findings)
        }
    @staticmethod
    def parse_nuclei(output: str) -> Dict[str, Any]:
        """Parse Nuclei output"""
        findings = []
        # Nuclei format typical: [template-id] [protocol] [severity] target
        nuclei_pattern = r'\[(.*?)\]\s+\[(.*?)\]\s+\[(.*?)\]\s+(.*)'
        for line in output.split('\n'):
            line = line.strip()
            # remove ansi colors
            clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
            match = re.search(nuclei_pattern, clean_line)
            if match:
                findings.append({
                    'template': match.group(1),
                    'protocol': match.group(2),
                    'severity': match.group(3).lower(),
                    'target': match.group(4)
                })
        return {'findings': findings, 'count': len(findings)}

    @staticmethod
    def parse_ffuf(output: str) -> Dict[str, Any]:
        """Parse ffuf output"""
        findings = []
        for line in output.split('\n'):
            clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line.strip())
            if 'Status: 200' in clean_line or 'Status: 301' in clean_line:
                findings.append(clean_line)
        return {'findings': findings, 'count': len(findings)}

    @staticmethod
    def parse_dirsearch(output: str) -> Dict[str, Any]:
        """Parse Dirsearch output"""
        findings = []
        for line in output.split('\n'):
            clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line.strip())
            # typical dirsearch output: [02:05:46] 200 -   12B  - /admin
            # We want lines that have status codes like 200, 301, 302, 401, 403, 404
            if re.search(r'\b\d{3}\b\s+-\s+', clean_line):
                findings.append(clean_line)
        return {'findings': findings, 'count': len(findings)}

    @staticmethod
    def parse_searchsploit(output: str) -> Dict[str, Any]:
        """Parse Searchsploit output"""
        findings = []
        for line in output.split('\n'):
            if '|' in line and not line.startswith('-') and not line.startswith(' '):
                parts = line.split('|')
                if len(parts) >= 2:
                    findings.append({'title': parts[0].strip(), 'path': parts[1].strip()})
        return {'findings': findings, 'count': len(findings)}

    @staticmethod
    def parse_generic(output: str) -> Dict[str, Any]:
        """Generic parser for tools without specific parsing"""
        return {
            'raw_output': output,
            'lines': len(output.split('\n')),
            'size': len(output)
        }
    
    @staticmethod
    def extract_vulnerabilities(parsed_data: Dict[str, Any], tool_name: str) -> List[Dict[str, Any]]:
        """Extract vulnerabilities from parsed data"""
        vulnerabilities: List[Dict[str, Any]] = []
        
        if tool_name == 'nmap':
            # Check for potentially vulnerable services
            open_ports = cast(List[Dict[str, Any]], parsed_data.get('open_ports', []))
            for port_info in open_ports:
                if port_info['service'] in ['telnet', 'ftp', 'rlogin']:
                    vulnerabilities.append({
                        'severity': 'medium',
                        'title': f"Insecure service: {port_info['service']}",
                        'description': f"Port {port_info['port']} is running {port_info['service']}, which transmits data in cleartext",
                        'recommendation': 'Use encrypted alternatives (SSH, SFTP, etc.)'
                    })
        
        elif tool_name == 'sqlmap':
            if parsed_data.get('vulnerable'):
                vulnerabilities.append({
                    'severity': 'critical',
                    'title': 'SQL Injection Vulnerability',
                    'description': f"SQL injection found: {parsed_data.get('injection_type', 'Unknown type')}",
                    'recommendation': 'Use parameterized queries and input validation'
                })
        
        elif tool_name == 'nikto':
            nikto_vulns = cast(List[str], parsed_data.get('vulnerabilities', []))
            for vuln in nikto_vulns:
                vulnerabilities.append({
                    'severity': 'medium',
                    'title': 'Web Server Vulnerability',
                    'description': vuln,
                    'recommendation': 'Review and patch the identified issue'
                })
                
        elif tool_name == 'whatweb':
            whatweb_findings = cast(List[str], parsed_data.get('findings', []))
            for finding in whatweb_findings:
                # Consider specific plugins as findings
                severity = 'low'
                title = 'WhatWeb Technology Finding'
                
                if 'password' in finding.lower() or 'admin' in finding.lower():
                    severity = 'high'
                    title = 'Potentially Sensitive Path/Feature'
                
                vulnerabilities.append({
                    'severity': severity,
                    'title': title,
                    'description': finding[:500],
                    'recommendation': 'Review the identified technology or endpoint for potential misconfigurations or outdated versions.'
                })
                
        elif tool_name == 'nuclei':
            nuclei_findings = cast(List[Dict[str, Any]], parsed_data.get('findings', []))
            for finding in nuclei_findings:
                vulnerabilities.append({
                    'severity': finding.get('severity', 'info'),
                    'title': f"Nuclei: {finding.get('template', 'Finding')}",
                    'description': f"Target {finding.get('target')} triggered {finding.get('template')} over {finding.get('protocol')}",
                    'recommendation': 'Review the Nuclei template logic and apply the recommended vendor patch.'
                })
                
        elif tool_name == 'ffuf':
            ffuf_findings = cast(List[str], parsed_data.get('findings', []))
            for finding in ffuf_findings:
                vulnerabilities.append({
                    'severity': 'low',
                    'title': 'Discovered Directory/File via Fuzzing',
                    'description': finding,
                    'recommendation': 'Ensure no sensitive files or administrative interfaces are unintentionally exposed.'
                })
                
        elif tool_name == 'dirsearch':
            dirsearch_findings = cast(List[str], parsed_data.get('findings', []))
            for finding in dirsearch_findings:
                status_match = re.search(r'\b(\d{3})\b', finding)
                status = status_match.group(1) if status_match else ''
                
                # Default severity
                severity = 'low'
                if status in ['200']:
                    severity = 'medium'
                    if any(kw in finding.lower() for kw in ['admin', 'login', 'config', 'backup', 'secret', '.git', '.env']):
                        severity = 'high'
                elif status in ['401', '403']:
                    severity = 'medium'
                
                if status and status != '404':
                    vulnerabilities.append({
                        'severity': severity,
                        'title': f'Discovered Directory/File ({status})',
                        'description': finding,
                        'recommendation': 'Review exposed directory or file. Restrict access if sensitive.'
                    })
                
        elif tool_name == 'searchsploit':
            sploit_findings = cast(List[Dict[str, str]], parsed_data.get('findings', []))
            for finding in sploit_findings:
                vulnerabilities.append({
                    'severity': 'high',
                    'title': f"Public Exploit Available: {finding.get('title')}",
                    'description': f"An Exploit-DB entry was found: {finding.get('path')}",
                    'recommendation': 'Update the vulnerable component immediately.'
                })
        
        return vulnerabilities
