# 🛠️ Tool Installation Guide for CyberSuite

Complete guide to installing all penetration testing tools required by CyberSuite.

## 🚀 Quick Installation

### Automated Installation Scripts

We've provided installation scripts for your convenience:

**Windows:**
```cmd
install_tools.bat
```

**Linux/macOS:**
```bash
chmod +x install_tools.sh
./install_tools.sh
```

## 📋 Manual Installation Instructions

### Windows Installation

#### 1. Nmap
```
Download: https://nmap.org/download.html
- Run the installer
- Check "Add Nmap to PATH"
- Restart terminal after installation
```

#### 2. Python Tools (via pip)
```cmd
pip install sqlmap
pip install whatweb
pip install dirsearch
```

#### 3. Nikto
```cmd
# Option 1: Using Git
git clone https://github.com/sullo/nikto.git
cd nikto/program
# Add to PATH or use full path

# Option 2: Download ZIP
# Extract and add to PATH
```

#### 4. Hydra
```
Download: https://github.com/maaaaz/thc-hydra-windows
- Extract to C:\Tools\hydra
- Add to PATH: C:\Tools\hydra
```

#### 5. Aircrack-ng
```
Download: https://www.aircrack-ng.org/downloads.html
- Run installer
- Add to PATH during installation
```

#### 6. Metasploit Framework
```
Download: https://www.metasploit.com/
- Run installer (large download ~200MB)
- Add to PATH during installation
```

#### 7. Amass
```
Download: https://github.com/OWASP/Amass/releases
- Download Windows binary
- Extract to C:\Tools\amass
- Add to PATH
```

### Linux Installation (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install from repositories
sudo apt install -y \
    nmap \
    sqlmap \
    nikto \
    hydra \
    aircrack-ng \
    amass \
    dirsearch

# Install Python tools
pip3 install whatweb

# Install Metasploit (optional)
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod 755 msfinstall
./msfinstall
```

### Linux Installation (Arch)

```bash
# Install from official repos
sudo pacman -S nmap sqlmap nikto hydra aircrack-ng

# Install from AUR (using yay)
yay -S amass whatweb dirsearch metasploit

# Or using pip
pip3 install whatweb dirsearch sqlmap
```

### macOS Installation

```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install tools
brew install nmap sqlmap nikto hydra aircrack-ng amass metasploit

# Install Python tools
pip3 install whatweb dirsearch
```

## ✅ Verification

After installation, verify tools are accessible:

### Command Line Verification

```bash
# Test each tool
nmap --version
sqlmap --version
nikto -Version
hydra -h
aircrack-ng --help
msfconsole --version
amass -version
```

### CyberSuite Verification

1. Launch CyberSuite:
   ```bash
   python main.py
   ```

2. Go to: **Tools** → **Check Installed Tools**

3. You should see green checkmarks (✅) for installed tools

## 🔧 Troubleshooting

### Tool Not Found in PATH

**Windows:**
1. Search "Environment Variables" in Start Menu
2. Click "Environment Variables"
3. Under "System Variables", find "Path"
4. Click "Edit" → "New"
5. Add tool directory (e.g., `C:\Tools\nmap`)
6. Click OK and restart terminal

**Linux/macOS:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH=$PATH:/path/to/tool

# Reload shell
source ~/.bashrc
```

### Permission Errors

**Linux/macOS:**
```bash
# Some tools need root privileges
sudo python3 main.py

# Or add user to required groups
sudo usermod -aG sudo $USER
```

**Windows:**
- Run Command Prompt as Administrator
- Run CyberSuite with admin privileges

### Python Tools Not Working

```bash
# Upgrade pip
pip install --upgrade pip

# Install with --user flag
pip install --user sqlmap whatweb dirsearch

# Or use pip3
pip3 install sqlmap whatweb dirsearch
```

## 🎯 Recommended: Use Kali Linux

For the easiest setup, use **Kali Linux** which has all tools pre-installed:

### Option 1: Virtual Machine
1. Download Kali Linux: https://www.kali.org/get-kali/
2. Install in VirtualBox or VMware
3. All tools are pre-installed!

### Option 2: WSL2 (Windows)
```powershell
# Install WSL2
wsl --install

# Install Kali Linux
wsl --install -d kali-linux

# Launch Kali
wsl -d kali-linux

# Update and install tools
sudo apt update
sudo apt install -y kali-linux-default
```

### Option 3: Docker
```bash
# Run Kali Linux in Docker
docker pull kalilinux/kali-rolling
docker run -it kalilinux/kali-rolling /bin/bash

# Install tools
apt update
apt install -y kali-linux-default
```

## 📦 Tool Descriptions

| Tool | Purpose | Required? |
|------|---------|-----------|
| **Nmap** | Network scanning & port discovery | Recommended |
| **Amass** | Subdomain enumeration | Optional |
| **whatweb** | OSINT & email gathering | Optional |
| **SQLMap** | SQL injection testing | Recommended |
| **Dirsearch** | Directory brute-forcing | Recommended |
| **Nikto** | Web vulnerability scanning | Recommended |
| **Hydra** | Password cracking | Optional |
| **Aircrack-ng** | WiFi security testing | Optional |
| **Metasploit** | Exploitation framework | Optional |

## 🔐 Security Notes

1. **Antivirus Warnings**: Security tools may be flagged
   - Add exceptions for tool directories
   - This is normal for penetration testing tools

2. **Firewall**: May need to allow tools through firewall
   - Add rules for each tool as needed

3. **Administrator Rights**: Some tools require elevated privileges
   - Run with sudo (Linux/macOS) or as Administrator (Windows)

## 📚 Additional Resources

- **Nmap**: https://nmap.org/book/
- **Metasploit**: https://docs.metasploit.com/
- **OWASP**: https://owasp.org/
- **Kali Linux**: https://www.kali.org/docs/

## 🆘 Still Having Issues?

1. Check tool's official documentation
2. Verify system requirements
3. Check PATH configuration
4. Try manual installation
5. Consider using Kali Linux VM

---

**Remember: Only use these tools on systems you own or have explicit permission to test!** 🛡️
