import json
import requests


# Load the real 124-feature test observation
with open("backend/test_payload.json", "r") as file:
    observation = json.load(file)


# Select the mitigation to simulate
payload = {
    "observation": observation,
    "feature": "Process_Handle Count"
}


# Send request to FastAPI
response = requests.post(
    "http://127.0.0.1:8000/simulate-mitigation",
    json=payload
)


print("Status Code:", response.status_code)

print("\nResponse:")
print(json.dumps(response.json(), indent=4))