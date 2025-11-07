from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.database import Base

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    goal = Column(String)
    scheduled_duration = Column(Integer, nullable=False)  # in minutes
    start_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)
    status = Column(String, 
                   CheckConstraint("status IN ('scheduled', 'active', 'paused', 'completed', 'interrupted', 'abandoned', 'overdue')"),
                   default='scheduled')
    pause_count = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationship to interruptions
    interruptions = relationship("Interruption", back_populates="session", cascade="all, delete-orphan")

class Interruption(Base):
    __tablename__ = "interruptions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    reason = Column(String, nullable=False)
    pause_time = Column(TIMESTAMP, server_default=func.now())
    resume_time = Column(TIMESTAMP)
    
    # Relationship to session
    session = relationship("Session", back_populates="interruptions")

