#!/bin/bash

VENV_DIR="venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating venv..."
    python3 -m venv "$VENV_DIR"
fi

echo "Checking requirements..."
. "$VENV_DIR/bin/activate"
pip freeze > installed.txt

if ! grep -q -F -x -f requirements.txt installed.txt; then
    echo "Installing requirements..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "All requirements are already installed."
fi

if [ ! -f "settings.yaml" ]; then
    echo "File settings.yaml does not exists. Copy settings_template.yaml as settings.yaml and edit it."
    exit 1
fi

echo "Starting..."
python -m readysynk.main settings.yaml
