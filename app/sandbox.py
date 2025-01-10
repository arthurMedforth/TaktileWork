from lambda_functions import CreditReportCheck, KYC, IncomeVerification

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
                        "rule_name": "Credit Score Below Threshold",
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


def evaluate_credit_application(application):
    workflow = fetch_workflow_config()
    for stage in workflow["stages"]:
        response = call_lambda(stage["lambda_function"], application, stage["rules"], stage["parameters"])
    return {"message": response}


application = {
  "application_id": "123456789",
  "personal_details": {
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-05-15",
    "ssn": "123-45-6789",
    "email": "johndoe@example.com",
    "phone_number": "+1234567890"
  },
  "address": {
    "street_address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "country": "USA"
  },
  "employment_details": {
    "employer_name": "TechCorp Inc.",
    "job_title": "Software Engineer",
    "annual_income": 85000,
    "employment_status": "Full-time",
    "work_phone": "+1234567891"
  },
  "financial_details": {
    "existing_debt": 10000,
    "monthly_expenses": 2000,
    "credit_score": 720,
    "bank_account": {
      "account_type": "Checking",
      "bank_name": "BigBank",
      "account_number": "1234567890",
      "routing_number": "111000025"
    }
  },
  "additional_info": {
    "desired_credit_limit": 5000,
    "purpose_of_credit": "Personal expenses",
    "referred_by": "Friend"
  },
  "consent": {
    "terms_accepted": True,
    "credit_check_consent": True,
    "data_sharing_consent": True
  }
}
response = evaluate_credit_application(application)
print(response)