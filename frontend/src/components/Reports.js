import React, { useEffect, useState } from 'react';
import client from '../api/client';
import './Reports.css';

function Reports() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReport();
  }, []);

  const loadReport = async () => {
    try {
      const response = await client.get('/sessions/report/weekly');
      setReport(response.data);
    } catch (error) {
      console.error('Failed to load report:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExportCSV = async () => {
    try {
      const response = await client.get('/sessions/export/csv');
      const blob = new Blob([response.data.csv_data], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `sessions_${new Date().toISOString().split('T')[0]}.csv`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Failed to export CSV:', error);
      alert('Failed to export data');
    }
  };

  if (loading) {
    return <div className="reports-container">Loading...</div>;
  }

  return (
    <div className="reports-container">
      <div className="reports-header">
        <h2>Weekly Productivity Report</h2>
        <button onClick={handleExportCSV} className="btn-primary">
          Export CSV
        </button>
      </div>

      <div className="report-stats">
        <div className="stat-card">
          <div className="stat-value">{report.total_sessions}</div>
          <div className="stat-label">Total Sessions</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{report.total_focus_time}</div>
          <div className="stat-label">Focus Time (minutes)</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{report.average_focus_score.toFixed(1)}</div>
          <div className="stat-label">Avg Focus Score</div>
        </div>
      </div>

      {report.top_interruption_reason && (
        <div className="report-section">
          <h3>Top Interruption Reason</h3>
          <p className="interruption-reason">{report.top_interruption_reason}</p>
        </div>
      )}

      <div className="report-section">
        <h3>Session Breakdown by Status</h3>
        <div className="status-breakdown">
          {Object.entries(report.focus_breakdown).map(([status, count]) => (
            <div key={status} className="breakdown-item">
              <span className="breakdown-status">{status}</span>
              <span className="breakdown-count">{count}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Reports;

