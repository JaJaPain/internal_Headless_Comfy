import requests
import json

def get_latest_history():
    try:
        resp = requests.get("http://127.0.0.1:8188/history")
        history = resp.json()
        if not history:
            print("History is empty")
            return
        
        # Sort by timestamp in status messages if possible, or just latest key
        latest_id = list(history.keys())[-1]
        latest = history[latest_id]
        print(f"Latest Prompt ID: {latest_id}")
        
        status = latest.get("status", {})
        messages = status.get("messages", [])
        for msg in messages:
            if msg[0] == "execution_error":
                print(f"Error: {msg[1].get('exception_message')}")
                print(f"Node: {msg[1].get('node_id')} ({msg[1].get('node_type')})")
                print("Traceback:")
                for line in msg[1].get('traceback', []):
                    print(line)
            elif msg[0] == "execution_success":
                print("Execution SUCCESS!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_latest_history()
