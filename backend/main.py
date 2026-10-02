from typing import Any
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from backend.database.db import (
    save_risk_assessment,
    register_system
)

from backend.ml.mitigation_engine import (
    simulate_mitigation,
    prioritize_mitigations
)

from backend.ml.risk_engine import (
    predict_risk,
    explain_risk,
    feature_names
)

from backend.ml.recommendation_engine import (
    generate_recommendations
)


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="AI Cyber Risk Scoring System",
    description="AI-powered cybersecurity risk assessment backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    


# ============================================================
# Request Models
# ============================================================

class RiskRequest(BaseModel):
    system_id: str
    observation: dict[str, Any]


class MitigationRequest(BaseModel):
    observation: dict[str, Any]
    feature: str


class SystemRegistrationRequest(BaseModel):
    system_id: str
    hostname: str
    operating_system: str
    agent_version: str


# ============================================================
# Home
# ============================================================

@app.get("/")
def home():

    return {
        "message": "AI Cyber Risk API is running"
    }


# ============================================================
# 1. COMPLETE CYBER RISK ASSESSMENT
# ============================================================

@app.post("/predict-risk")
def predict_cyber_risk(request: RiskRequest):

    system_id = request.system_id
    observation = request.observation

    # --------------------------------------------------------
    # Check for missing features
    # --------------------------------------------------------

    missing_features = [
        feature
        for feature in feature_names
        if feature not in observation
    ]

    if missing_features:

        raise HTTPException(
            status_code=422,
            detail={
                "message": "Missing required features",
                "count": len(missing_features),
                "features": missing_features
            }
        )

    # --------------------------------------------------------
    # Check for unexpected features
    # --------------------------------------------------------

    unexpected_features = [
        feature
        for feature in observation
        if feature not in feature_names
    ]

    if unexpected_features:

        raise HTTPException(
            status_code=422,
            detail={
                "message": "Unexpected features found",
                "count": len(unexpected_features),
                "features": unexpected_features
            }
        )

    # --------------------------------------------------------
    # Predict cyber risk
    # --------------------------------------------------------

    risk_result = predict_risk(
        observation
    )

    # --------------------------------------------------------
    # Generate SHAP explanation
    # --------------------------------------------------------

    shap_results = explain_risk(
        observation,
        top_n=10
    )

    # --------------------------------------------------------
    # Generate security recommendations
    # --------------------------------------------------------

    recommendations = generate_recommendations(
        shap_results,
        top_n=5
    )

    # --------------------------------------------------------
    # Save risk assessment to MongoDB
    # --------------------------------------------------------

    
    assessment = {
    "system_id": system_id,
    "observation": observation,

    "attack_probability": risk_result[
        "attack_probability"
    ],

    "risk_score": risk_result[
        "risk_score"
    ],

    "risk_level": risk_result[
        "risk_level"
    ],

    "model_version": "random_forest_v1",

    "timestamp": datetime.now(timezone.utc),

    "shap_explanations": shap_results,

    "recommendations": recommendations
}
    

    try:

        assessment_id = save_risk_assessment(
            assessment
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail={
                "message":
                    "Risk prediction succeeded, "
                    "but saving to MongoDB failed",

                "error": str(error)
            }
        )

    # --------------------------------------------------------
    # Return complete assessment
    # --------------------------------------------------------

    return {

        "system_id": system_id,

        "risk_assessment": risk_result,

        "shap_explanations": shap_results,

        "recommendations": recommendations,

        "database": {
            "saved": True,
            "assessment_id": assessment_id
        }

    }


# ============================================================
# 2. MITIGATION SIMULATION
# ============================================================

@app.post("/simulate-mitigation")
def simulate_cyber_mitigation(
    request: MitigationRequest
):

    observation = request.observation
    feature = request.feature

    # --------------------------------------------------------
    # Check for missing features
    # --------------------------------------------------------

    missing_features = [
        feature_name
        for feature_name in feature_names
        if feature_name not in observation
    ]

    if missing_features:

        raise HTTPException(
            status_code=422,
            detail={
                "message": "Missing required features",
                "count": len(missing_features),
                "features": missing_features
            }
        )

    # --------------------------------------------------------
    # Check for unexpected features
    # --------------------------------------------------------

    unexpected_features = [
        feature_name
        for feature_name in observation
        if feature_name not in feature_names
    ]

    if unexpected_features:

        raise HTTPException(
            status_code=422,
            detail={
                "message": "Unexpected features found",
                "count": len(unexpected_features),
                "features": unexpected_features
            }
        )

    # --------------------------------------------------------
    # Calculate current risk
    # --------------------------------------------------------

    current_risk = predict_risk(
        observation
    )

    # --------------------------------------------------------
    # Simulate selected mitigation
    # --------------------------------------------------------

    try:

        simulation = simulate_mitigation(
            observation,
            feature,
            current_risk["risk_score"]
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail={
                "message": str(error)
            }
        )

    # --------------------------------------------------------
    # Return mitigation result
    # --------------------------------------------------------

    return {

        "current_risk": current_risk,

        "mitigation_simulation": simulation

    }


# ============================================================
# 3. MITIGATION PRIORITIZATION
# ============================================================

@app.post("/prioritize-mitigations")
def prioritize_cyber_mitigations(
    request: RiskRequest
):

    system_id = request.system_id
    observation = request.observation

    # --------------------------------------------------------
    # Check for missing features
    # --------------------------------------------------------

    missing_features = [
        feature
        for feature in feature_names
        if feature not in observation
    ]

    if missing_features:

        raise HTTPException(
            status_code=422,
            detail={
                "message": "Missing required features",
                "count": len(missing_features),
                "features": missing_features
            }
        )

    # --------------------------------------------------------
    # Check for unexpected features
    # --------------------------------------------------------

    unexpected_features = [
        feature
        for feature in observation
        if feature not in feature_names
    ]

    if unexpected_features:

        raise HTTPException(
            status_code=422,
            detail={
                "message": "Unexpected features found",
                "count": len(unexpected_features),
                "features": unexpected_features
            }
        )

    # --------------------------------------------------------
    # Calculate current risk
    # --------------------------------------------------------

    current_risk = predict_risk(
        observation
    )

    # --------------------------------------------------------
    # Prioritize mitigations
    # --------------------------------------------------------

    prioritized_mitigations = prioritize_mitigations(
        observation,
        current_risk["risk_score"]
    )

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {

        "system_id": system_id,

        "current_risk": current_risk,

        "prioritized_mitigations":
            prioritized_mitigations

    }


# ============================================================
# 4. RISK HISTORY
# ============================================================

@app.get("/risk-history")
def get_risk_history(limit: int = 20):

    from backend.database.db import (
        risk_assessments_collection
    )

    try:

        assessments = list(
            risk_assessments_collection
            .find(
                {},
                {
                    "_id": 1,
                    "system_id": 1,
                    "attack_probability": 1,
                    "risk_score": 1,
                    "risk_level": 1,
                    "model_version": 1,
                    "timestamp": 1
                }
            )
            .sort(
                "timestamp",
                -1
            )
            .limit(limit)
        )

        history = []

        for assessment in assessments:

            history.append({

                "assessment_id":
                    str(assessment["_id"]),

                "system_id":
                    assessment.get(
                        "system_id",
                        "UNKNOWN"
                    ),

                "attack_probability":
                    assessment.get(
                        "attack_probability"
                    ),

                "risk_score":
                    assessment.get(
                        "risk_score"
                    ),

                "risk_level":
                    assessment.get(
                        "risk_level"
                    ),

                "model_version":
                    assessment.get(
                        "model_version"
                    ),

                "timestamp":
                    assessment.get(
                        "timestamp"
                    )
            })

        return {

            "count":
                len(history),

            "risk_history":
                history

        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail={
                "message":
                    "Failed to retrieve risk history",

                "error": str(error)
            }
        )


# ============================================================
# 5. DASHBOARD STATISTICS
# ============================================================

@app.get("/dashboard-stats")
def get_dashboard_stats():

    from backend.database.db import (
        risk_assessments_collection
    )

    try:

        # ----------------------------------------------------
        # Total assessments
        # ----------------------------------------------------

        total_assessments = (
            risk_assessments_collection
            .count_documents({})
        )

        # ----------------------------------------------------
        # Risk distribution
        # ----------------------------------------------------

        critical_count = (
            risk_assessments_collection
            .count_documents(
                {
                    "risk_level": "CRITICAL"
                }
            )
        )

        high_count = (
            risk_assessments_collection
            .count_documents(
                {
                    "risk_level": "HIGH"
                }
            )
        )

        medium_count = (
            risk_assessments_collection
            .count_documents(
                {
                    "risk_level": "MEDIUM"
                }
            )
        )

        low_count = (
            risk_assessments_collection
            .count_documents(
                {
                    "risk_level": "LOW"
                }
            )
        )

        # ----------------------------------------------------
        # Get risk scores
        # ----------------------------------------------------

        scores = list(
            risk_assessments_collection
            .find(
                {},
                {
                    "_id": 0,
                    "risk_score": 1
                }
            )
        )

        risk_scores = [
            item["risk_score"]
            for item in scores
            if "risk_score" in item
        ]

        # ----------------------------------------------------
        # Calculate statistics
        # ----------------------------------------------------

        if risk_scores:

            average_risk = (
                sum(risk_scores)
                / len(risk_scores)
            )

            highest_risk = max(
                risk_scores
            )

            lowest_risk = min(
                risk_scores
            )

        else:

            average_risk = 0
            highest_risk = 0
            lowest_risk = 0

        # ----------------------------------------------------
        # Return dashboard statistics
        # ----------------------------------------------------

        return {

            "total_assessments":
                total_assessments,

            "risk_distribution": {

                "critical":
                    critical_count,

                "high":
                    high_count,

                "medium":
                    medium_count,

                "low":
                    low_count

            },

            "risk_statistics": {

                "average_risk":
                    average_risk,

                "highest_risk":
                    highest_risk,

                "lowest_risk":
                    lowest_risk

            }

        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail={
                "message":
                    "Failed to retrieve dashboard statistics",

                "error": str(error)
            }
        )


# ============================================================
# 6. SYSTEM REGISTRATION
# ============================================================

@app.post("/register-system")
def register_cyber_system(
    request: SystemRegistrationRequest
):

    system = {

        "system_id":
            request.system_id,

        "hostname":
            request.hostname,

        "operating_system":
            request.operating_system,

        "agent_version":
            request.agent_version,

        "registered_at":
            datetime.now(timezone.utc)

    }

    try:

        database_id = register_system(
            system
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail={
                "message":
                    "Failed to register system",

                "error": str(error)
            }
        )

    return {

        "message":
            "System registered successfully",

        "system": {

            "system_id":
                request.system_id,

            "hostname":
                request.hostname,

            "operating_system":
                request.operating_system,

            "agent_version":
                request.agent_version,

            "database_id":
                database_id

        }

    }
    
    # ============================================================
# 7. SYSTEMS LIST
# ============================================================

@app.get("/systems")
def get_systems():

    from backend.database.db import (
        systems_collection,
        risk_assessments_collection
    )

    try:

        systems = list(
            systems_collection
            .find({})
            .sort("registered_at", -1)
        )

        system_list = []

        for system in systems:

            system_id = system.get(
                "system_id",
                "UNKNOWN"
            )

            # Find latest risk assessment
            latest_assessment = (
                risk_assessments_collection
                .find_one(
                    {
                        "system_id": system_id
                    },
                    sort=[
                        ("timestamp", -1)
                    ]
                )
            )

            if latest_assessment:

                latest_risk = {
                    "risk_score":
                        latest_assessment.get(
                            "risk_score",
                            0
                        ),

                    "risk_level":
                        latest_assessment.get(
                            "risk_level",
                            "UNKNOWN"
                        ),

                    "attack_probability":
                        latest_assessment.get(
                            "attack_probability",
                            0
                        ),

                    "timestamp":
                        latest_assessment.get(
                            "timestamp"
                        )
                }

            else:

                latest_risk = {
                    "risk_score": 0,
                    "risk_level": "NOT ASSESSED",
                    "attack_probability": 0,
                    "timestamp": None
                }

            system_list.append({

                "system_id":
                    system_id,

                "hostname":
                    system.get(
                        "hostname",
                        "Unknown"
                    ),

                "operating_system":
                    system.get(
                        "operating_system",
                        "Unknown"
                    ),

                "agent_version":
                    system.get(
                        "agent_version",
                        "Unknown"
                    ),

                "registered_at":
                    system.get(
                        "registered_at"
                    ),

                "latest_risk":
                    latest_risk
            })

        return {

            "count":
                len(system_list),

            "systems":
                system_list
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail={
                "message":
                    "Failed to retrieve systems",

                "error":
                    str(error)
            }
        )
        
        # ============================================================
# 8. SYSTEM RISK DETAILS
# ============================================================

@app.get("/systems/{system_id}/risk")
def get_system_risk(system_id: str):

    from backend.database.db import (
        risk_assessments_collection
    )

    try:

        assessment = (
            risk_assessments_collection
            .find_one(
                {
                    "system_id": system_id
                },
                sort=[
                    ("timestamp", -1)
                ]
            )
        )

        if not assessment:

            raise HTTPException(
                status_code=404,
                detail="No risk assessment found for this system"
            )

        return {

            "system_id":
                system_id,

            "risk_assessment": {

                "attack_probability":
                    assessment.get(
                        "attack_probability"
                    ),

                "risk_score":
                    assessment.get(
                        "risk_score"
                    ),

                "risk_level":
                    assessment.get(
                        "risk_level"
                    ),

                "model_version":
                    assessment.get(
                        "model_version"
                    ),

                "timestamp":
                    assessment.get(
                        "timestamp"
                    )
            },

            "shap_explanations":
                assessment.get(
                    "shap_explanations",
                    []
                ),

            "recommendations":
                assessment.get(
                    "recommendations",
                    []
                )
        }

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail={
                "message":
                    "Failed to retrieve risk details",

                "error":
                    str(error)
            }
        )
      
      # ============================================================
# 9. SYSTEM OBSERVATION
# ============================================================

@app.get("/systems/{system_id}/observation")
def get_system_observation(system_id: str):

    from backend.database.db import risk_assessments_collection

    try:

        assessment = (
            risk_assessments_collection
            .find_one(
                {
                    "system_id": system_id
                },
                sort=[
                    ("timestamp", -1)
                ]
            )
        )

        if not assessment:

            raise HTTPException(
                status_code=404,
                detail="No risk assessment found for this system"
            )

        observation = assessment.get(
            "observation",
            {}
        )

        if not observation:

            raise HTTPException(
                status_code=404,
                detail="No model observation found for this system"
            )

        return {
            "system_id": system_id,
            "observation": observation,
            "timestamp": assessment.get("timestamp")
        }

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail={
                "message": "Failed to retrieve system observation",
                "error": str(error)
            }
        )