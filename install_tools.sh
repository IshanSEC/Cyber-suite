#!/bin/bash

echo "========================================"
echo "  CyberSuite - Tool Installation Script"
echo "  For Linux/macOS Systems"
echo "========================================"
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo "Detected: Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    echo "Detected: macOS"
else
    echo "Unsupported OS"
    exit 1
fi

echo ""
echo "This script will install penetration testing tools."
echo "You may need to enter your password for sudo commands."
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Update package manager
echo ""
echo "========================================"
echo "  Updating Package Manager"
echo "========================================"

if [ "$OS" == "linux" ]; then
    if command_exists apt; then
        echo "Using apt (Debian/Ubuntu)..."
        sudo apt update
        PKG_MANAGER="apt"
    elif command_exists pacman; then
        echo "Using pacman (Arch)..."
        sudo pacman -Sy
        PKG_MANAGER="pacman"
    elif command_exists dnf; then
        echo "Using dnf (Fedora)..."
        sudo dnf check-update
        PKG_MANAGER="dnf"
    else
        echo "No supported package manager found"
        exit 1
    fi
elif [ "$OS" == "macos" ]; then
    if ! command_exists brew; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    echo "Updating Homebrew..."
    brew update
    PKG_MANAGER="brew"
fi

# Install tools
echo ""
echo "========================================"
echo "  Installing Penetration Testing Tools"
echo "========================================"

install_tool() {
    local tool=$1
    local package=$2
    
    if command_exists "$tool"; then
        echo "[SKIP] $tool is already installed"
        return 0
    fi
    
    echo ""
    echo "Installing $tool..."
    
    if [ "$PKG_MANAGER" == "apt" ]; then
        sudo apt install -y "$package"
    elif [ "$PKG_MANAGER" == "pacman" ]; then
        sudo pacman -S --noconfirm "$package"
    elif [ "$PKG_MANAGER" == "dnf" ]; then
        sudo dnf install -y "$package"
    elif [ "$PKG_MANAGER" == "brew" ]; then
        brew install "$package"
    fi
    
    if command_exists "$tool"; then
        echo "[OK] $tool installed successfully"
    else
        echo "[FAIL] $tool installation failed"
    fi
}

# Install each tool
install_tool "nmap" "nmap"
install_tool "sqlmap" "sqlmap"
install_tool "nikto" "nikto"
install_tool "hydra" "hydra"
install_tool "dirsearch" "dirsearch"
install_tool "nuclei" "nuclei"
install_tool "ffuf" "ffuf"
install_tool "searchsploit" "exploitdb"

# Aircrack-ng
if [ "$OS" == "linux" ]; then
    install_tool "aircrack-ng" "aircrack-ng"
elif [ "$OS" == "macos" ]; then
    install_tool "aircrack-ng" "aircrack-ng"
fi

# Python-based tools
echo ""
echo "Installing Python-based tools..."

pip3 install --user sqlmap 2>/dev/null
sudo apt install -y whatweb

# Amass
echo ""
echo "Installing Amass..."
if [ "$PKG_MANAGER" == "apt" ]; then
    sudo apt install -y amass
elif [ "$PKG_MANAGER" == "brew" ]; then
    brew install amass
elif [ "$PKG_MANAGER" == "pacman" ]; then
    # Amass might be in AUR
    echo "For Arch Linux, install amass from AUR: yay -S amass"
fi

# Metasploit (optional - large installation)
echo ""
read -p "Install Metasploit Framework? (large download) [y/N]: " install_msf

if [[ $install_msf =~ ^[Yy]$ ]]; then
    echo "Installing Metasploit..."
    if [ "$OS" == "linux" ]; then
        curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
        chmod 755 msfinstall
        ./msfinstall
        rm msfinstall
    elif [ "$OS" == "macos" ]; then
        brew install metasploit
    fi
fi



# Summary
echo ""
echo "========================================"
echo "  Installation Complete!"
echo "========================================"
echo ""
echo "Verifying installations..."
echo ""

tools=("nmap" "sqlmap" "nikto" "hydra" "aircrack-ng" "msfconsole" "amass" "nuclei" "ffuf" "searchsploit")

for tool in "${tools[@]}"; do
    if command_exists "$tool"; then
        echo "[✓] $tool - Installed"
    else
        echo "[✗] $tool - Not found"
    fi
done

echo ""
echo "========================================"
echo "  Next Steps"
echo "========================================"
echo ""
echo "1. Launch CyberSuite: python3 main.py"
echo "2. Go to: Tools → Check Installed Tools"
echo "3. Verify all tools are detected"
echo ""
echo "If any tools are missing, you may need to:"
echo "  - Add them to your PATH"
echo "  - Install manually from official sources"
echo "  - Check installation logs above"
echo ""
echo "Happy Ethical Hacking! 🛡️"
echo ""
