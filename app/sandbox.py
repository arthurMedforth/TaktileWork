from lambda_functions import CreditReportCheck, KYC, IncomeVerification

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
                "lambda_function": "KYC",
                "rules": {
                    "rule_id": 1,
                    "rule_name": "Age Less Than 18",
                    "threshold": 18,
                    "parameter": "age",
                    "operation": "lt",
                    "active": True
                },
                "parameters": {
                    "fraud_score_threshold": 75
                },
                "description": "Verify if the applicant's fraud score is within acceptable limits."
            },
            {
                "stage_id": 2,
                "lambda_function": "CreditHistory",
                "parameters": {
                    "credit_bureau": "Experian"
                },
                "description": "Retrieve the applicant's credit report from the specified credit bureau."
            },
            {
                "stage_id": 3,
                "lambda_function": "IncomeVerification",
                "parameters": {
                    "income_threshold": 30000
                },
                "description": "Ensure the applicant's verified income meets the required threshold."
            }
        ]
    }

def call_lambda(function_name: str, payload: dict, rules: dict, params: dict) -> dict:
    """
    Invokes an AWS Lambda function with a given payload and returns its response.

    Args:
        function_name (str): The name of the Lambda function to invoke.
        payload (dict): The payload to send to the Lambda function.

    Returns:
        dict: The response from the Lambda function.
    """
    if function_name == 'KYC':
        response = KYC(payload, rules, params)
    elif function_name == 'CreditHistory':
        response = CreditReportCheck(payload, rules, params)
    else:
        response = IncomeVerification(payload, rules, params)
    return response


def evaluate_credit_application(application):
    workflow = fetch_workflow_config()
    stages = workflow["stages"]
    for stage in stages:
        response = call_lambda(stage["lambda_function"], application, stage["rules"], stage["parameters"])
    return {"message": f"Application received successfully."}

evaluate_credit_application()