#!/bin/bash
# Launcher for Portfolio GUI Manager (Linux/Mac)

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3 to run this application."
    exit 1
fi

# Check if tkinter is installed
python3 -c "import tkinter" &> /dev/null
if [ $? -ne 0 ]; then
    echo "Error: tkinter module is not found."
    echo "Please install python3-tk package."
    echo "Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "Fedora: sudo dnf install python3-tkinter"
    echo "Arch: sudo pacman -S tk"
    read -p "Press Enter to exit..."
    exit 1
fi

# Run the application
echo "Starting Portfolio Manager..."
./venv/bin/python3 gui_app.py
