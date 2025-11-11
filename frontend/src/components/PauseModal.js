import React, { useState } from 'react';
import './PauseModal.css';

function PauseModal({ isOpen, onClose, onPause }) {
  const [reason, setReason] = useState('');
  const commonReasons = ['phone call', 'Slack', 'distraction', 'meeting', 'break', 'other'];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (reason.trim()) {
      await onPause(reason);
      setReason('');
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2>Why are you pausing?</h2>
        <form onSubmit={handleSubmit}>
          <div className="reason-buttons">
            {commonReasons.map((r) => (
              <button
                key={r}
                type="button"
                className={`reason-btn ${reason === r ? 'active' : ''}`}
                onClick={() => setReason(r)}
              >
                {r}
              </button>
            ))}
          </div>
          <input
            type="text"
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            placeholder="Or enter your own reason..."
            className="reason-input"
          />
          <div className="modal-actions">
            <button type="button" onClick={onClose} className="btn-secondary">
              Cancel
            </button>
            <button type="submit" disabled={!reason.trim()} className="btn-primary">
              Pause
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default PauseModal;

