from backend.ml.risk_engine import feature_names
from agent.windows_counters import collect_toniot_features


print()
print("========================================")
print(" FEATURE SCHEMA VALIDATION")
print("========================================")
print()

observation = collect_toniot_features()

print(
    "Agent features:",
    len(observation)
)

print(
    "Model features:",
    len(feature_names)
)

agent_features = set(observation.keys())
model_features = set(feature_names)

missing_from_agent = (
    model_features - agent_features
)

extra_in_agent = (
    agent_features - model_features
)

print()
print(
    "Missing from agent:",
    len(missing_from_agent)
)

for feature in sorted(missing_from_agent):

    print(
        "  -",
        feature
    )

print()
print(
    "Extra features in agent:",
    len(extra_in_agent)
)

for feature in sorted(extra_in_agent):

    print(
        "  -",
        feature
    )

print()

if (
    not missing_from_agent
    and not extra_in_agent
):

    print(
        "✅ Feature names match exactly!"
    )

else:

    print(
        "⚠️ Feature schema needs mapping."
    )

print()
print("========================================")