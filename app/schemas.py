from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

# Session Schemas
class SessionBase(BaseModel):
    title: str
    goal: Optional[str] = None
    scheduled_duration: int = Field(..., gt=0, description="Duration in minutes")

class SessionCreate(SessionBase):
    pass

class SessionResponse(SessionBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    status: str
    pause_count: int
    created_at: datetime

class SessionHistory(SessionResponse):
    actual_duration: Optional[int] = None  # in minutes

# Interruption Schemas
class InterruptionCreate(BaseModel):
    reason: str

class InterruptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    reason: str
    pause_time: datetime
    resume_time: Optional[datetime]

# Pause Request
class PauseRequest(BaseModel):
    reason: str

# History Response
class HistoryResponse(BaseModel):
    total_sessions: int
    completed_sessions: int
    interrupted_sessions: int
    abandoned_sessions: int
    overdue_sessions: int
    sessions: List[SessionHistory]

# Report Response
class WeeklyReport(BaseModel):
    week_start: datetime
    total_sessions: int
    total_focus_time: int  # minutes
    average_focus_score: float
    top_interruption_reason: Optional[str]
    focus_breakdown: dict

# CSV Export
class ExportRequest(BaseModel):
    format: str = "csv"

