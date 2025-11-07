@echo off
echo ===================================
echo Deep Work Session Tracker Setup
echo ===================================
echo.

echo Setting up backend...
python -m venv env
if errorlevel 1 (
    echo Failed to create virtual environment
    pause
    exit /b 1
)

call env\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install Python dependencies
    pause
    exit /b 1
)

echo Running database migrations...
alembic upgrade head
if errorlevel 1 (
    echo Failed to run migrations
    pause
    exit /b 1
)

echo.
echo Setting up frontend...
cd frontend
npm install
if errorlevel 1 (
    echo Failed to install frontend dependencies
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo Installing OpenAPI Generator CLI (if not already installed)...
npm install -g @openapitools/openapi-generator-cli
if errorlevel 1 (
    echo Note: Failed to install OpenAPI Generator CLI. You may need to install it manually.
)

echo.
echo ===================================
echo Setup complete!
echo ===================================
echo.
echo To start the application, run: runapplication.bat
pause

