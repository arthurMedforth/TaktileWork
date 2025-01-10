from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import json

from app.models.CreditApplication import CreditApplication
from .lambda_functions import CreditReportCheck, KYC, IncomeVerification

# Create FastAPI app
app = FastAPI()

def fetch_workflow_config():
    # Mocked response of fetch_workflow_config
    return {
        "workflow_id": "credit_app_workflow_001",
        "stages": [
            {
                "stage_id": 1,
                "lambda_function": "KYC",
                "rules": [],
                "parameters": {
                    "fraud_score_threshold": 75
                },
                "description": "Verify if the applicant's fraud score is within acceptable limits."
            },
            {
                "stage_id": 2,
                "lambda_function": "CreditHistory",
                "rules": [
                    {
                        "rule_id": 1,
                        "rule_name": "Credit Score Above Threshold",
                        "threshold": 650,
                        "parameter": "creditScore",
                        "operation": "gt",
                        "active": True
                    }
                ],
                "parameters": {
                    "credit_bureau": "Experian"
                },
                "description": "Retrieve the applicant's credit report from the specified credit bureau."
            },
            {
                "stage_id": 3,
                "lambda_function": "IncomeVerification",
                "rules": [],
                "parameters": {
                    "income_threshold": 30000
                },
                "description": "Ensure the applicant's verified income meets the required threshold."
            }
        ]
    }


def call_lambda(function_name: str, payload: dict, rules: dict, params: dict) -> dict:
    if function_name == 'KYC':
        response = KYC(payload, rules, params)
    elif function_name == 'CreditHistory':
        response = CreditReportCheck(payload, rules, params)
    elif function_name == "IncomeVerification":
        response = IncomeVerification(payload, rules, params)
    else:
        raise ValueError("No such Lambda function exists")
    return response


# Define a simple route
@app.get("/")
def read_root():
    return {"message": "Taktile demonstration!"}


# Define POST route that expects the DataModel
@app.post("/evaluateCreditApp")
def evaluate_credit_application(application: CreditApplication):
    # Fetch the workflow configuration (presumably from a mock function or a database)
    workflow = fetch_workflow_config()
    
    # Initialize an empty list to store the responses from each stage
    stage_responses = []
    
    # Loop through the stages in the workflow
    for stage in workflow["stages"]:
        # Call the lambda for each stage and capture the response
        response = call_lambda(stage["lambda_function"], application, stage["rules"], stage["parameters"])
        
        # Append the response along with stage information to the stage_responses list
        stage_responses.append({
            "stage_id": stage["stage_id"],
            "lambda_function": stage["lambda_function"],
            "response": response
        })
    
    # Return the combined response
    return {"applicationResult": stage_responses}
