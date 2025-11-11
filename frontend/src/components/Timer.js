import React, { useState, useEffect, useRef } from 'react';
import './Timer.css';

function Timer({ startTime, scheduledDuration, isActive, onComplete }) {
  const [timeRemaining, setTimeRemaining] = useState(null);
  const [elapsedTime, setElapsedTime] = useState(0);
  const intervalRef = useRef(null);

  useEffect(() => {
    if (!startTime || !isActive) {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
      setTimeRemaining(null);
      setElapsedTime(0);
      return;
    }

    // Helper: parse incoming startTime robustly. Backend may send naive ISO strings.
    const parseStartTime = (s) => {
      if (!s) return null;
      if (s instanceof Date) return s;
      try {
        // If string contains timezone info (Z or +HH:MM / -HH:MM), trust it
        if (typeof s === 'string' && /[Zz]|[+\-]\d{2}:?\d{2}$/.test(s)) {
          return new Date(s);
        }
        // Otherwise append 'Z' to treat the timestamp as UTC (backend uses UTC)
        if (typeof s === 'string') return new Date(s + 'Z');
        return new Date(s);
      } catch (err) {
        console.error('Failed to parse start time:', s, err);
        return null;
      }
    };

    const updateTimer = () => {
      try {
        const nowMs = Date.now();
        const startDate = parseStartTime(startTime);

        if (!startDate || isNaN(startDate.getTime())) {
          console.error('Invalid start time:', startTime);
          return;
        }

        // Use millisecond arithmetic and convert to seconds for display
        const elapsedSeconds = Math.floor((nowMs - startDate.getTime()) / 1000);
        const totalSeconds = Number(scheduledDuration) * 60;
        const remainingSeconds = Math.max(0, totalSeconds - elapsedSeconds);

        setElapsedTime(elapsedSeconds);
        setTimeRemaining(remainingSeconds);

        if (remainingSeconds <= 0) {
          if (intervalRef.current) clearInterval(intervalRef.current);
          onComplete && onComplete();
        }
      } catch (error) {
        console.error('Error updating timer:', error);
      }
    };

    // Update immediately
    updateTimer();
    
    // Then update every second
    intervalRef.current = setInterval(updateTimer, 1000);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [startTime, scheduledDuration, isActive, onComplete]);

  const formatTime = (totalSeconds) => {
    if (totalSeconds === null || totalSeconds === undefined || isNaN(totalSeconds)) {
      return '00:00';
    }
    const minutes = Math.floor(Math.max(0, totalSeconds) / 60);
    const seconds = Math.floor(Math.max(0, totalSeconds) % 60);
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  };

  const getProgress = () => {
    if (timeRemaining === null || scheduledDuration === 0) return 0;
    const totalSeconds = scheduledDuration * 60;
    return ((totalSeconds - timeRemaining) / totalSeconds) * 100;
  };

  const progress = getProgress();
  const circumference = 2 * Math.PI * 45; // radius is 45
  const strokeDashoffset = circumference - (progress / 100) * circumference;
  
  // Determine timer color based on remaining time
  const getTimerColor = () => {
    if (timeRemaining === null) return '#4caf50';
    const totalSeconds = scheduledDuration * 60;
    const percentRemaining = (timeRemaining / totalSeconds) * 100;
    if (percentRemaining <= 10) return '#f44336'; // Red for < 10%
    if (percentRemaining <= 25) return '#ff9800'; // Orange for < 25%
    return '#4caf50'; // Green for > 25%
  };

  const timerColor = getTimerColor();

  return (
    <div className="timer-container">
      <div className="timer-display">
        <div className="timer-circle">
          <svg className="timer-svg" viewBox="0 0 100 100">
            <circle
              className="timer-bg"
              cx="50"
              cy="50"
              r="45"
            />
            <circle
              className="timer-progress"
              cx="50"
              cy="50"
              r="45"
              style={{
                strokeDasharray: circumference,
                strokeDashoffset: strokeDashoffset,
                stroke: timerColor,
              }}
            />
          </svg>
          <div className="timer-text">
            <div className="timer-main" style={{ color: timerColor }}>{formatTime(timeRemaining)}</div>
            <div className="timer-label">remaining</div>
            {elapsedTime > 0 && (
              <div className="timer-elapsed">Elapsed: {formatTime(elapsedTime)}</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Timer;

