-- Seed data for Deep Work Session Tracker
-- This file contains sample sessions for testing

-- Session A: 50 minutes, paused 2× → status: completed
INSERT INTO sessions (title, goal, scheduled_duration, status, pause_count, created_at) 
VALUES ('Write project doc', 'Finish outline', 50, 'scheduled', 0, datetime('now', '-5 days'));

-- Update Session A to be completed
UPDATE sessions SET status = 'completed', start_time = datetime('now', '-5 days', '+1 hour'), end_time = datetime('now', '-5 days', '+1 hour', '+52 minutes'), pause_count = 2 WHERE title = 'Write project doc';

-- Add interruptions for Session A
INSERT INTO interruptions (session_id, reason, pause_time, resume_time) VALUES 
(1, 'phone call', datetime('now', '-5 days', '+1 hour', '+25 minutes'), datetime('now', '-5 days', '+1 hour', '+30 minutes')),
(1, 'Slack message', datetime('now', '-5 days', '+1 hour', '+40 minutes'), datetime('now', '-5 days', '+1 hour', '+42 minutes'));

-- Session B: paused 4× → status: interrupted
INSERT INTO sessions (title, goal, scheduled_duration, status, pause_count, created_at) 
VALUES ('Code review', 'Review PR #123', 60, 'scheduled', 0, datetime('now', '-4 days'));

UPDATE sessions SET status = 'interrupted', start_time = datetime('now', '-4 days', '+2 hours'), pause_count = 4 WHERE title = 'Code review';

INSERT INTO interruptions (session_id, reason, pause_time, resume_time) VALUES 
(2, 'distraction', datetime('now', '-4 days', '+2 hours', '+10 minutes'), datetime('now', '-4 days', '+2 hours', '+15 minutes')),
(2, 'phone call', datetime('now', '-4 days', '+2 hours', '+20 minutes'), datetime('now', '-4 days', '+2 hours', '+25 minutes')),
(2, 'Slack', datetime('now', '-4 days', '+2 hours', '+30 minutes'), datetime('now', '-4 days', '+2 hours', '+32 minutes')),
(2, 'distraction', datetime('now', '-4 days', '+2 hours', '+35 minutes'), NULL);

-- Session C: not resumed after pause → status: abandoned
INSERT INTO sessions (title, goal, scheduled_duration, status, pause_count, created_at) 
VALUES ('Design UI', 'Complete wireframes', 45, 'abandoned', 1, datetime('now', '-3 days'));

UPDATE sessions SET start_time = datetime('now', '-3 days', '+3 hours'), end_time = datetime('now', '-2 days') WHERE title = 'Design UI';

INSERT INTO interruptions (session_id, reason, pause_time, resume_time) VALUES 
(3, 'urgent meeting', datetime('now', '-3 days', '+3 hours', '+25 minutes'), NULL);

-- Session D: completed 60 minutes after 50-minute duration → status: overdue
INSERT INTO sessions (title, goal, scheduled_duration, status, pause_count, created_at) 
VALUES ('Fix bugs', 'Resolve critical issues', 50, 'overdue', 1, datetime('now', '-2 days'));

UPDATE sessions SET start_time = datetime('now', '-2 days', '+4 hours'), end_time = datetime('now', '-2 days', '+4 hours', '+60 minutes'), pause_count = 1 WHERE title = 'Fix bugs';

INSERT INTO interruptions (session_id, reason, pause_time, resume_time) VALUES 
(4, 'team sync', datetime('now', '-2 days', '+4 hours', '+30 minutes'), datetime('now', '-2 days', '+4 hours', '+35 minutes'));

-- A few more active/scheduled sessions for current testing
INSERT INTO sessions (title, goal, scheduled_duration, status, pause_count, created_at) 
VALUES 
('API Documentation', 'Document endpoints', 90, 'scheduled', 0, datetime('now', '-1 day')),
('Database optimization', 'Improve query performance', 120, 'scheduled', 0, datetime('now', '-6 hours')),
('Code refactoring', 'Clean up legacy code', 45, 'active', 0, datetime('now', '-2 hours'));

UPDATE sessions SET start_time = datetime('now', '-2 hours') WHERE title = 'Code refactoring';

