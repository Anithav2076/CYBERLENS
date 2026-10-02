import requests
import json


API_URL = "http://127.0.0.1:8000/prioritize-mitigations"


# Load the real TON_IoT test observation
with open("backend/test_payload.json", "r") as file:
    observation = json.load(file)


# The API expects:
# system_id
# observation
request_body = {
    "system_id": "TEST-PC-001",
    "observation": observation
}


response = requests.post(
    API_URL,
    json=request_body
)


print("Status Code:", response.status_code)

print("\nResponse:")

try:
    print(
        json.dumps(
            response.json(),
            indent=4
        )
    )

except Exception:
    print(response.text)