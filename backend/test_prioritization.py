import json

from backend.ml.risk_engine import predict_risk
from backend.ml.mitigation_engine import prioritize_mitigations


# Load real cybersecurity observation
with open("backend/test_payload.json", "r") as file:
    observation = json.load(file)


# Calculate current risk
risk_result = predict_risk(observation)

original_risk = risk_result["risk_score"]


# Prioritize mitigations
results = prioritize_mitigations(
    observation,
    original_risk
)


print("\nMITIGATION PRIORITIZATION")
print("=" * 70)

print(f"Current Risk: {original_risk:.2f}")
print(f"Risk Level: {risk_result['risk_level']}")

print("\nPrioritized Mitigations:")
print("-" * 70)


for result in results:

    print(
        f"\nPriority {result['priority']}"
    )

    print(
        f"Feature: {result['feature']}"
    )

    print(
        f"Mitigation: {result['mitigation']}"
    )

    print(
        f"New Risk: {result['new_risk']:.2f}"
    )

    print(
        f"Estimated Reduction: "
        f"{result['estimated_reduction']:.2f}"
    )

    print(
        f"New Risk Level: "
        f"{result['new_risk_level']}"
    )