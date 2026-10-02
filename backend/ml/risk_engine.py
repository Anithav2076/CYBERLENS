import os
import joblib
import pandas as pd
import numpy as np
import shap


# ============================================================
# 1. Locate the project root and model directory
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

MODEL_DIR = os.path.join(BASE_DIR, "models")


# ============================================================
# 2. Load saved ML artifacts
# ============================================================

rf_model = joblib.load(
    os.path.join(MODEL_DIR, "random_forest.pkl")
)

calibrated_rf = joblib.load(
    os.path.join(MODEL_DIR, "calibrated_random_forest.pkl")
)

imputer = joblib.load(
    os.path.join(MODEL_DIR, "imputer.pkl")
)

feature_names = joblib.load(
    os.path.join(MODEL_DIR, "feature_names.pkl")
)


# ============================================================
# 3. Calculate risk score and risk level
# ============================================================

def calculate_risk(probability):

    risk_score = probability * 100

    if risk_score < 25:
        risk_level = "LOW"

    elif risk_score < 50:
        risk_level = "MEDIUM"

    elif risk_score < 75:
        risk_level = "HIGH"

    else:
        risk_level = "CRITICAL"

    return risk_score, risk_level


# ============================================================
# 4. Predict cyber risk for one system
# ============================================================

def predict_risk(observation):

    # Convert the incoming observation into a DataFrame
    data = pd.DataFrame([observation])

    # Convert blank values to NaN
    data = data.replace(r"^\s*$", np.nan, regex=True)

    # Arrange columns in exactly the same order
    # used during model training
    data = data.reindex(columns=feature_names)

    # Convert values to numeric
    data = data.apply(pd.to_numeric, errors="coerce")

    # Apply the SAME imputer used during training
    processed_data = imputer.transform(data)

    # Get probability of attack
    attack_probability = calibrated_rf.predict_proba(
        processed_data
    )[0, 1]

    # Convert probability into risk score and level
    risk_score, risk_level = calculate_risk(
        attack_probability
    )

    return {
        "attack_probability": float(attack_probability),
        "risk_score": float(risk_score),
        "risk_level": risk_level
    }


# ============================================================
# 5. Basic verification
# ============================================================

print("ML artifacts loaded successfully.")
print("Number of features:", len(feature_names))

# ==========================================
# SHAP EXPLAINER
# ==========================================

shap_explainer = shap.TreeExplainer(rf_model)

print("SHAP explainer loaded successfully.")

# ==========================================
# 6. Generate SHAP explanation
# ==========================================

def explain_risk(observation, top_n=10):

    # Convert observation into DataFrame
    data = pd.DataFrame([observation])

    # Convert blank values to NaN
    data = data.replace(r"^\s*$", np.nan, regex=True)

    # Arrange columns in the same order as training
    data = data.reindex(columns=feature_names)

    # Convert values to numeric
    data = data.apply(pd.to_numeric, errors="coerce")

    # Apply the same imputer used during training
    processed_data = imputer.transform(data)

    # Convert back to DataFrame so feature names are preserved
    processed_df = pd.DataFrame(
        processed_data,
        columns=feature_names
    )

    # Calculate SHAP values
    shap_values = shap_explainer.shap_values(processed_df)

    # Get SHAP values for attack class
    if isinstance(shap_values, list):
        attack_shap = shap_values[1][0]
    else:
        attack_shap = shap_values[0, :, 1]

    # Create explanation table
    explanation = pd.DataFrame({
        "feature": feature_names,
        "shap_value": attack_shap,
        "feature_value": processed_df.iloc[0].values
    })

    # Absolute SHAP value helps identify strongest contributors
    explanation["absolute_shap"] = (
        explanation["shap_value"].abs()
    )

    # Sort by strongest contribution
    explanation = explanation.sort_values(
        "absolute_shap",
        ascending=False
    )

    # Return only top contributors
    top_features = explanation.head(top_n)

    return top_features[
        ["feature", "shap_value", "feature_value"]
    ].to_dict(orient="records")