@echo off
echo Adding GazeAway project folder to Windows Defender exclusions...
echo.

REM Get the current directory
set "PROJECT_DIR=%CD%"

REM Add folder exclusion to Windows Defender
powershell -Command "Add-MpPreference -ExclusionPath '%PROJECT_DIR%'"

if %errorlevel% equ 0 (
    echo ✓ Successfully added %PROJECT_DIR% to Windows Defender exclusions
    echo.
    echo Windows Defender will no longer scan files in this folder.
    echo You can now build GazeAway without false positive detection.
    echo.
    echo To remove this exclusion later, run: remove-exclusion.bat
) else (
    echo ✗ Failed to add exclusion. Try running as Administrator.
    echo Right-click this file and select "Run as administrator"
)

pause
