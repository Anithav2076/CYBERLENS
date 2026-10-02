# ============================================================
# Recommendation Engine
# ============================================================

# Recommendations are based on important SHAP contributors.
# They are model-based security suggestions, not guaranteed fixes.


RECOMMENDATION_LIBRARY = {

    "Process_Virtual_Bytes": {
        "recommendation":
            "Investigate abnormal process virtual memory usage",

        "security_rationale":
            "Review processes consuming unusually large virtual memory "
            "and investigate unexpected resource usage.",

        "simulation_change":
            "20% reduction in Process_Virtual_Bytes"
    },

    "Process_Handle Count": {
        "recommendation":
            "Investigate unusually high process handle usage",

        "security_rationale":
            "Review processes with unusually high handle counts "
            "and investigate abnormal process behavior.",

        "simulation_change":
            "20% reduction in Process_Handle Count"
    },

    "Process_Thread Count": {
        "recommendation":
            "Investigate unusually high process thread usage",

        "security_rationale":
            "Review processes with unusually high thread counts "
            "and investigate unexpected process activity.",

        "simulation_change":
            "20% reduction in Process_Thread Count"
    },

    "Network_I(Intel R _82574L_GNC)TCP_APS": {
        "recommendation":
            "Investigate unusual TCP activity",

        "security_rationale":
            "Review unusual TCP activity and investigate unexpected "
            "network connections or communication patterns.",

        "simulation_change":
            "20% reduction in TCP activity"
    },

    "Memory System Cache Resident Bytes": {
        "recommendation":
            "Investigate abnormal system cache usage",

        "security_rationale":
            "Review unusually high system cache usage and "
            "investigate unexpected resource consumption.",

        "simulation_change":
            "20% reduction in system cache usage"
    }
}


def generate_recommendations(shap_results, top_n=5):

    recommendations = []

    for item in shap_results:

        feature = item["feature"]
        shap_value = item["shap_value"]
        feature_value = item["feature_value"]

        # Only recommend features that exist
        # in our recommendation library.
        if feature not in RECOMMENDATION_LIBRARY:
            continue

        info = RECOMMENDATION_LIBRARY[feature]

        # Determine whether the feature increases
        # or decreases the model's attack prediction.
        if shap_value > 0:
            contribution = "Increases predicted attack risk"
        elif shap_value < 0:
            contribution = "Decreases predicted attack risk"
        else:
            contribution = "No significant contribution"

        recommendations.append({
            "feature": feature,
            "feature_value": feature_value,
            "shap_value": shap_value,
            "contribution": contribution,
            "recommendation": info["recommendation"],
            "security_rationale": info["security_rationale"],
            "simulation_change": info["simulation_change"],
            "model_based_estimate": True
        })

        if len(recommendations) >= top_n:
            break

    return recommendations