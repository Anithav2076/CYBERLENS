import json
import requests


# Load the real cybersecurity observation
with open("backend/test_payload.json", "r") as file:
    observation = json.load(file)


# Mitigations we want to compare
features = [
    "Process_Virtual_Bytes",
    "Process_Handle Count",
    "Process_Thread Count"
]


results = []


# Test each mitigation
for feature in features:

    payload = {
        "observation": observation,
        "feature": feature
    }

    response = requests.post(
        "http://127.0.0.1:8000/simulate-mitigation",
        json=payload
    )

    if response.status_code == 200:

        data = response.json()

        simulation = data["mitigation_simulation"]

        results.append({
            "feature": simulation["feature"],
            "original_risk": simulation["original_risk"],
            "new_risk": simulation["new_risk"],
            "estimated_reduction": simulation["estimated_reduction"],
            "new_risk_level": simulation["new_risk_level"]
        })


# Display results
print("\nMITIGATION COMPARISON")
print("=" * 70)

for result in results:

    print(f"\nFeature: {result['feature']}")
    print(f"Original Risk: {result['original_risk']:.2f}")
    print(f"New Risk: {result['new_risk']:.2f}")
    print(f"Estimated Reduction: {result['estimated_reduction']:.2f}")
    print(f"New Risk Level: {result['new_risk_level']}")

print("\n" + "=" * 70)