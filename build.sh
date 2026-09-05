#!/bin/bash

echo "Building scrcpy-gui..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python 3.8+ first"
    exit 1
fi

# Check if PySide6 is installed
if ! python3 -c "import PySide6" 2>/dev/null; then
    echo "Installing PySide6..."
    pip3 install PySide6
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install PySide6"
        exit 1
    fi
fi

# Create dist directory
mkdir -p dist

# Copy the main script
cp scrcpy_gui.py dist/scrcpy-gui.py

# Create launcher script
cat > dist/run.sh << 'EOF'
#!/bin/bash
python3 "$(dirname "$0")/scrcpy-gui.py" "$@"
EOF

chmod +x dist/run.sh

# Create requirements.txt
echo "PySide6>=6.5.0" > dist/requirements.txt

# Try to create executable with PyInstaller if available
if python3 -c "import PyInstaller" 2>/dev/null; then
    echo "Creating standalone executable..."
    cd dist
    pyinstaller --onefile --windowed --name scrcpy-gui scrcpy-gui.py
    if [ $? -ne 0 ]; then
        echo "WARNING: PyInstaller failed, using Python script instead"
    fi
    cd ..
else
    echo "PyInstaller not found. Installing..."
    pip3 install PyInstaller
    if [ $? -eq 0 ]; then
        echo "Creating standalone executable..."
        cd dist
        pyinstaller --onefile --windowed --name scrcpy-gui scrcpy-gui.py
        cd ..
    else
        echo "WARNING: Could not create standalone executable"
        echo "The application will run as a Python script"
    fi
fi

echo ""
echo "========================================"
echo "Build completed!"
echo "========================================"
echo ""
echo "To run scrcpy-gui:"
echo "  - Run: ./dist/run.sh"
echo "  - Or: python3 dist/scrcpy-gui.py"
echo ""
echo "Requirements:"
echo "  - Python 3.8+"
echo "  - PySide6"
echo "  - scrcpy (installed separately)"
echo "  - adb (for device connection)"
echo ""
