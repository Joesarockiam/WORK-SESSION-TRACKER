@echo off
echo ===================================
echo Starting Deep Work Session Tracker
echo ===================================
echo.

echo Activating Python virtual environment...
call env\Scripts\activate.bat

echo.
echo Starting FastAPI backend...
start "Backend" cmd /k "python main.py"

echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo Generating Python SDK...
if not exist "deepwork_sdk" (
    npx openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o deepwork_sdk
    if errorlevel 1 (
        echo Warning: Failed to generate SDK. Backend may not be ready yet.
    )
)

echo.
echo Starting React frontend...
cd frontend
start "Frontend" cmd /k "npm start"

echo.
echo ===================================
echo Application started!
echo ===================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
pause

