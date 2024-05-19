#!/bin/bash

# exit if a command exits with a non zero status
set -e  

# install commonly missing packages
sudo apt install flac
sudo apt install ffmpeg

# define virtual environment directory
VENV_DIR="venv"

# check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "python3 could not be found. Please install it before running this script."
    exit 1
fi

# create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv $VENV_DIR
fi

# activate virtual environment
source $VENV_DIR/bin/activate

# upgrade pip
pip install --upgrade pip

# check if requirements file exists and install packages
if [ ! -f "requirements.txt" ]; then
    echo "requirements.txt not found. Please create it before running this script."
    deactivate
    exit 1
fi
pip install -r requirements.txt

# deactivate the virtual environment
deactivate

echo "^^^ Setup complete"
echo "   The virtual environment can be activated through: source $VENV_DIR/bin/activate"
