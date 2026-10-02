import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST_URI = os.getenv("MONGO_HOST_URI")

if not MONGO_USERNAME or not MONGO_PASSWORD or not MONGO_HOST_URI:
    raise ValueError("MongoDB configuration is missing in .env")

credentials = f"{quote_plus(MONGO_USERNAME)}:{quote_plus(MONGO_PASSWORD)}@"

MONGO_URI = MONGO_HOST_URI.replace(
    "mongodb://",
    f"mongodb://{credentials}",
    1
)

client = MongoClient(MONGO_URI)

db = client["ai_cyber_risk"]

systems_collection = db["systems"]
observations_collection = db["observations"]
risk_assessments_collection = db["risk_assessments"]
mitigation_results_collection = db["mitigation_results"]

def save_observation(observation):
    result = observations_collection.insert_one(observation)
    return str(result.inserted_id)

def save_risk_assessment(assessment):
    result = risk_assessments_collection.insert_one(assessment)
    return str(result.inserted_id)

def register_system(system):

    result = systems_collection.insert_one(system)

    return str(result.inserted_id)