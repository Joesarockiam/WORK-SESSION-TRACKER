# Debugging Pause Issue - Step by Step Guide

## Issue: Cannot pause sessions

Follow these steps to identify and fix the problem:

## Step 1: Verify Backend is Running

1. Open a browser and go to: http://localhost:8000
2. You should see: `{"message":"Deep Work Session Tracker API","docs":"/docs","openapi":"/openapi.json"}`
3. If you see an error, the backend is not running. Start it with:
   ```bash
   call env\Scripts\activate.bat
   python main.py
   ```

## Step 2: Check Backend API Documentation

1. Go to: http://localhost:8000/docs
2. This is the Swagger UI where you can test endpoints directly
3. Try the pause endpoint:
   - Find `PATCH /sessions/{session_id}/pause`
   - Click "Try it out"
   - Enter a session ID (you can get this from the history endpoint)
   - Enter a reason in the request body: `{"reason": "test"}`
   - Click "Execute"
   - Check if it works

## Step 3: Check Frontend Console

1. Open the frontend in your browser (http://localhost:3000)
2. Open Developer Tools (F12)
3. Go to the Console tab
4. Try to pause a session
5. Look for error messages - they will tell you exactly what's wrong

## Step 4: Verify Session Status

The pause button only appears when the session status is 'active'. 

1. After starting a session, check the console logs
2. You should see: "SessionCard rendering with session: X status: active"
3. If the status is still 'scheduled', the start didn't work properly

## Step 5: Test the Flow Manually

1. **Create a session** - Should work (you said this works)
2. **Start the session** - Check console for "Start successful"
3. **Wait 1 second** - Let the status update
4. **Click Refresh button** - Manually refresh the session
5. **Check status** - Should now show "Active" badge
6. **Click Pause** - Should open the modal
7. **Enter reason and submit** - Check console for errors

## Common Issues and Solutions

### Issue 1: "Cannot pause session with status: scheduled"
**Solution:** The session wasn't started. Make sure you click "Start Session" first and wait for it to complete.

### Issue 2: "Failed to pause session: Network Error"
**Solution:** Backend is not running. Start it with `python main.py`

### Issue 3: "CORS error"
**Solution:** Make sure the backend CORS is configured correctly (it should be in main.py)

### Issue 4: Pause button doesn't appear
**Solution:** 
- Check the session status in console logs
- Make sure the session is 'active', not 'scheduled'
- Try clicking the Refresh button

### Issue 5: Modal opens but pause doesn't work
**Solution:**
- Check browser console for the exact error
- Make sure you entered a reason
- Check that the backend received the request (check backend terminal)

## Quick Test Script

Run this in your browser console (F12) to test the API directly:

```javascript
// Test creating a session
fetch('http://localhost:8000/sessions/', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    title: 'Test Session',
    goal: 'Test pause',
    scheduled_duration: 30
  })
})
.then(r => r.json())
.then(data => {
  console.log('Created session:', data);
  const sessionId = data.id;
  
  // Start the session
  return fetch(`http://localhost:8000/sessions/${sessionId}/start`, {
    method: 'PATCH'
  });
})
.then(r => r.json())
.then(data => {
  console.log('Started session:', data);
  const sessionId = data.id;
  
  // Pause the session
  return fetch(`http://localhost:8000/sessions/${sessionId}/pause`, {
    method: 'PATCH',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({reason: 'test pause'})
  });
})
.then(r => r.json())
.then(data => {
  console.log('Paused session:', data);
})
.catch(err => {
  console.error('Error:', err);
});
```

If this script works, the backend is fine and the issue is in the frontend. If it doesn't work, the issue is in the backend.

## Still Having Issues?

1. Check the backend terminal for error messages
2. Check the browser console for error messages
3. Verify both backend (port 8000) and frontend (port 3000) are running
4. Try the manual test script above
5. Check that the session status is actually 'active' before trying to pause

