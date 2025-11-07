import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.models import Base
from app.services.session_service import SessionService
from app import schemas

# Test database
TEST_DATABASE_URL = "sqlite:///./test_deep_work.db"

@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test"""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()
        Base.metadata.drop_all(bind=engine)
        try:
            os.remove("test_deep_work.db")
        except:
            pass

def test_create_session(db):
    """Test creating a new session"""
    session_data = schemas.SessionCreate(
        title="Test Session",
        goal="Test goal",
        scheduled_duration=60
    )
    session = SessionService.create_session(db, session_data)
    
    assert session.id is not None
    assert session.title == "Test Session"
    assert session.status == "scheduled"

def test_start_session(db):
    """Test starting a scheduled session"""
    session_data = schemas.SessionCreate(title="Test", goal="Goal", scheduled_duration=60)
    session = SessionService.create_session(db, session_data)
    
    started = SessionService.start_session(db, session.id)
    assert started.status == "active"
    assert started.start_time is not None

def test_start_invalid_status(db):
    """Test starting a session that's already active"""
    session_data = schemas.SessionCreate(title="Test", goal="Goal", scheduled_duration=60)
    session = SessionService.create_session(db, session_data)
    SessionService.start_session(db, session.id)
    
    with pytest.raises(ValueError, match="Cannot start session"):
        SessionService.start_session(db, session.id)

def test_pause_session(db):
    """Test pausing an active session"""
    session_data = schemas.SessionCreate(title="Test", goal="Goal", scheduled_duration=60)
    session = SessionService.create_session(db, session_data)
    SessionService.start_session(db, session.id)
    
    paused = SessionService.pause_session(db, session.id, "Test reason")
    assert paused.status == "paused"
    assert paused.pause_count == 1

def test_pause_limit_exceeded(db):
    """Test that session becomes interrupted after 3 pauses"""
    session_data = schemas.SessionCreate(title="Test", goal="Goal", scheduled_duration=60)
    session = SessionService.create_session(db, session_data)
    SessionService.start_session(db, session.id)
    
    # Pause 4 times
    for i in range(4):
        SessionService.pause_session(db, session.id, f"Reason {i}")
        if i < 3:
            SessionService.resume_session(db, session.id)
    
    db.refresh(session)
    assert session.status == "interrupted"
    assert session.pause_count == 4

def test_resume_session(db):
    """Test resuming a paused session"""
    session_data = schemas.SessionCreate(title="Test", goal="Goal", scheduled_duration=60)
    session = SessionService.create_session(db, session_data)
    SessionService.start_session(db, session.id)
    SessionService.pause_session(db, session.id, "Test reason")
    
    resumed = SessionService.resume_session(db, session.id)
    assert resumed.status == "active"

def test_complete_session(db):
    """Test completing a session"""
    session_data = schemas.SessionCreate(title="Test", goal="Goal", scheduled_duration=60)
    session = SessionService.create_session(db, session_data)
    SessionService.start_session(db, session.id)
    
    completed = SessionService.complete_session(db, session.id)
    assert completed.status == "completed"
    assert completed.end_time is not None

def test_complete_abandoned_session(db):
    """Test completing a paused session marks it as abandoned"""
    session_data = schemas.SessionCreate(title="Test", goal="Goal", scheduled_duration=60)
    session = SessionService.create_session(db, session_data)
    SessionService.start_session(db, session.id)
    SessionService.pause_session(db, session.id, "Test reason")
    
    completed = SessionService.complete_session(db, session.id)
    assert completed.status == "abandoned"

def test_complete_overdue_session(db):
    """Test that overdue sessions are marked correctly"""
    session_data = schemas.SessionCreate(title="Test", goal="Goal", scheduled_duration=50)
    session = SessionService.create_session(db, session_data)
    SessionService.start_session(db, session.id)
    
    # Manually set start time to 60 minutes ago to simulate overtime
    from app.models import Session as SessionModel
    session_model = db.query(SessionModel).filter(SessionModel.id == session.id).first()
    session_model.start_time = datetime.utcnow() - timedelta(minutes=60)
    db.commit()
    
    completed = SessionService.complete_session(db, session.id)
    assert completed.status == "overdue"

def test_cannot_pause_before_start(db):
    """Test validation: cannot pause a scheduled session"""
    session_data = schemas.SessionCreate(title="Test", goal="Goal", scheduled_duration=60)
    session = SessionService.create_session(db, session_data)
    
    with pytest.raises(ValueError, match="Cannot pause session"):
        SessionService.pause_session(db, session.id, "Test")

def test_get_history(db):
    """Test getting session history"""
    # Create a few sessions
    for i in range(3):
        session_data = schemas.SessionCreate(
            title=f"Session {i}",
            goal="Goal",
            scheduled_duration=60
        )
        SessionService.create_session(db, session_data)
    
    history = SessionService.get_session_history(db)
    assert len(history) == 3

def test_focus_score_calculation(db):
    """Test focus score calculation"""
    session_data = schemas.SessionCreate(title="Test", goal="Goal", scheduled_duration=60)
    session = SessionService.create_session(db, session_data)
    SessionService.start_session(db, session.id)
    SessionService.complete_session(db, session.id)
    
    score = SessionService.calculate_focus_score(db, session.id)
    assert score == 100  # No interruptions, completed

def test_weekly_report(db):
    """Test weekly report generation"""
    # Create a session within the last week
    session_data = schemas.SessionCreate(title="Test", goal="Goal", scheduled_duration=60)
    session = SessionService.create_session(db, session_data)
    SessionService.start_session(db, session.id)
    SessionService.complete_session(db, session.id)
    
    report = SessionService.get_weekly_report(db)
    assert report["total_sessions"] > 0
    assert "average_focus_score" in report

