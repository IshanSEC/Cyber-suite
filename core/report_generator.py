"""
Report Generator for CyberSuite
Generates professional penetration testing reports
"""
import json
import csv
from datetime import datetime
from typing import Any, Dict, List

from database.db_manager import DatabaseManager

class ReportGenerator:
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager
        
    def generate_html_report(self, file_path: str, report_type: str) -> None:
        """Generate HTML report"""
        stats: Dict[str, Any] = self.db_manager.get_statistics()
        scans: List[Dict[str, Any]] = self.db_manager.get_scan_history(limit=100)
        vulns: List[Dict[str, Any]] = self.db_manager.get_vulnerabilities()
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CyberSuite Penetration Test Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .section {{
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .stat-card h3 {{
            margin: 0;
            font-size: 2em;
        }}
        .stat-card p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #667eea;
            color: white;
            font-weight: bold;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .severity-critical {{
            background-color: #ff4444;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
        }}
        .severity-high {{
            background-color: #ff8800;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
        }}
        .severity-medium {{
            background-color: #ffbb33;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
        }}
        .severity-low {{
            background-color: #00C851;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666;
            border-top: 2px solid #ddd;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔒 CyberSuite Penetration Test Report</h1>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Report Type: {report_type}</p>
    </div>
    
    <div class="section">
        <h2>📊 Executive Summary</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <h3>{stats['total_scans']}</h3>
                <p>Total Scans</p>
            </div>
            <div class="stat-card">
                <h3>{stats['total_targets']}</h3>
                <p>Targets Tested</p>
            </div>
            <div class="stat-card">
                <h3>{stats['total_vulnerabilities']}</h3>
                <p>Vulnerabilities Found</p>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>🛡️ Vulnerability Summary</h2>
        <table>
            <thead>
                <tr>
                    <th>Severity</th>
                    <th>Title</th>
                    <th>Description</th>
                    <th>Recommendation</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for vuln in vulns[:50]:  # Limit to 50 vulnerabilities
            severity_class = f"severity-{vuln.get('severity', 'low').lower()}"
            html_content += f"""
                <tr>
                    <td><span class="{severity_class}">{vuln.get('severity', 'Unknown')}</span></td>
                    <td>{vuln.get('title', 'N/A')}</td>
                    <td>{vuln.get('description', 'N/A')}</td>
                    <td>{vuln.get('recommendation', 'N/A')}</td>
                </tr>
"""
        
        html_content += """
            </tbody>
        </table>
    </div>
    
    <div class="section">
        <h2>📋 Scan History</h2>
        <table>
            <thead>
                <tr>
                    <th>Target</th>
                    <th>Tool</th>
                    <th>Date</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for scan in scans[:30]:  # Limit to 30 scans
            html_content += f"""
                <tr>
                    <td>{scan.get('target', 'N/A')}</td>
                    <td>{scan.get('tool', 'N/A')}</td>
                    <td>{scan.get('date', 'N/A')}</td>
                    <td>{scan.get('status', 'N/A')}</td>
                </tr>
"""
        
        html_content += """
            </tbody>
        </table>
    </div>
    
    <div class="footer">
        <p><strong>CyberSuite v1.0</strong> - All-in-One Penetration Testing Suite</p>
        <p>⚠️ This report is confidential and should be handled according to your organization's security policies.</p>
        <p>© 2026 CyberSec Team</p>
    </div>
</body>
</html>
"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def generate_pdf_report(self, file_path: str, report_type: str):
        """Generate PDF report using reportlab if available."""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        except ImportError:
            html_path = file_path.replace('.pdf', '.html')
            self.generate_html_report(html_path, report_type)
            raise Exception(
                f"PDF generation requires reportlab.\n"
                f"HTML report generated instead: {html_path}\n"
                f"Install it with: pip install reportlab"
            )

        stats: Dict[str, Any] = self.db_manager.get_statistics()
        scans: List[Dict[str, Any]] = self.db_manager.get_scan_history(limit=100)
        vulns: List[Dict[str, Any]] = self.db_manager.get_vulnerabilities()

        doc = SimpleDocTemplate(file_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story: List[Any] = []

        title_style = styles['Heading1']
        title_style.alignment = 1
        story.append(Paragraph('CyberSuite Penetration Test Report', title_style))
        story.append(Spacer(1, 12))

        story.append(Paragraph(f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', styles['Normal']))
        story.append(Paragraph(f'Report Type: {report_type}', styles['Normal']))
        story.append(Spacer(1, 24))

        summary_style = ParagraphStyle(
            name='Summary',
            parent=styles['Heading2'],
            textColor=colors.darkblue
        )
        story.append(Paragraph('Executive Summary', summary_style))
        story.append(Spacer(1, 12))

        summary_data: List[List[str]] = [
            ['Total Scans', str(stats['total_scans'])],
            ['Targets Tested', str(stats['total_targets'])],
            ['Vulnerabilities Found', str(stats['total_vulnerabilities'])]
        ]
        summary_table = Table(summary_data, hAlign='LEFT', colWidths=[200, 200])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 24))

        story.append(Paragraph('Vulnerability Summary', summary_style))
        story.append(Spacer(1, 12))

        vuln_data: List[List[str]] = [['Severity', 'Title', 'Description', 'Recommendation']]
        for vuln in vulns[:50]:
            vuln_data.append([
                vuln.get('severity', 'Unknown'),
                vuln.get('title', 'N/A'),
                vuln.get('description', 'N/A'),
                vuln.get('recommendation', 'N/A')
            ])

        vuln_table = Table(vuln_data, hAlign='LEFT', colWidths=[80, 140, 180, 140])
        vuln_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
        ]))
        story.append(vuln_table)
        story.append(Spacer(1, 24))

        story.append(Paragraph('Scan History', summary_style))
        story.append(Spacer(1, 12))

        scan_data: List[List[str]] = [['Target', 'Tool', 'Date', 'Status']]
        for scan in scans[:30]:
            scan_data.append([
                scan.get('target', 'N/A'),
                scan.get('tool', 'N/A'),
                scan.get('date', 'N/A'),
                scan.get('status', 'N/A')
            ])

        scan_table = Table(scan_data, hAlign='LEFT', colWidths=[140, 120, 120, 100])
        scan_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
        ]))
        story.append(scan_table)
        story.append(Spacer(1, 24))

        footer_style = ParagraphStyle(
            name='Footer',
            parent=styles['Normal'],
            alignment=1,
            textColor=colors.grey
        )
        story.append(Paragraph('CyberSuite v1.0 - All-in-One Penetration Testing Suite', footer_style))
        story.append(Paragraph('⚠️ This report is confidential and should be handled according to your organization\'s security policies.', footer_style))

        doc.build(story)
    
    def generate_json_report(self, file_path: str) -> None:
        """Generate JSON report"""
        stats: Dict[str, Any] = self.db_manager.get_statistics()
        scans: List[Dict[str, Any]] = self.db_manager.get_scan_history(limit=100)
        vulns: List[Dict[str, Any]] = self.db_manager.get_vulnerabilities()
        
        report_data: Dict[str, Any] = {
            'generated_at': datetime.now().isoformat(),
            'statistics': stats,
            'scans': scans,
            'vulnerabilities': vulns
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2)
    
    def generate_csv_report(self, file_path: str) -> None:
        """Generate CSV report of vulnerabilities"""
        vulns: List[Dict[str, Any]] = self.db_manager.get_vulnerabilities()
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            if vulns:
                fieldnames = ['severity', 'title', 'description', 'recommendation', 'date']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                writer.writeheader()
                for vuln in vulns:
                    writer.writerow({
                        'severity': vuln.get('severity', ''),
                        'title': vuln.get('title', ''),
                        'description': vuln.get('description', ''),
                        'recommendation': vuln.get('recommendation', ''),
                        'date': vuln.get('date', '')
                    })
