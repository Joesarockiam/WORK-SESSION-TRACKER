from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from app import database, schemas
from app.services.session_service import SessionService
import io
import csv

router = APIRouter(prefix="/sessions", tags=["sessions"])

def get_database():
    """Dependency to get database session"""
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.SessionResponse, status_code=201)
async def create_session(
    session: schemas.SessionCreate,
    db: Session = Depends(get_database)
):
    """Schedule a new work session"""
    try:
        new_session = SessionService.create_session(db, session)
        return new_session
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{session_id}/start", response_model=schemas.SessionResponse)
async def start_session(
    session_id: int,
    db: Session = Depends(get_database)
):
    """Start a scheduled session"""
    try:
        print(f"Start request received for session {session_id}")
        session = SessionService.start_session(db, session_id)
        print(f"Session {session_id} started successfully. Status: {session.status}")
        return session
    except ValueError as e:
        print(f"Error starting session {session_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{session_id}/pause", response_model=schemas.SessionResponse)
async def pause_session(
    session_id: int,
    pause_request: schemas.PauseRequest,
    db: Session = Depends(get_database)
):
    """Pause an active session"""
    try:
        print(f"Pause request received for session {session_id} with reason: {pause_request.reason}")
        session = SessionService.pause_session(db, session_id, pause_request.reason)
        print(f"Session {session_id} paused successfully. New status: {session.status}, Pause count: {session.pause_count}")
        return session
    except ValueError as e:
        print(f"Error pausing session {session_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Unexpected error pausing session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.patch("/{session_id}/resume", response_model=schemas.SessionResponse)
async def resume_session(
    session_id: int,
    db: Session = Depends(get_database)
):
    """Resume a paused session"""
    try:
        session = SessionService.resume_session(db, session_id)
        return session
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{session_id}/complete", response_model=schemas.SessionResponse)
async def complete_session(
    session_id: int,
    db: Session = Depends(get_database)
):
    """Mark a session as completed"""
    try:
        session = SessionService.complete_session(db, session_id)
        return session
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/history", response_model=List[schemas.SessionHistory])
async def get_history(db: Session = Depends(get_database)):
    """Get all sessions with stats"""
    history = SessionService.get_session_history(db)
    return history

@router.get("/report/weekly")
async def get_weekly_report(db: Session = Depends(get_database)):
    """Get weekly productivity report with focus score"""
    report = SessionService.get_weekly_report(db)
    return report

@router.get("/export/csv")
async def export_csv(db: Session = Depends(get_database)):
    """Export all sessions to CSV"""
    history = SessionService.get_session_history(db)
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=[
        'id', 'title', 'goal', 'scheduled_duration', 'actual_duration',
        'status', 'pause_count', 'start_time', 'end_time', 'created_at'
    ])
    writer.writeheader()
    
    for session in history:
        writer.writerow(session)
    
    output.seek(0)
    return {
        "csv_data": output.getvalue()
    }

@router.get("/{session_id}/focus-score")
async def get_focus_score(session_id: int, db: Session = Depends(get_database)):
    """Get focus score for a specific session"""
    score = SessionService.calculate_focus_score(db, session_id)
    return {"session_id": session_id, "focus_score": score}

@router.options("/", response_class=Response)
async def options_sessions():
    """Handle CORS preflight requests for /sessions/"""
    return Response(status_code=200)

