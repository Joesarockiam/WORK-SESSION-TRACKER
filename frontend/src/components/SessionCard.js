import React, { useState } from 'react';
import client from '../api/client';
import Timer from './Timer';
import PauseModal from './PauseModal';
import './SessionCard.css';

function SessionCard({ session, onSessionUpdated }) {
  const [showPauseModal, setShowPauseModal] = useState(false);
  const [loading, setLoading] = useState(false);
  // Local optimistic state so UI updates immediately when starting/resuming
  const [localStatus, setLocalStatus] = useState(session.status);
  const [localStartTime, setLocalStartTime] = useState(session.start_time);

  // Sync props -> local state when parent refreshes
  React.useEffect(() => {
    setLocalStatus(session.status);
    setLocalStartTime(session.start_time);
  }, [session.status, session.start_time]);

  const handleStart = async () => {
    setLoading(true);
    try {
      const response = await client.patch(`/sessions/${session.id}/start`);
      console.log('Start successful:', response.data);
      // Optimistically update local UI so buttons appear immediately
      setLocalStatus('active');
      setLocalStartTime(new Date().toISOString());
      // Trigger a refresh in the parent and stop loading so UI updates immediately
      onSessionUpdated();
      setLoading(false);
      // Also refresh after a short delay to ensure timer initializes correctly
      setTimeout(() => {
        onSessionUpdated();
      }, 1000);
    } catch (error) {
      console.error('Failed to start session:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to start session';
      alert(`Failed to start session: ${errorMessage}`);
      setLoading(false);
    }
  };

  const handlePause = async (reason) => {
    if (!reason || !reason.trim()) {
      alert('Please provide a reason for pausing');
      return;
    }
    setLoading(true);
    try {
      console.log('Pausing session:', session.id, 'with reason:', reason);
      const response = await client.patch(`/sessions/${session.id}/pause`, { reason });
      console.log('Pause successful:', response.data);
      // Wait a bit for the database to update, then refresh
      setTimeout(() => {
        onSessionUpdated();
        setLoading(false);
      }, 500);
    } catch (error) {
      console.error('Failed to pause session:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to pause session';
      alert(`Failed to pause session: ${errorMessage}\n\nMake sure:\n1. The session is in 'active' status\n2. The backend is running on http://localhost:8000`);
      setLoading(false);
    }
  };

  const handleResume = async () => {
    setLoading(true);
    try {
      const response = await client.patch(`/sessions/${session.id}/resume`);
      console.log('Resume successful:', response.data);
      onSessionUpdated();
    } catch (error) {
      console.error('Failed to resume session:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to resume session';
      alert(`Failed to resume session: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  const handleComplete = async () => {
    if (!window.confirm('Are you sure you want to complete this session?')) {
      return;
    }
    setLoading(true);
    try {
      await client.patch(`/sessions/${session.id}/complete`);
      onSessionUpdated();
    } catch (error) {
      console.error('Failed to complete session:', error);
      alert('Failed to complete session');
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      scheduled: { text: 'Scheduled', class: 'badge-scheduled' },
      active: { text: 'Active', class: 'badge-active' },
      paused: { text: 'Paused', class: 'badge-paused' },
      completed: { text: 'Completed', class: 'badge-completed' },
      interrupted: { text: 'Interrupted', class: 'badge-interrupted' },
      abandoned: { text: 'Abandoned', class: 'badge-abandoned' },
      overdue: { text: 'Overdue', class: 'badge-overdue' },
    };
    const badge = badges[status] || { text: status, class: 'badge-default' };
    return <span className={`badge ${badge.class}`}>{badge.text}</span>;
  };

  // Debug: Log session status
  console.log('SessionCard rendering with session:', session.id, 'status:', session.status);

  return (
    <div className="session-card">
      <div className="session-header">
        <div className="session-title-section">
          <h2>{session.title}</h2>
          {session.goal && <p className="session-goal">{session.goal}</p>}
        </div>
        {getStatusBadge(session.status)}
      </div>

      <div className="session-content">
        <div className="session-stats">
          <div className="stat-item">
            <span className="stat-label">Duration</span>
            <span className="stat-value">{session.scheduled_duration} min</span>
          </div>
          {session.pause_count > 0 && (
            <div className="stat-item">
              <span className="stat-label">Pauses</span>
              <span className="stat-value">{session.pause_count}</span>
            </div>
          )}
          {session.start_time && (
            <div className="stat-item">
              <span className="stat-label">Started</span>
              <span className="stat-value">
                {(() => {
                  const s = localStartTime || session.start_time;
                  if (!s) return '—';
                  try {
                    // show 12-hour with am/pm in en-IN, then lowercase the am/pm to match design
                    return new Date(s).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', hour12: true, timeZone: 'Asia/Kolkata' }).toLowerCase();
                  } catch (err) {
                    return new Date(s).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                  }
                })()}
              </span>
            </div>
          )}
        </div>

        {(localStartTime || session.start_time) && localStatus === 'active' && (
          <div className="timer-wrapper">
            <Timer
              startTime={localStartTime || session.start_time}
              scheduledDuration={session.scheduled_duration}
              isActive={session.status === 'active'}
            />
          </div>
        )}

        {localStatus === 'scheduled' && (
          <div className="session-ready-message">
            <div className="ready-icon">🎯</div>
            <p>Ready to start your deep work session. Click "Start Session" when you're ready to begin.</p>
          </div>
        )}

        {localStatus === 'paused' && (
          <div className="session-paused-message">
            <div className="paused-icon">⏸️</div>
            <p>Session is paused. Click "Resume" to continue or "Complete" to finish.</p>
          </div>
        )}
      </div>

      <div className="session-actions">
        {localStatus === 'scheduled' && (
          <button onClick={handleStart} disabled={loading} className="btn-primary">
            {loading ? 'Starting...' : 'Start Session'}
          </button>
        )}

        {localStatus === 'active' && (
          <>
            <button 
              onClick={() => {
                console.log('Pause button clicked for session:', session);
                setShowPauseModal(true);
              }} 
              disabled={loading} 
              className="btn-warning"
            >
              {loading ? 'Processing...' : 'Pause'}
            </button>
            <button onClick={handleComplete} disabled={loading} className="btn-success">
              {loading ? 'Processing...' : 'Complete'}
            </button>
          </>
        )}

        {localStatus === 'paused' && (
          <>
            <button onClick={handleResume} disabled={loading} className="btn-primary">
              {loading ? 'Resuming...' : 'Resume'}
            </button>
            <button onClick={handleComplete} disabled={loading} className="btn-success">
              {loading ? 'Processing...' : 'Complete (Abandoned)'}
            </button>
          </>
        )}

        {!['scheduled', 'active', 'paused'].includes(session.status) && (
          <p className="session-info">Session is {session.status}. No actions available.</p>
        )}
      </div>

      <PauseModal
        isOpen={showPauseModal}
        onClose={() => {
          if (!loading) {
            setShowPauseModal(false);
          }
        }}
        onPause={async (reason) => {
          await handlePause(reason);
          setShowPauseModal(false);
        }}
      />
    </div>
  );
}

export default SessionCard;

