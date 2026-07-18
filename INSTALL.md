# 🚀 CyberSuite Installation Guide

Complete step-by-step installation instructions for CyberSuite.

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Python Installation](#python-installation)
3. [CyberSuite Installation](#cybersuite-installation)
4. [Tool Installation](#tool-installation)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

## 💻 System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, Linux (Ubuntu 20.04+, Debian 10+, Arch), macOS 10.15+
- **Python**: 3.8 or higher
- **RAM**: 4GB
- **Disk Space**: 500MB for CyberSuite + 2-5GB for tools
- **Display**: 1280x720 minimum resolution

### Recommended Requirements
- **RAM**: 8GB or more
- **Disk Space**: 10GB+ for tools and wordlists
- **Display**: 1920x1080 or higher

## 🐍 Python Installation

### Windows

1. **Download Python**
   - Visit https://www.python.org/downloads/
   - Download Python 3.8 or higher
   - Run the installer

2. **Important**: Check "Add Python to PATH" during installation

3. **Verify Installation**
   ```cmd
   python --version
   pip --version
   ```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

### Linux (Arch)

```bash
sudo pacman -S python python-pip
python --version
```

### macOS

```bash
# Using Homebrew
brew install python3
python3 --version
```

## 📦 CyberSuite Installation

### Step 1: Navigate to CyberSuite Directory

```bash
cd cybersuite
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- PySide6 (GUI framework)
- Other required packages

### Step 4: Verify Installation

```bash
python main.py
```

If the GUI opens, CyberSuite is installed correctly!

## 🛠️ Tool Installation

CyberSuite integrates with external penetration testing tools. Install the ones you need:

### Windows

#### Nmap
1. Download from https://nmap.org/download.html
2. Run installer
3. Add to PATH: `C:\Program Files (x86)\Nmap`

#### SQLMap
```cmd
pip install sqlmap
```

#### Other Tools
- Download from official websites
- Extract to a directory
- Add to system PATH

### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install tools
sudo apt install -y \
    nmap \
    sqlmap \
    nikto \
    hydra \
    aircrack-ng

# Install Amass
sudo apt install amass

# Install whatweb
sudo apt install whatweb

# Install Dirsearch
git clone https://github.com/maurosoria/dirsearch.git
cd dirsearch
sudo python3 setup.py install
```

### Linux (Arch)

```bash
# Install from official repos
sudo pacman -S nmap sqlmap nikto hydra aircrack-ng

# Install from AUR (using yay)
yay -S amass whatweb dirsearch
```

### macOS

```bash
# Using Homebrew
brew install nmap sqlmap nikto hydra aircrack-ng

# Install whatweb
pip3 install whatweb

# Install Dirsearch
git clone https://github.com/maurosoria/dirsearch.git
cd dirsearch
python3 setup.py install
```

### Metasploit Framework

**Linux:**
```bash
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod 755 msfinstall
./msfinstall
```

**Windows:**
- Download installer from https://www.metasploit.com/
- Run installer
- Add to PATH

**macOS:**
```bash
brew install metasploit
```

## ✅ Verification

### Check CyberSuite

```bash
python main.py
```

The application should launch with the dark-themed GUI.

### Check Installed Tools

1. Launch CyberSuite
2. Go to **Tools** → **Check Installed Tools**
3. Review the status of each tool

You should see:
- ✅ Green checkmarks for installed tools
- ❌ Red X for missing tools

### Test a Simple Scan

1. Go to **Reconnaissance** tab
2. Select **Nmap** sub-tab
3. Enter target: `scanme.nmap.org` (official test server)
4. Click **Start Scan**
5. View results

## 🔧 Troubleshooting

### Python Not Found

**Windows:**
- Reinstall Python with "Add to PATH" checked
- Manually add Python to PATH

**Linux/macOS:**
- Use `python3` instead of `python`
- Install Python from package manager

### PySide6 Installation Fails

```bash
# Try upgrading pip first
pip install --upgrade pip

# Then install PySide6
pip install PySide6
```

### Tools Not Detected

1. **Check Installation**
   ```bash
   nmap --version
   sqlmap --version
   ```

2. **Add to PATH**
   - Windows: System Properties → Environment Variables → PATH
   - Linux/macOS: Add to `~/.bashrc` or `~/.zshrc`

3. **Use Full Paths**
   - Configure in Tools → Configuration
   - Specify full path to each tool

### Permission Errors

**Linux/macOS:**
```bash
# Some tools need root privileges
sudo python3 main.py
```

**Windows:**
- Run as Administrator

### Database Errors

```bash
# Reset database
rm database/scans.db

# Restart application
python main.py
```

## 🎓 Next Steps

After installation:

1. **Read the README** - Understand features and usage
2. **Check Legal Disclaimer** - Understand ethical use
3. **Explore Dashboard** - Familiarize with interface
4. **Run Test Scans** - Use authorized test targets
5. **Generate Reports** - Practice report generation

## 📚 Additional Resources

- **Official Documentation**: See README.md
- **Tool Documentation**: Visit each tool's official website
- **Python Documentation**: https://docs.python.org/
- **PySide6 Documentation**: https://doc.qt.io/qtforpython/

## ⚠️ Important Notes

1. **Virtual Environment**: Always recommended to avoid conflicts
2. **Administrator Rights**: Some tools require elevated privileges
3. **Firewall**: May need to allow tools through firewall
4. **Antivirus**: Security tools may be flagged - add exceptions
5. **Legal**: Only use on authorized systems

## 🆘 Getting Help

If you encounter issues:

1. Check error messages carefully
2. Review this installation guide
3. Verify all requirements are met
4. Check tool installation status
5. Review troubleshooting section

---

**Happy Ethical Hacking! 🛡️**
