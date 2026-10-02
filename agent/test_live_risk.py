from agent.windows_counters import collect_toniot_features
from backend.ml.risk_engine import (
    predict_risk,
    explain_risk
)


print()
print("========================================")
print(" LIVE ENDPOINT RISK TEST")
print("========================================")
print()


# ------------------------------------------------------------
# 1. Collect live Windows telemetry
# ------------------------------------------------------------

print("Collecting live endpoint data...")

observation = collect_toniot_features()


print()
print("Live features collected:", len(observation))


# ------------------------------------------------------------
# 2. Predict risk
# ------------------------------------------------------------

print()
print("Running risk prediction...")

risk_result = predict_risk(observation)


print()
print("========================================")
print(" RISK RESULT")
print("========================================")

print(
    "Attack probability:",
    risk_result["attack_probability"]
)

print(
    "Risk score:",
    risk_result["risk_score"]
)

print(
    "Risk level:",
    risk_result["risk_level"]
)


# ------------------------------------------------------------
# 3. SHAP explanation
# ------------------------------------------------------------

print()
print("Generating SHAP explanation...")

shap_results = explain_risk(
    observation,
    top_n=10
)


print()
print("========================================")
print(" TOP SHAP FEATURES")
print("========================================")

for item in shap_results:

    print(
        f"{item['feature']} | "
        f"SHAP={item['shap_value']:.6f} | "
        f"Value={item['feature_value']}"
    )


print()
print("========================================")
print(" LIVE RISK TEST COMPLETE")
print("========================================")