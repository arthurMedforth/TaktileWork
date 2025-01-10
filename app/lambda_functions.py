import json
from typing import Dict

def KYC(payload: Dict, rules: Dict, params: Dict) -> Dict:
    return {
        "status": "success",
        "message": "KYC check completed successfully",
        "data": {
            "customer_id": "12345",
            "name": "John Doe",
            "dob": "1985-05-15",
            "address": {
            "line1": "123 Main Street",
            "line2": "Apt 4B",
            "city": "New York",
            "state": "NY",
            "zip_code": "10001",
            "country": "US"
            },
            "identification": {
            "id_type": "passport",
            "id_number": "A1234567",
            "expiry_date": "2030-12-31"
            },
            "kyc_score": 90,
            "kyc_status": "approved",
            "knockout_rules": [
            {
                "rule_id": 1,
                "description": "Address mismatch",
                "status": "pass"
            },
            {
                "rule_id": 2,
                "description": "Name match",
                "status": "pass"
            }
            ]
        }
    }
    
def CreditReportCheck(payload, rules, params) -> Dict:
    with open('/Users/arthurmedforth/Taktile work/experian.json', '+r') as experian_report:
        experian_response = json.load(experian_report)   

    response = {}
    response["credit_score"] = experian_response["creditScore"]["score"]
    # Apply rules to the credit report
    for rule in rules:
        if rule["operation"] == "lt" and experian_response[rule["parameter"]]["score"] < rule["threshold"]:
            # Rule passed
            response["status"] = f"Rule {rule['rule_name']} passed: {experian_response[rule['parameter']]['score']} is less than threshold"
            break
        elif rule["operation"] == "eq" and experian_response[rule["parameter"]]["score"] == rule.get("value"):
            # Rule passed
            response["status"] = f"Rule {rule['rule_name']} passed: {experian_response[rule['parameter']]['score']} is equal to {rule['value']}"
            break
        elif rule["operation"] == "gt" and experian_response[rule["parameter"]]["score"] > rule["threshold"]:
            # Rule passed
            response["status"] = f"Rule {rule['rule_name']} passed: {experian_response[rule['parameter']]['score']} is greater than threshold"
            break
        else:
            response["status"] = f"Rule {rule['rule_name']} failed - Credit score: {experian_response[rule['parameter']]['score']} - {rule['threshold']}"
    return response

def IncomeVerification(payload: Dict, rules: Dict, params: Dict) -> Dict:
    return {
        "status": "success",
        "message": "Income verification completed",
        "data": {
            "customer_id": "12345",
            "reported_income": 55000,
            "verified_income": 54000,
            "income_status": "verified",
            "income_source": "payroll",
            "income_verified_by": "Plaid",
            "verification_date": "2025-01-10",
            "knockout_rules": [
            {
                "rule_id": 1,
                "description": "Income discrepancy threshold exceeded",
                "status": "fail",
                "details": {
                "threshold": 5000,
                "discrepancy": 1000
                }
            },
            {
                "rule_id": 2,
                "description": "Income source verified",
                "status": "pass"
            }
            ]
        }
    }

def CreditLimitComputation(payload: Dict, params: Dict) -> Dict:
    response = {}
    # Parameters
    interest_rate = params["interest_rate"] # 2% monthly interest rate
    max_dti_ratio = params["max_dti_ratio"] # 40% debt-to-income ratio
    
    verified_income = payload[2]["response"]["data"]["verified_income"]/12

    # Step 1: Calculate maximum monthly repayment
    max_monthly_repayment = verified_income * max_dti_ratio
    
    # Step 2: Calculate base credit limit
    base_credit_limit = max_monthly_repayment / interest_rate

    # Step 3: Adjust credit limit based on credit score
    credit_score = payload[1]["response"]["credit_score"]
    
    if credit_score > 750:
        adjustment_factor = 1.0  # Full credit limit
    elif 650 <= credit_score <= 750:
        adjustment_factor = 0.8  # Reduce by 20%
    else:
        adjustment_factor = 0.5  # Reduce by 50%
    
    # Final credit limit
    credit_limit = base_credit_limit * adjustment_factor

    response["credit_limit"] = credit_limit
    response["status"] = "Success"
    
    return response
