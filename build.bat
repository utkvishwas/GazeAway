@echo off
echo ========================================
echo GazeAway Complete Build Process
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python from: https://python.org/downloads/
    pause
    exit /b 1
)

echo Step 1: Installing Python requirements...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install requirements!
    pause
    exit /b 1
)
echo ✓ Requirements installed successfully
echo.

echo Step 2: Building GazeAway executable...
python build-script.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to build GazeAway.exe!
    pause
    exit /b 1
)

REM Check if GazeAway.exe was created in dist folder
if not exist "dist\GazeAway.exe" (
    echo ERROR: GazeAway.exe was not created in dist folder!
    echo Check the build output for errors.
    pause
    exit /b 1
)
echo ✓ GazeAway.exe built successfully in dist folder

REM Copy GazeAway.exe from dist folder to current directory for NSIS
echo Copying GazeAway.exe to current directory...
copy "dist\GazeAway.exe" "GazeAway.exe" >nul
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy GazeAway.exe to current directory!
    pause
    exit /b 1
)
echo ✓ GazeAway.exe copied to current directory

REM Copy icon.ico to current directory for NSIS installer
echo Copying icon.ico to current directory...
copy "build\icon.ico" "icon.ico" >nul
if %errorlevel% neq 0 (
    echo WARNING: Failed to copy icon.ico to current directory!
    echo Installer will continue without icon file.
) else (
    echo ✓ icon.ico copied to current directory
)
echo.

echo Step 3: Building installer...
REM Try to build the installer directly
makensis installer.nsi
if errorlevel 1 (
    echo.
    echo WARNING: Failed to build installer!
    echo NSIS might not be installed or not in PATH.
    echo.
    echo You can still use the executable: dist\GazeAway.exe
    echo To build installer later, install NSIS and run: makensis installer.nsi
    echo.
    echo Build completed with executable only.
    echo.
    pause
    exit /b 0
)
echo ✓ Installer built successfully
echo.
REM Check if required files exist
if not exist "icon.ico" (
    echo WARNING: icon.ico not found. Installer will use default icon.
) else (
    echo ✓ icon.ico found
)

if not exist "notification.wav" (
    echo WARNING: notification.wav not found. Installer will skip this file.
) else (
    echo ✓ notification.wav found
)
echo.

echo.
echo ========================================
echo ✓ BUILD COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Files created:
echo - GazeAway.exe (executable - in current directory)
echo - dist\GazeAway.exe (executable - backup in dist folder)
if exist "GazeAway-Setup.exe" (
    echo - GazeAway-Setup.exe (installer)
    echo.
    echo You can now distribute GazeAway-Setup.exe to users.
) else (
    echo.
    echo Installer was not created. You can still use the executable.
)
echo.

pause
