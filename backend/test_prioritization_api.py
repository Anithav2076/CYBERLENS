import json
import requests


# Load real cybersecurity observation
with open("backend/test_payload.json", "r") as file:
    observation = json.load(file)


# Send observation to prioritization API
response = requests.post(
    "http://127.0.0.1:8000/prioritize-mitigations",
    json=observation
)


print("Status Code:", response.status_code)

print("\nResponse:")
print(json.dumps(response.json(), indent=4))