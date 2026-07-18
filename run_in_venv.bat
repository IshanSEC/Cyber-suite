@echo off
echo Creating/setting up venv for CyberSuite...
if not exist cybersuite_env (
    python -m venv cybersuite_env
    echo Venv created.
)
echo Activating venv...
call cybersuite_env\Scripts\activate.bat
echo Installing/upgrading requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Launching CyberSuite GUI...
python main.py
pause
