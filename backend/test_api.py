import json
import requests


# ============================================================
# Load real TON_IoT test payload
# ============================================================

with open(
    "backend/test_payload.json",
    "r",
    encoding="utf-8"
) as file:

    observation = json.load(file)


# ============================================================
# Create API request
# ============================================================

request_body = {

    "system_id": "TEST-PC-001",

    "observation": observation

}


# ============================================================
# Send request to FastAPI
# ============================================================

url = "http://127.0.0.1:8000/predict-risk"

response = requests.post(
    url,
    json=request_body
)


# ============================================================
# Display result
# ============================================================

print()
print("===== CYBER RISK API TEST =====")
print()

print("Status Code:")
print(response.status_code)

print()

print("Response:")

try:

    result = response.json()

    print(result)

except Exception:

    print(response.text)