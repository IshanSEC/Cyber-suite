# CyberSuite

## 🛡️ About the Project

**CyberSuite** is an **All-in-One GUI Penetration Testing Suite** built in Python using PySide6. It provides a unified, graphical interface to manage and execute various popular penetration testing and reconnaissance tools. 

Instead of juggling multiple command-line interfaces, CyberSuite brings together powerful security tools into a single, cohesive dashboard where you can:
- Perform **Reconnaissance** (e.g., using Nmap, Amass, whatweb).
- Conduct **Web Testing** (e.g., using SQLMap, Dirsearch, Nikto).
- Manage **Vulnerability Assessments** (filter, view, and organize discovered vulnerabilities).
- Generate **Professional Reports** (HTML, JSON, CSV) to share your findings.

CyberSuite is designed for security professionals, ethical hackers, and students looking for a streamlined workflow during security assessments.

**Disclaimer:** CyberSuite is strictly for educational purposes and authorized security testing. Always obtain explicit written permission before scanning any networks or applications.

---

## ⚙️ Installation Process

### Prerequisites
- Python 3.8 or higher installed on your system.
- Some modules require external underlying tools (e.g., Nmap, Nikto, SQLMap) to be installed on your OS and available in your system's PATH.

### Step-by-Step Installation

1. **Clone or Download the Repository:**
   Ensure you have the project files locally on your machine.
   ```bash
   cd cybersuite
   ```

2. **Create a Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   # venv\Scripts\activate   # On Windows
   ```

3. **Install Python Dependencies:**
   Run the following command to install required Python packages (such as `PySide6`):
   ```bash
   pip install -r requirements.txt
   ```

*(For detailed tool-specific installation instructions like installing Nmap or Nikto on your system, please refer to the `INSTALL.md` or `TOOL_INSTALLATION.md` file).*

---

## 🚀 How to Run It

Once you have installed the required Python dependencies, you can start CyberSuite easily.

From your terminal or command prompt, navigate to the `cybersuite` directory and run the `main.py` script:

### On Linux / macOS:
```bash
python3 main.py
```

### On Windows:
```bash
python main.py
```

*Alternatively, you can use the provided batch (`run.bat`) or shell (`run.sh`) scripts to start the application.*

The CyberSuite Graphical User Interface (GUI) will launch automatically. From there, you can navigate the tabs, configure your settings, and begin your ethical hacking workflows!

> **Note:** Some scans (like aggressive Nmap scans) might require administrative or root privileges. If you encounter permission errors, you may need to run the application with elevated privileges (e.g., `sudo python3 main.py` on Linux), although this should be done with caution.
