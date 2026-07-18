# ⚡ CyberSuite Quick Start Guide

Get up and running with CyberSuite in 5 minutes!

## 🚀 Quick Installation

### 1. Install Python Dependencies
```bash
cd cybersuite
pip install -r requirements.txt
```

### 2. Run CyberSuite
```bash
# Windows
python main.py

# Linux/macOS
python3 main.py
```

That's it! The GUI should launch.

## 🎯 First Steps

### Check Tool Status
1. Click **Tools** → **Check Installed Tools**
2. See which penetration testing tools are installed
3. Install missing tools as needed (see INSTALL.md)

### Run Your First Scan

#### Option 1: Quick Nmap Scan
1. Go to **🔍 Reconnaissance** tab
2. Select **Nmap** sub-tab
3. Enter target: `scanme.nmap.org` (official test server)
4. Select "Quick Scan (-F)"
5. Click **Start Scan**
6. Watch results appear in real-time!

#### Option 2: Web Vulnerability Scan
1. Go to **🌐 Web Testing** tab
2. Select **Nikto** sub-tab
3. Enter a test website
4. Click **Start Web Server Scan**

### View Dashboard
- Go to **🏠 Dashboard** tab
- See scan statistics
- View recent scans
- Use quick action buttons

### Generate a Report
1. Run a few scans
2. Go to **📊 Reports** tab
3. Select report type and format
4. Click **Generate Report**
5. Save the report

## 📚 Key Features to Try

### 🔍 Reconnaissance
- **Nmap**: Network scanning
- **Amass**: Find subdomains
- **whatweb**: OSINT gathering

### 🌐 Web Testing
- **SQLMap**: Test for SQL injection
- **Dirsearch**: Find hidden directories
- **Nikto**: Scan for web vulnerabilities

### 🛡️ Vulnerability Assessment
- View all discovered vulnerabilities
- Filter by severity
- Export findings

### 📊 Professional Reports
- HTML reports with styling
- JSON for automation
- CSV for spreadsheets

## ⚠️ Important Reminders

### Legal & Ethical Use
✅ **DO:**
- Test your own systems
- Use in lab environments
- Get written authorization
- Follow responsible disclosure

❌ **DON'T:**
- Test systems without permission
- Use for illegal activities
- Ignore authorization warnings

### Safety Tips
1. **Always get permission** before scanning
2. **Use test targets** like `scanme.nmap.org`
3. **Read tool documentation** before use
4. **Start with safe options** (avoid aggressive scans)
5. **Keep logs** of your testing activities

## 🎓 Learning Path

### Beginner
1. ✅ Install and launch CyberSuite
2. ✅ Run basic Nmap scan
3. ✅ Explore the dashboard
4. ✅ Generate your first report

### Intermediate
1. Try different scan types
2. Use multiple tools on same target
3. Analyze vulnerability findings
4. Create comprehensive reports

### Advanced
1. Combine multiple tools
2. Custom scan configurations
3. Integrate with your workflow
4. Contribute improvements

## 🔧 Common Issues

### "Tool not found"
- Install the tool (see INSTALL.md)
- Add to system PATH
- Or configure full path in Settings

### "Permission denied"
- Some tools need admin/root
- Run with elevated privileges
- Check file permissions

### GUI doesn't start
- Check Python version (3.8+)
- Install PySide6: `pip install PySide6`
- Check error messages

## 📖 Next Steps

1. **Read README.md** - Full documentation
2. **Check INSTALL.md** - Detailed installation
3. **Explore each tab** - Try all modules
4. **Practice ethically** - Use responsibly

## 🆘 Need Help?

- Check error messages in the GUI
- Review documentation files
- Verify tool installation
- Test with known-good targets

## 🎯 Quick Reference

### Keyboard Shortcuts
- `Ctrl+N` - New scan
- `Ctrl+Q` - Quit application

### Menu Options
- **File** → New Scan, Exit
- **Tools** → Configuration, Check Tools
- **Database** → View History, Clear History
- **Help** → About, Documentation

### Test Targets (Legal to scan)
- `scanme.nmap.org` - Nmap's official test server
- Your own local machines
- Lab environments you control

---

**Happy Ethical Hacking! 🛡️**

Remember: With great power comes great responsibility!
