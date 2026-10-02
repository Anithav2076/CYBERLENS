import json

from ml.risk_engine import predict_risk
from ml.mitigation_engine import simulate_mitigation


# ============================================================
# Load test payload
# ============================================================

with open("backend/test_payload.json", "r") as file:
    observation = json.load(file)


# ============================================================
# Calculate original risk
# ============================================================

original_result = predict_risk(observation)

original_risk = original_result["risk_score"]

print("\n===== ORIGINAL RISK =====")
print("Attack Probability:", original_result["attack_probability"])
print("Risk Score:", original_result["risk_score"])
print("Risk Level:", original_result["risk_level"])


# ============================================================
# Test mitigation 1
# ============================================================

result_1 = simulate_mitigation(
    observation,
    "Process_Virtual_Bytes",
    original_risk
)

print("\n===== MITIGATION 1 =====")
print("Mitigation:", result_1["mitigation"])
print("Original Risk:", result_1["original_risk"])
print("New Risk:", result_1["new_risk"])
print("Estimated Reduction:", result_1["estimated_reduction"])
print("New Risk Level:", result_1["new_risk_level"])


# ============================================================
# Test mitigation 2
# ============================================================

result_2 = simulate_mitigation(
    observation,
    "Process_Handle Count",
    original_risk
)

print("\n===== MITIGATION 2 =====")
print("Mitigation:", result_2["mitigation"])
print("Original Risk:", result_2["original_risk"])
print("New Risk:", result_2["new_risk"])
print("Estimated Reduction:", result_2["estimated_reduction"])
print("New Risk Level:", result_2["new_risk_level"])


# ============================================================
# Test mitigation 3
# ============================================================

result_3 = simulate_mitigation(
    observation,
    "Process_Thread Count",
    original_risk
)

print("\n===== MITIGATION 3 =====")
print("Mitigation:", result_3["mitigation"])
print("Original Risk:", result_3["original_risk"])
print("New Risk:", result_3["new_risk"])
print("Estimated Reduction:", result_3["estimated_reduction"])
print("New Risk Level:", result_3["new_risk_level"])