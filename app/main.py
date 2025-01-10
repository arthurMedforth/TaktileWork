from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from app.models.CreditApplication import CreditApplication
import json

# Create FastAPI app
app = FastAPI()

# Stub of configuration response
def fetch_workflow_config():
    """
    Stub function to simulate fetching workflow configuration from the database.
    """
    return {
        "workflow_id": "credit_app_workflow_001",
        "stages": [
            {
                "stage_id": 1,
                "lambda_function": "check_fraud_score",
                "parameters": {
                    "fraud_score_threshold": 75
                },
                "description": "Verify if the applicant's fraud score is within acceptable limits."
            },
            {
                "stage_id": 2,
                "lambda_function": "fetch_credit_report",
                "parameters": {
                    "credit_bureau": "Experian"
                },
                "description": "Retrieve the applicant's credit report from the specified credit bureau."
            },
            {
                "stage_id": 3,
                "lambda_function": "verify_income",
                "parameters": {
                    "income_threshold": 30000
                },
                "description": "Ensure the applicant's verified income meets the required threshold."
            }
        ]
    }


# Define a simple route
@app.get("/")
def read_root():
    return {"message": "Taktile demonstration!"}


# Define POST route that expects the DataModel
@app.post("/evaluateCreditApp")
def evaluate_credit_application(application: CreditApplication):
    workflow_json = fetch_workflow_config()
    workflow = json.loads(workflow_json)

    return {"message": f"Application {application.application_id} received successfully."}
