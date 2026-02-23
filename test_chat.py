import requests
import json

url = "http://127.0.0.1:5000/api/chat"
headers = {"Content-Type": "application/json"}
data = {"message": "Who are you?"}

try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
