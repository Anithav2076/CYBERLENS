import pandas as pd

from backend.ml.risk_engine import (
    calibrated_rf,
    feature_names
)


# ============================================================
# Mitigation simulation library
# ============================================================

MITIGATION_LIBRARY = {

    "Process_Virtual_Bytes": {
        "mitigation":
            "Reduce Process_Virtual_Bytes by 20%",

        "reduction_factor": 0.80,

        "security_rationale":
            "Investigate processes consuming unusually large "
            "virtual memory and review unexpected resource usage."
    },

    "Process_Handle Count": {
        "mitigation":
            "Reduce Process_Handle Count by 20%",

        "reduction_factor": 0.80,

        "security_rationale":
            "Investigate processes with unusually high handle "
            "counts and review abnormal process behavior."
    },

    "Process_Thread Count": {
        "mitigation":
            "Reduce Process_Thread Count by 20%",

        "reduction_factor": 0.80,

        "security_rationale":
            "Investigate processes with unusually high thread "
            "counts and review unexpected process activity."
    }
}


# ============================================================
# Calculate risk
# ============================================================

def calculate_risk_from_probability(probability):

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
# Simulate one mitigation
# ============================================================

def simulate_mitigation(
    observation,
    feature,
    original_risk
):

    if feature not in MITIGATION_LIBRARY:

        raise ValueError(
            f"No mitigation available for feature: {feature}"
        )

    mitigation = MITIGATION_LIBRARY[feature]

    # Convert observation into DataFrame
    simulated = pd.DataFrame([observation])

    # Arrange columns exactly like training
    simulated = simulated.reindex(
        columns=feature_names
    )

    # Convert values to numeric
    simulated = simulated.apply(
        pd.to_numeric,
        errors="coerce"
    )

    # Apply virtual mitigation
    simulated[feature] = (
        simulated[feature]
        * mitigation["reduction_factor"]
    )

    # Predict new attack probability
    new_probability = calibrated_rf.predict_proba(
        simulated.to_numpy()
    )[0, 1]

    # Calculate new risk
    new_risk, new_risk_level = calculate_risk_from_probability(
        new_probability
    )

    # Calculate estimated reduction
    estimated_reduction = original_risk - new_risk

    return {

        "feature": feature,

        "mitigation": mitigation["mitigation"],

        "original_risk": float(original_risk),

        "new_risk": float(new_risk),

        "estimated_reduction": float(
            estimated_reduction
        ),

        "new_risk_level": new_risk_level,

        "security_rationale":
            mitigation["security_rationale"],

        "model_based_estimate": True
    }


# ============================================================
# Prioritize multiple mitigations
# ============================================================

def prioritize_mitigations(
    observation,
    original_risk
):
    """
    Simulate all supported mitigations and prioritize them
    based on model-estimated risk reduction.
    """

    results = []

    # Simulate every mitigation
    for feature in MITIGATION_LIBRARY:

        simulation = simulate_mitigation(
            observation,
            feature,
            original_risk
        )

        results.append(simulation)

    # Sort from highest estimated reduction
    # to lowest estimated reduction
    results.sort(
        key=lambda item: item["estimated_reduction"],
        reverse=True
    )

    # Add priority numbers
    for index, result in enumerate(
        results,
        start=1
    ):

        result["priority"] = index

    return results