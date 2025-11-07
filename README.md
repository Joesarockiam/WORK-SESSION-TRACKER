# Deep Work Session Tracker

A comprehensive productivity tracking system for monitoring focused work sessions with detailed interruption analysis and performance metrics.

## Overview

The Deep Work Session Tracker helps you manage your focused work sessions by tracking:
- Session planning and scheduling
- Real-time session monitoring with countdown timer
- Interruption logging and analysis
- Automatic status classification (completed, interrupted, abandoned, overdue)
- Weekly productivity reports with focus scores
- CSV export for external analysis

## Features

### Core Functionality

- **Session Management**: Schedule, start, pause, resume, and complete work sessions
- **State Machine**: Robust session lifecycle with automatic status detection
- **Interruption Tracking**: Log and analyze what disrupts your focus
- **Real-time Timer**: Visual countdown timer with progress indicator
- **Smart Classification**: Sessions are automatically categorized based on behavior:
  - ✅ **Completed**: Successfully finished within time
  - ⚠️ **Interrupted**: Paused more than 3 times
  - ❌ **Abandoned**: Paused but never resumed
  - ⏰ **Overdue**: Exceeded scheduled duration by more than 10%

### Add-on Features

- **Focus Score Calculation**: Measure concentration quality based on interruptions and completion
- **Weekly Reports**: Aggregate productivity data and trends
- **CSV Export**: Download session data for spreadsheet analysis
- **Top Interruption Analysis**: Identify your most common distractions
- **Python SDK**: Programmatic access via auto-generated SDK

## Architecture

```
Deep Work Session Tracker/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── schemas.py          # Pydantic schemas
│   │   ├── database.py         # Database configuration
│   │   ├── routers/
│   │   │   └── sessions.py     # REST endpoints
│   │   └── services/
│   │       └── session_service.py  # Business logic
│   ├── alembic/          # Database migrations
│   └── tests/            # Unit tests
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── api/          # API client
│   │   └── App.js        # Main application
│   └── public/
├── deepwork_sdk/         # Generated Python SDK
├── setupdev.bat          # Setup script
├── runapplication.bat    # Run script
└── README.md             # This file
```

### Tech Stack

**Backend:**
- FastAPI: Modern async web framework
- SQLAlchemy: ORM for database operations
- Alembic: Database migration management
- SQLite: Lightweight database
- Pydantic: Data validation

**Frontend:**
- React: UI library
- Axios: HTTP client
- CSS3: Styling and animations

**DevOps:**
- OpenAPI Generator: SDK generation
- Python virtual environment
- npm: Package management

## Prerequisites

- Python 3.8 or higher
- Node.js 16+ and npm
- Git (optional)

## Installation

### Quick Setup (Windows)

1. **Clone or extract the project:**
   ```bash
   cd "Deep Work Session Tracker"
   ```

2. **Run the setup script:**
   ```bash
   setupdev.bat
   ```
   
   This will:
   - Create a Python virtual environment
   - Install all backend dependencies
   - Run database migrations
   - Install frontend dependencies
   - Install OpenAPI Generator CLI

3. **Start the application:**
   ```bash
   runapplication.bat
   ```

   This will:
   - Start the FastAPI backend on http://localhost:8000
   - Generate the Python SDK
   - Start the React frontend on http://localhost:3000

### Manual Setup

#### Backend Setup

```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# Windows:
env\Scripts\activate
# Linux/Mac:
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## Usage

### Using the Web Interface

1. **Schedule a Session:**
   - Enter a title, optional goal, and duration
   - Click "Schedule Session"

2. **Start Working:**
   - Click "Start Session" when ready
   - Watch the countdown timer

3. **Handle Interruptions:**
   - Click "Pause" when distracted
   - Select or enter a reason
   - Click "Resume" to continue

4. **Complete Session:**
   - Click "Complete" when finished
   - View status and stats in history

5. **View Reports:**
   - Navigate to "Reports" tab
   - See weekly productivity metrics
   - Export data as CSV

### Using the Python SDK

```python
from deepwork_sdk import ApiClient
from deepwork_sdk.api.sessions_api import SessionsApi

# Create client and API instance
client = ApiClient()
api = SessionsApi(client)

# Create a session
session = api.sessions_post(
    title="My Work Session",
    goal="Complete project documentation",
    scheduled_duration=45
)

# Start the session
api.sessions_session_id_start_patch(session.id)

# Pause with a reason
api.sessions_session_id_pause_patch(
    session.id, 
    pause_request={"reason": "phone call"}
)

# Resume
api.sessions_session_id_resume_patch(session.id)

# Complete
api.sessions_session_id_complete_patch(session.id)

# Get history
history = api.sessions_history_get()
```

See `sample_sdk_usage.py` for a complete example.

### API Endpoints

All endpoints are documented via Swagger UI at http://localhost:8000/docs

**Session Management:**
- `POST /sessions/` - Create new session
- `PATCH /sessions/{id}/start` - Start a session
- `PATCH /sessions/{id}/pause` - Pause with reason
- `PATCH /sessions/{id}/resume` - Resume session
- `PATCH /sessions/{id}/complete` - Complete session

**Analytics:**
- `GET /sessions/history` - Get all sessions
- `GET /sessions/report/weekly` - Weekly productivity report
- `GET /sessions/export/csv` - Export to CSV
- `GET /sessions/{id}/focus-score` - Calculate focus score

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

The tests cover:
- Session state transitions
- Validation rules (pause limits, overdue detection)
- Interruption logging
- Focus score calculation
- Weekly report generation

All tests should pass (13/13).

## Database Schema

**Sessions Table:**
- `id`: Primary key
- `title`: Session title
- `goal`: Optional goal description
- `scheduled_duration`: Planned duration in minutes
- `start_time`: When session started
- `end_time`: When session ended
- `status`: Current status
- `pause_count`: Number of interruptions
- `created_at`: Timestamp

**Interruptions Table:**
- `id`: Primary key
- `session_id`: Foreign key to sessions
- `reason`: Why the session was paused
- `pause_time`: When paused
- `resume_time`: When resumed (null if abandoned)

## Business Logic

### Session State Machine

```
scheduled → active → paused ↔ resumed → completed
                              ↓
                          abandoned
                              ↓
                          overdue
                              ↓
                          interrupted (>3 pauses)
```

### Validation Rules

1. **Can only pause if status is 'active'**
2. **Pause limit**: Sessions with more than 3 pauses are marked 'interrupted'
3. **Overdue detection**: Sessions exceeding scheduled duration by >10% are 'overdue'
4. **Abandoned detection**: Sessions completed while paused are 'abandoned'

### Focus Score Formula

```
focus_score = (1 - interruption_penalty) × completion_ratio × 100

where:
  interruption_penalty = min(pause_count / scheduled_duration, 1.0)
  completion_ratio = 1.0 if completed, else 0.5
```

## Development

### Project Structure

- **Backend**: FastAPI application with service layer architecture
- **Frontend**: Component-based React application
- **Migrations**: Alembic for schema versioning
- **Testing**: Pytest with full coverage

### Adding Features

1. **Backend Changes:**
   - Update models in `app/models.py`
   - Create Alembic migration: `alembic revision --autogenerate -m "description"`
   - Update schemas in `app/schemas.py`
   - Add service logic in `app/services/session_service.py`
   - Create routes in `app/routers/sessions.py`

2. **Frontend Changes:**
   - Add components in `frontend/src/components/`
   - Update routing in `frontend/src/App.js`
   - Style with CSS modules

3. **SDK Regeneration:**
   - Run `openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o deepwork_sdk`

## Troubleshooting

**Backend won't start:**
- Ensure port 8000 is available
- Check virtual environment is activated
- Verify database exists and is accessible

**Frontend can't connect to backend:**
- Ensure backend is running on port 8000
- Check CORS settings in `main.py`
- Verify network connectivity

**SDK generation fails:**
- Ensure backend is running
- Check OpenAPI Generator CLI is installed
- Verify openapi.json is accessible

**Tests fail:**
- Ensure all dependencies are installed
- Check database permissions
- Verify test isolation

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Acknowledgments

- FastAPI for the excellent backend framework
- React for the powerful UI library
- OpenAPI Generator for seamless SDK generation
- The deep work community for inspiration

