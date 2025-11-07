"""
Sample script demonstrating the use of Deep Work Session Tracker Python SDK
This script shows how to interact with the API using the generated SDK
"""

import sys
import time

try:
    from deepwork_sdk import Configuration, ApiClient
    from deepwork_sdk.api.sessions_api import SessionsApi
    from deepwork_sdk.model.session_create import SessionCreate
    from deepwork_sdk.model.pause_request import PauseRequest
except ImportError:
    print("Error: SDK not found. Please run 'runapplication.bat' to generate the SDK first.")
    sys.exit(1)

def main():
    # Configure the API client
    configuration = Configuration(
        host="http://localhost:8000"
    )
    
    with ApiClient(configuration) as api_client:
        # Create API instance
        api = SessionsApi(api_client)
        
        print("=" * 50)
        print("Deep Work Session Tracker - SDK Demo")
        print("=" * 50)
        print()
        
        # 1. Create a new session
        print("1. Creating a new session...")
        session_data = SessionCreate(
            title="SDK Demo Session",
            goal="Demonstrate SDK functionality",
            scheduled_duration=25
        )
        session = api.sessions_post(session_data)
        print(f"   Created session ID: {session.id}")
        print(f"   Status: {session.status}")
        print()
        
        # 2. Start the session
        print("2. Starting the session...")
        session = api.sessions_session_id_start_patch(session.id)
        print(f"   Status: {session.status}")
        print()
        
        # 3. Pause the session with a reason
        print("3. Pausing the session...")
        pause_request = PauseRequest(reason="SDK demonstration")
        session = api.sessions_session_id_pause_patch(session.id, pause_request)
        print(f"   Status: {session.status}")
        print(f"   Pause count: {session.pause_count}")
        print()
        
        # 4. Resume the session
        print("4. Resuming the session...")
        session = api.sessions_session_id_resume_patch(session.id)
        print(f"   Status: {session.status}")
        print()
        
        # Wait a moment
        print("5. Working for a few seconds...")
        time.sleep(2)
        
        # 6. Complete the session
        print("6. Completing the session...")
        session = api.sessions_session_id_complete_patch(session.id)
        print(f"   Status: {session.status}")
        print()
        
        # 7. Get session history
        print("7. Fetching session history...")
        history = api.sessions_history_get()
        print(f"   Total sessions: {len(history)}")
        print()
        
        # 8. Get weekly report
        print("8. Fetching weekly productivity report...")
        report = api.sessions_report_weekly_get()
        print(f"   Total sessions this week: {report['total_sessions']}")
        print(f"   Total focus time: {report['total_focus_time']} minutes")
        print(f"   Average focus score: {report['average_focus_score']}")
        print()
        
        # 9. Calculate focus score for our session
        print("9. Calculating focus score for our session...")
        try:
            focus_score = api.sessions_session_id_focus_score_get(session.id)
            print(f"   Focus Score: {focus_score['focus_score']}")
        except Exception as e:
            print(f"   Could not calculate focus score: {e}")
        print()
        
        print("=" * 50)
        print("Demo completed successfully!")
        print("=" * 50)

if __name__ == "__main__":
    main()

