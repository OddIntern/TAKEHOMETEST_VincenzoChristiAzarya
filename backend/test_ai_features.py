import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:5000"
USERNAME = "admin"
PASSWORD = "123456"

def run_test():
    session = requests.Session()

    # 1. Login to get a fresh token
    print(f"[-] Logging in as {USERNAME}...")
    login_payload = {"username": USERNAME, "password": PASSWORD}
    try:
        response = session.post(f"{BASE_URL}/auth/login", json=login_payload)
        response.raise_for_status()
        data = response.json()
        token = data.get('token')
        print(f"[+] Login Successful! Token acquired.")
    except Exception as e:
        print(f"[!] Login Failed: {e}")
        print(response.text)
        return

    # 2. Test the AI Task Creation
    print("\n[-] Testing AI Auto-Tagging & Priority...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # This text contains triggers: "Urgent" -> High Priority, "bug" -> #bug tag
    task_payload = {
        "title": "Urgent: Fix the login bug by next Friday",
        "description": "System crashes on auth."
    }

    try:
        response = session.post(f"{BASE_URL}/tasks", headers=headers, json=task_payload)
        response.raise_for_status()
        task = response.json()
        
        # 3. Validation
        print(f"[+] Task Created: ID {task['id']}")
        print(f"    Title:    {task['title']}")
        print(f"    Priority: {task['priority']} (Expected: High)")
        print(f"    Tags:     {task['tags']} (Expected: ['bug'] or similar)")
        print(f"    Due Date: {task['due_date']} (Expected: A date string)")
        
        if task['priority'] == 'High' and 'bug' in task['tags']:
            print("\n[SUCCESS] AI Service is working perfectly!")
        else:
            print("\n[WARNING] AI Service logic might need tuning.")
            
    except Exception as e:
        print(f"[!] Task Creation Failed: {e}")
        print(response.text)

if __name__ == "__main__":
    run_test()