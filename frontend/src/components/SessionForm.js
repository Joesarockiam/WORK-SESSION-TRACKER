import React, { useState } from 'react';
import client from '../api/client';
import './SessionForm.css';

function SessionForm({ onSessionCreated }) {
  const [title, setTitle] = useState('');
  const [goal, setGoal] = useState('');
  const [duration, setDuration] = useState(60);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await client.post('/sessions/', {
        title,
        goal,
        scheduled_duration: duration,
      });
      console.log('Session created:', response.data);
      // Clear form
      setTitle('');
      setGoal('');
      setDuration(60);
      // Notify parent to reload sessions
      onSessionCreated();
    } catch (error) {
      console.error('Failed to create session:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to create session';
      alert(`Failed to create session: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="session-form-container">
      <h2>Schedule New Session</h2>
      <form onSubmit={handleSubmit} className="session-form">
        <div className="form-group">
          <label htmlFor="title">Session Title</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            placeholder="e.g., Write project documentation"
          />
        </div>

        <div className="form-group">
          <label htmlFor="goal">Goal</label>
          <input
            type="text"
            id="goal"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            placeholder="What do you want to accomplish?"
          />
        </div>

        <div className="form-group">
          <label htmlFor="duration">Duration (minutes)</label>
          <input
            type="number"
            id="duration"
            value={duration}
            onChange={(e) => setDuration(parseInt(e.target.value))}
            required
            min="1"
          />
        </div>

        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? 'Scheduling...' : 'Schedule Session'}
        </button>
      </form>
    </div>
  );
}

export default SessionForm;

