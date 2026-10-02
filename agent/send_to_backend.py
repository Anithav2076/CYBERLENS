import requests

from agent.windows_counters import collect_toniot_features


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000/predict-risk"

SYSTEM_ID = "LIVE-WINDOWS-PC-001"


# ============================================================
# COLLECT LIVE ENDPOINT DATA
# ============================================================

print()
print("========================================")
print(" SENDING LIVE ENDPOINT DATA")
print("========================================")
print()

print("Collecting Windows telemetry...")

observation = collect_toniot_features()

print()
print(f"Collected features: {len(observation)}")


# ============================================================
# CREATE API PAYLOAD
# ============================================================

payload = {
    "system_id": SYSTEM_ID,
    "observation": observation
}


# ============================================================
# SEND TO FASTAPI
# ============================================================

print()
print("Sending data to FastAPI...")
print(f"URL: {API_URL}")

try:

    response = requests.post(
        API_URL,
        json=payload,
        timeout=60
    )

except requests.exceptions.ConnectionError:

    print()
    print("❌ Could not connect to FastAPI.")
    print()
    print("Make sure the backend is running:")
    print()
    print("uvicorn backend.main:app --reload")

    raise SystemExit(1)

except requests.exceptions.Timeout:

    print()
    print("❌ FastAPI request timed out.")

    raise SystemExit(1)


# ============================================================
# DISPLAY RESPONSE
# ============================================================

print()
print("========================================")
print(" BACKEND RESPONSE")
print("========================================")

print("Status code:", response.status_code)

try:

    result = response.json()

    print()
    print(result)

except ValueError:

    print()
    print(response.text)