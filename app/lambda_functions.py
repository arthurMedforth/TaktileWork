import json

def KYC(payload, rules, params):
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
    
def CreditReportCheck(payload, rules, params):
    with open('/Users/arthurmedforth/Taktile work/experian.json', '+r') as experian_report:
        experian_response = json.load(experian_report)   

    response = {}
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

def IncomeVerification(payload, rules, params):
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
