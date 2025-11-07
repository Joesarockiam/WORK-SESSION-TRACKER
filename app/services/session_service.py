from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import Session as SessionModel, Interruption
from app import schemas

class SessionService:
    
    @staticmethod
    def create_session(db: Session, session_data: schemas.SessionCreate) -> SessionModel:
        """Create a new scheduled session"""
        db_session = SessionModel(**session_data.model_dump())
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session
    
    @staticmethod
    def start_session(db: Session, session_id: int) -> SessionModel:
        """Start a scheduled session"""
        db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not db_session:
            raise ValueError("Session not found")
        
        if db_session.status != 'scheduled':
            raise ValueError(f"Cannot start session with status: {db_session.status}")
        
        db_session.status = 'active'
        db_session.start_time = datetime.utcnow()
        db.commit()
        db.refresh(db_session)
        return db_session
    
    @staticmethod
    def pause_session(db: Session, session_id: int, reason: str) -> SessionModel:
        """Pause an active session"""
        db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not db_session:
            raise ValueError("Session not found")
        
        if db_session.status != 'active':
            raise ValueError(f"Cannot pause session with status: {db_session.status}")
        
        # Create interruption record
        interruption = Interruption(
            session_id=session_id,
            reason=reason,
            pause_time=datetime.utcnow()
        )
        db.add(interruption)
        
        # Update session
        db_session.status = 'paused'
        db_session.pause_count += 1
        
        # Check if exceeded 3 pauses
        if db_session.pause_count > 3:
            db_session.status = 'interrupted'
        
        db.commit()
        db.refresh(db_session)
        return db_session
    
    @staticmethod
    def resume_session(db: Session, session_id: int) -> SessionModel:
        """Resume a paused session"""
        db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not db_session:
            raise ValueError("Session not found")
        
        if db_session.status not in ['paused', 'abandoned']:
            raise ValueError(f"Cannot resume session with status: {db_session.status}")
        
        # Update the most recent interruption with resume time
        interruption = db.query(Interruption).filter(
            Interruption.session_id == session_id,
            Interruption.resume_time.is_(None)
        ).order_by(Interruption.pause_time.desc()).first()
        
        if interruption:
            interruption.resume_time = datetime.utcnow()
        
        # Change status back to active
        db_session.status = 'active'
        db.commit()
        db.refresh(db_session)
        return db_session
    
    @staticmethod
    def complete_session(db: Session, session_id: int) -> SessionModel:
        """Complete a session"""
        db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not db_session:
            raise ValueError("Session not found")
        
        if db_session.status not in ['active', 'paused']:
            raise ValueError(f"Cannot complete session with status: {db_session.status}")
        
        now = datetime.utcnow()
        db_session.end_time = now
        
        # Check for abandoned sessions (paused but never resumed)
        initial_status = db_session.status
        if initial_status == 'paused':
            db_session.status = 'abandoned'
        else:
            db_session.status = 'completed'
        
        # Check if overdue (exceeded scheduled duration by more than 10%)
        if db_session.start_time:
            actual_duration = (now - db_session.start_time).total_seconds() / 60
            max_acceptable = db_session.scheduled_duration * 1.1
            
            if actual_duration > max_acceptable:
                db_session.status = 'overdue'
        
        db.commit()
        db.refresh(db_session)
        return db_session
    
    @staticmethod
    def get_session_history(db: Session) -> list:
        """Get all sessions with calculated stats"""
        sessions = db.query(SessionModel).order_by(SessionModel.created_at.desc()).all()
        
        history = []
        for session in sessions:
            session_dict = {
                "id": session.id,
                "title": session.title,
                "goal": session.goal,
                "scheduled_duration": session.scheduled_duration,
                "start_time": session.start_time,
                "end_time": session.end_time,
                "status": session.status,
                "pause_count": session.pause_count,
                "created_at": session.created_at,
                "actual_duration": None
            }
            
            # Calculate actual duration if completed
            if session.start_time and session.end_time:
                duration = (session.end_time - session.start_time).total_seconds() / 60
                session_dict["actual_duration"] = int(duration)
            
            history.append(session_dict)
        
        return history
    
    @staticmethod
    def calculate_focus_score(db: Session, session_id: int) -> float:
        """Calculate focus score for a session"""
        session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not session:
            return 0.0
        
        # Base completion ratio
        completion_ratio = 1.0 if session.status == 'completed' else 0.5
        
        # Interruption penalty
        interruption_penalty = min(session.pause_count / session.scheduled_duration, 1.0) if session.scheduled_duration > 0 else 0
        
        # Focus score formula
        focus_score = (1 - interruption_penalty) * completion_ratio * 100
        return round(max(0, min(100, focus_score)), 2)
    
    @staticmethod
    def get_weekly_report(db: Session) -> dict:
        """Generate weekly productivity report"""
        from sqlalchemy import func
        
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        recent_sessions = db.query(SessionModel).filter(
            SessionModel.created_at >= week_ago
        ).all()
        
        if not recent_sessions:
            return {
                "week_start": week_ago,
                "total_sessions": 0,
                "total_focus_time": 0,
                "average_focus_score": 0.0,
                "top_interruption_reason": None,
                "focus_breakdown": {}
            }
        
        total_focus_time = 0
        focus_scores = []
        interruption_reasons = []
        
        for session in recent_sessions:
            if session.start_time and session.end_time:
                duration = (session.end_time - session.start_time).total_seconds() / 60
                total_focus_time += int(duration)
            
            score = SessionService.calculate_focus_score(db, session.id)
            focus_scores.append(score)
            
            # Collect interruption reasons
            for interruption in session.interruptions:
                interruption_reasons.append(interruption.reason)
        
        # Find top interruption reason
        top_reason = None
        if interruption_reasons:
            from collections import Counter
            top_reason = Counter(interruption_reasons).most_common(1)[0][0]
        
        # Focus breakdown by status
        focus_breakdown = {}
        for session in recent_sessions:
            status = session.status
            focus_breakdown[status] = focus_breakdown.get(status, 0) + 1
        
        return {
            "week_start": week_ago,
            "total_sessions": len(recent_sessions),
            "total_focus_time": total_focus_time,
            "average_focus_score": round(sum(focus_scores) / len(focus_scores), 2) if focus_scores else 0,
            "top_interruption_reason": top_reason,
            "focus_breakdown": focus_breakdown
        }

