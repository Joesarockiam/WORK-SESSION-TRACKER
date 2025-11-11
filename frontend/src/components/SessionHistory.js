import React from 'react';
import './SessionHistory.css';

function SessionHistory({ sessions }) {
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

  const formatDate = (dateString) => {
    if (!dateString) return '—';
    const date = new Date(dateString);
    try {
  const datePart = date.toLocaleDateString('en-IN', { timeZone: 'Asia/Kolkata' });
  const timePart = date.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', hour12: true, timeZone: 'Asia/Kolkata' });
  // normalize AM/PM casing to match UI (lowercase)
  return `${datePart} ${timePart.toLowerCase()}`;
    } catch (err) {
      // Fallback
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    }
  };

  return (
    <div className="session-history">
      <h2>Session History</h2>
      {sessions.length === 0 ? (
        <p className="no-sessions">No sessions yet. Schedule your first session to get started!</p>
      ) : (
        <div className="history-table-container">
          <table className="history-table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Goal</th>
                <th>Scheduled</th>
                <th>Actual</th>
                <th>Pauses</th>
                <th>Status</th>
                <th>Completed</th>
              </tr>
            </thead>
            <tbody>
              {sessions.map((session) => (
                <tr key={session.id}>
                  <td>{session.title}</td>
                  <td>{session.goal || '—'}</td>
                  <td>{session.scheduled_duration}m</td>
                  <td>{session.actual_duration ? `${session.actual_duration}m` : '—'}</td>
                  <td>{session.pause_count}</td>
                  <td>{getStatusBadge(session.status)}</td>
                  <td>{formatDate(session.end_time)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default SessionHistory;

