@echo off
set VENV_DIR=venv

if not exist %VENV_DIR% (
    echo Creating venv...
    python -m venv %VENV_DIR%
)

echo Checking requirements...
%VENV_DIR%\Scripts\pip freeze > installed.txt
findstr /i /g:requirements.txt installed.txt > nul
if %errorlevel% neq 0 (
    echo Installing requirements...
    %VENV_DIR%\Scripts\pip install --upgrade pip
    %VENV_DIR%\Scripts\pip install -r requirements.txt
) else (
    echo All requirements are already installed.
)

if not exist "settings.yaml" (
    echo File settings.yaml does not exists. Copy settings_template.yaml as settings.yaml and edit it.
    exit /b 1
)

echo Starting...
%VENV_DIR%\Scripts\python -m readysynk.main settings.yaml
