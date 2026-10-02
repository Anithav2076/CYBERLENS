from datetime import datetime, timezone

from backend.database.db import save_risk_assessment


test_assessment = {
    "system_id": "TEST-PC-001",
    "attack_probability": 0.997153,
    "risk_score": 99.72,
    "risk_level": "CRITICAL",
    "model_version": "random_forest_v1",
    "timestamp": datetime.now(timezone.utc),
}

try:
    assessment_id = save_risk_assessment(test_assessment)

    print("✅ Risk assessment saved successfully!")
    print("MongoDB document ID:", assessment_id)

except Exception as e:
    print("❌ Failed to save risk assessment!")
    print(e)