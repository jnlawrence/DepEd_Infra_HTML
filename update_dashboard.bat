@echo off
echo Updating Dashboard Data...
echo =========================
echo.
echo 1. Parsing RegionalProfile.csv...
python parse_data.py
if %ERRORLEVEL% NEQ 0 (
    echo Error running python script!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo 2. Copying data to Offline Dashboard...
copy /Y "dashboard_data.js" "Offline_Dashboard\dashboard_data.js"
if %ERRORLEVEL% NEQ 0 (
    echo Error copying file!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo =========================
echo SUCCESS! Dashboard updated.
echo You can now zip the "Offline_Dashboard" folder.
echo =========================
pause
