import os
import pandas as pd

from ml.risk_engine import predict_risk, explain_risk


# Locate dataset
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "datasets",
    "windows",
    "Train_Test_Windows_10.csv"
)


# Load the real TON_IoT dataset
df = pd.read_csv(DATASET_PATH)


# Select one real system record
sample = df.iloc[0]


# Keep only the ML features
observation = sample.drop(
    labels=["label", "type"]
).to_dict()


# Predict cyber risk
result = predict_risk(observation)


# Display results
print("\n===== CYBER RISK PREDICTION =====")

print("Actual Label:", sample["label"])
print("Attack Type:", sample["type"])

print(
    "Attack Probability:",
    round(result["attack_probability"], 6)
)

print(
    "Risk Score:",
    round(result["risk_score"], 2)
)

print(
    "Risk Level:",
    result["risk_level"]
)

print("\n===== SHAP EXPLANATION =====")

explanation = explain_risk(observation, top_n=10)

for item in explanation:
    print(
        item["feature"],
        "=> SHAP:",
        round(item["shap_value"], 6),
        "| Value:",
        item["feature_value"]
    )
    
    print("\n===== SHAP EXPLANATION =====")

for item in explanation:
    print(
        item["feature"],
        "=> SHAP:",
        round(item["shap_value"], 6),
        "| Value:",
        item["feature_value"]
    )