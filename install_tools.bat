@echo off
echo ========================================
echo   CyberSuite - Tool Installation Script
echo   For Windows Systems
echo ========================================
echo.
echo This script will help you install penetration testing tools.
echo.
echo IMPORTANT: You need to install these tools manually on Windows.
echo This script will guide you through the process.
echo.
pause

echo.
echo ========================================
echo   Installation Instructions
echo ========================================
echo.

echo 1. NMAP - Network Scanner
echo    Download from: https://nmap.org/download.html
echo    - Run the installer
echo    - Add to PATH during installation
echo.

echo 2. PYTHON-BASED TOOLS (Can be installed via pip)
echo    Installing Python tools...
echo.

pip install sqlmap 2>nul
if %errorlevel% equ 0 (
    echo [OK] SQLMap installed successfully
) else (
    echo [FAIL] SQLMap installation failed
)

pip install whatweb 2>nul
if %errorlevel% equ 0 (
    echo [OK] whatweb installed successfully
) else (
    echo [FAIL] whatweb installation failed - may need manual installation
)

echo.
echo 3. NIKTO - Web Scanner
echo    Download from: https://github.com/sullo/nikto
echo    Or install via: git clone https://github.com/sullo/nikto.git
echo.

echo 4. HYDRA - Password Cracker
echo    Windows version: https://github.com/maaaaz/thc-hydra-windows
echo    Download and extract to a folder
echo    Add to PATH
echo.

echo 5. AIRCRACK-NG - WiFi Security
echo    Download from: https://www.aircrack-ng.org/downloads.html
echo    Install and add to PATH
echo.

echo 6. METASPLOIT FRAMEWORK
echo    Download from: https://www.metasploit.com/
echo    Run the installer
echo    Add to PATH
echo.

echo 7. AMASS - Subdomain Enumeration
echo    Download from: https://github.com/OWASP/Amass/releases
echo    Extract and add to PATH
echo.

echo 8. DIRSEARCH - Directory Scanner
echo    Install via: git clone https://github.com/maurosoria/dirsearch.git
echo    Or: pip install dirsearch
echo.

pip install dirsearch 2>nul
if %errorlevel% equ 0 (
    echo [OK] Dirsearch installed successfully
) else (
    echo [FAIL] Dirsearch installation failed
)

echo.
echo ========================================
echo   Installation Summary
echo ========================================
echo.
echo Python-based tools have been attempted via pip.
echo For other tools, please follow the download links above.
echo.
echo After installation, verify tools by running:
echo    python main.py
echo    Then go to: Tools -^> Check Installed Tools
echo.
echo ========================================
echo   Alternative: Use Kali Linux
echo ========================================
echo.
echo For easier setup, consider using Kali Linux which has
echo all these tools pre-installed:
echo    - Download: https://www.kali.org/get-kali/
echo    - Use in VirtualBox or WSL2
echo.
pause
