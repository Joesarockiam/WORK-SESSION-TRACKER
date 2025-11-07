# Quick Start Guide

## Preview the Deep Work Session Tracker

Follow these simple steps to get the project running:

### Option 1: Automatic Setup (Recommended for Windows)

1. **Run the setup script:**
   ```bash
   setupdev.bat
   ```
   Wait for it to complete (installs all dependencies)

2. **Start the application:**
   ```bash
   runapplication.bat
   ```

3. **Access the application:**
   - Frontend: Open http://localhost:3000 in your browser
   - Backend API Docs: Open http://localhost:8000/docs in your browser

### Option 2: Manual Setup

#### Step 1: Backend Setup

```bash
# Create virtual environment
python -m venv env

# Activate it (Windows)
env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the backend server
python main.py
```

The backend will be available at: http://localhost:8000

#### Step 2: Frontend Setup (in a new terminal)

```bash
cd frontend

# Install dependencies
npm install

# Start the frontend
npm start
```

The frontend will automatically open at: http://localhost:3000

### What You'll See

**Frontend Interface:**
- **Sessions Tab**: Schedule new sessions, start/pause/resume/complete active sessions
- **History Tab**: View all past sessions with detailed stats
- **Reports Tab**: Weekly productivity metrics and focus scores

**Backend API:**
- Visit http://localhost:8000/docs for interactive API documentation (Swagger UI)
- Try out all endpoints directly from the browser

### Running Tests

```bash
# Activate virtual environment first
env\Scripts\activate

# Run tests
pytest tests/ -v
```

All 13 tests should pass ✓

### Stop the Application

Press `Ctrl+C` in each terminal window running the backend and frontend.

### Troubleshooting

**If you see "ModuleNotFoundError":**
- Make sure you activated the virtual environment: `env\Scripts\activate`

**If port 3000 or 8000 is already in use:**
- Close other applications using those ports
- Or modify the ports in the configuration

**If frontend can't connect to backend:**
- Make sure the backend is running first
- Check that backend is on http://localhost:8000

### Next Steps

1. Create your first deep work session
2. Try pausing and resuming to see interruption tracking
3. View your focus score in the Reports tab
4. Export your data as CSV
5. Read the full README.md for more details

Enjoy tracking your deep work sessions! 🎯


