from backend.database.db import save_observation


test_observation = {
    "system_id": "TEST-PC-001",
    "os": "Windows",
    "source": "test",
    "process_count": 120,
    "timestamp": "2026-09-23T21:00:00"
}

try:
    observation_id = save_observation(test_observation)

    print("✅ Observation saved successfully!")
    print("MongoDB document ID:", observation_id)

except Exception as e:
    print("❌ Failed to save observation!")
    print(e)