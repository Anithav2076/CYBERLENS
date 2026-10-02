import os
import json
import pandas as pd


# Project root
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

# Dataset location
DATASET_PATH = os.path.join(
    BASE_DIR,
    "datasets",
    "windows",
    "Train_Test_Windows_10.csv"
)

# Load dataset
df = pd.read_csv(DATASET_PATH)

# Take the first real record
sample = df.iloc[0]

# Remove target and attack type
observation = sample.drop(
    labels=["label", "type"]
).to_dict()

# Save as JSON
OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "backend",
    "test_payload.json"
)

with open(OUTPUT_PATH, "w") as file:
    json.dump(observation, file, indent=4)

print("Test payload created successfully.")
print("Number of features:", len(observation))
print("Saved to:", OUTPUT_PATH) 