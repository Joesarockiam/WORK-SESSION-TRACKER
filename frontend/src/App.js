import React, { useState, useEffect } from 'react';
import SessionForm from './components/SessionForm';
import SessionCard from './components/SessionCard';
import SessionHistory from './components/SessionHistory';
import Reports from './components/Reports';
import './App.css';

function App() {
  const [sessions, setSessions] = useState([]);
  const [activeSession, setActiveSession] = useState(null);
  const [showHistory, setShowHistory] = useState(false);
  const [showReports, setShowReports] = useState(false);

  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    try {
      const client = (await import('./api/client')).default;
      const response = await client.get('/sessions/history');
      console.log('Loaded sessions:', response.data);
      setSessions(response.data);
      
      // Find the most recent session that can be controlled (scheduled, active, or paused)
      // Priority: active > paused > scheduled (most recent)
      const active = response.data.find(s => s.status === 'active');
      const paused = response.data.find(s => s.status === 'paused');
      const scheduled = response.data
        .filter(s => s.status === 'scheduled')
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))[0];
      
      const currentSession = active || paused || scheduled || null;
      console.log('Current session found:', currentSession);
      setActiveSession(currentSession);
    } catch (error) {
      console.error('Failed to load sessions:', error);
      alert(`Failed to load sessions: ${error.message}. Make sure the backend is running on http://localhost:8000`);
    }
  };

  const handleSessionCreated = (newSession) => {
    loadSessions();
  };

  const handleSessionUpdated = () => {
    loadSessions();
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Deep Work Session Tracker</h1>
        <nav>
          <button 
            className={!showHistory && !showReports ? 'active' : ''}
            onClick={() => { setShowHistory(false); setShowReports(false); }}
          >
            Sessions
          </button>
          <button 
            className={showHistory ? 'active' : ''}
            onClick={() => { setShowHistory(true); setShowReports(false); }}
          >
            History
          </button>
          <button 
            className={showReports ? 'active' : ''}
            onClick={() => { setShowHistory(false); setShowReports(true); }}
          >
            Reports
          </button>
        </nav>
      </header>

      <main className="App-main">
        {showReports ? (
          <Reports />
        ) : showHistory ? (
          <SessionHistory sessions={sessions} />
        ) : (
          <>
            {activeSession ? (
              <SessionCard 
                session={activeSession} 
                onSessionUpdated={handleSessionUpdated}
              />
            ) : (
              <SessionForm onSessionCreated={handleSessionCreated} />
            )}
            <SessionHistory 
              sessions={sessions.filter(s => 
                s.status !== 'active' && 
                s.status !== 'paused' && 
                s.status !== 'scheduled'
              )} 
            />
          </>
        )}
      </main>
    </div>
  );
}

export default App;
