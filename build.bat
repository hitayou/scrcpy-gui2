@echo off
chcp 65001 >nul
echo Building scrcpy-gui...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if PySide6 is installed
python -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo Installing PySide6...
    pip install PySide6
    if errorlevel 1 (
        echo ERROR: Failed to install PySide6
        pause
        exit /b 1
    )
)

REM Create dist directory
if not exist "dist" mkdir dist

REM Copy the main script
copy scrcpy_gui.py dist\scrcpy-gui.py >nul

REM Create launcher script
echo @echo off > dist\run.bat
echo chcp 65001 >nul >> dist\run.bat
echo python scrcpy-gui.py %%* >> dist\run.bat

REM Create requirements.txt
echo PySide6>=6.5.0 > dist\requirements.txt

REM Try to create executable with PyInstaller if available
python -c "import PyInstaller" >nul 2>&1
if not errorlevel 1 (
    echo Creating standalone executable...
    cd dist
    pyinstaller --onefile --windowed --name scrcpy-gui --icon=NONE scrcpy-gui.py
    if errorlevel 1 (
        echo WARNING: PyInstaller failed, using Python script instead
    )
    cd ..
) else (
    echo PyInstaller not found. Installing...
    pip install PyInstaller
    if not errorlevel 1 (
        echo Creating standalone executable...
        cd dist
        pyinstaller --onefile --windowed --name scrcpy-gui --icon=NONE scrcpy-gui.py
        cd ..
    ) else (
        echo WARNING: Could not create standalone executable
        echo The application will run as a Python script
    )
)

echo.
echo ========================================
echo Build completed!
echo ========================================
echo.
echo To run scrcpy-gui:
echo   - Run: dist\run.bat
echo   - Or: python dist\scrcpy-gui.py
echo.
echo Requirements:
echo   - Python 3.8+
echo   - PySide6
echo   - scrcpy (installed separately)
echo   - adb (for device connection)
echo.
pause
