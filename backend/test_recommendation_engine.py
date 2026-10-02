from ml.recommendation_engine import generate_recommendations


# Sample SHAP results
sample_shap_results = [

    {
        "feature": "Process_Virtual_Bytes",
        "shap_value": 0.093782,
        "feature_value": 271000000000000.0
    },

    {
        "feature": "Process_Thread Count",
        "shap_value": 0.062347,
        "feature_value": 1623
    },

    {
        "feature": "Process_Handle Count",
        "shap_value": 0.054251,
        "feature_value": 51117
    },

    {
        "feature": "Process_Pool_Paged Bytes",
        "shap_value": -0.036622,
        "feature_value": 27042896
    }
]


recommendations = generate_recommendations(
    sample_shap_results
)


print("\n===== SECURITY RECOMMENDATIONS =====")

for item in recommendations:

    print("\nFeature:", item["feature"])

    print("SHAP Value:", item["shap_value"])

    print("Contribution:", item["contribution"])

    print("Recommendation:",
          item["recommendation"])

    print("Security Rationale:",
          item["security_rationale"])

    print("Simulation:",
          item["simulation_change"])