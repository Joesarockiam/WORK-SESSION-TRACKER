# Troubleshooting Guide

## Python 3.13 Compatibility Issue

If you encounter an error about `link.exe` not found when installing dependencies with Python 3.13, you have a few options:

### Option 1: Use Pre-built Wheels (Recommended)

The setup script now upgrades pip which should resolve this. However, if you still see errors, you can pre-install the wheels:

```bash
call env\Scripts\activate.bat
pip install --upgrade pip
pip wheel -w wheels -r requirements.txt
pip install --no-index --find-links wheels -r requirements.txt
```

### Option 2: Use Python 3.11 or 3.12

Python 3.13 is very new and some packages may have compatibility issues. Switch to Python 3.11 or 3.12:

1. Install Python 3.11 or 3.12 from python.org
2. When creating the venv, specify the Python version:
   ```bash
   py -3.11 -m venv env
   ```

### Option 3: Install Visual Studio Build Tools

If you need to use Python 3.13 and build from source:

1. Download and install "Microsoft C++ Build Tools" from:
   https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022
2. During installation, select "Desktop development with C++"
3. The setup should then complete successfully

## Other Common Issues

### "ModuleNotFoundError: No module named 'sqlalchemy'"

**Solution:** Make sure you activated the virtual environment first:
```bash
env\Scripts\activate.bat
```

### Port Already in Use

If you see "Address already in use" errors:

**Backend (port 8000):**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

**Frontend (port 3000):**
```bash
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F
```

Or simply restart your computer.

### Frontend Can't Connect to Backend

**Solutions:**
1. Make sure backend is running first (check http://localhost:8000)
2. Wait 5-10 seconds after starting backend before starting frontend
3. Check that CORS is enabled in the backend (it is by default)

### Database Locked Error

If you see database lock errors:

**Solution:**
```bash
# Stop the backend
# Then delete and recreate the database
del deep_work.db
alembic upgrade head
```

### SDK Generation Fails

If OpenAPI Generator fails:

**Solutions:**
1. Make sure backend is fully running first
2. Try generating manually:
   ```bash
   npx openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o deepwork_sdk
   ```
3. If it still fails, you can skip this step - the app works without the SDK

### Tests Fail with Timezone Errors

**Solution:** This has been fixed in the latest code. Make sure you have the latest version.

If you still see errors:
```bash
pip install --upgrade pytest
```

## Getting Help

If you continue to have issues:

1. Check that all prerequisites are met (Python 3.8+, Node.js 16+)
2. Make sure you have internet connectivity
3. Try running each step manually to identify where it fails
4. Check the error messages carefully - they often contain helpful hints

## Still Stuck?

Try this minimal setup to test your environment:

```bash
# Test Python
python --version

# Test Node
node --version

# Test pip
python -m pip --version

# Create minimal venv
python -m venv test_env
test_env\Scripts\activate
pip install fastapi uvicorn
```

If this works, then the issue is with the project dependencies, not your environment.


