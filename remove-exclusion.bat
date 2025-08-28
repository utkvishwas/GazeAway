@echo off
echo Removing GazeAway project folder from Windows Defender exclusions...
echo.

REM Get the current directory
set "PROJECT_DIR=%CD%"

REM Remove folder exclusion from Windows Defender
powershell -Command "Remove-MpPreference -ExclusionPath '%PROJECT_DIR%'"

if %errorlevel% equ 0 (
    echo ✓ Successfully removed %PROJECT_DIR% from Windows Defender exclusions
    echo.
    echo Windows Defender will now scan files in this folder again.
) else (
    echo ✗ Failed to remove exclusion. Try running as Administrator.
    echo Right-click this file and select "Run as administrator"
)

pause
