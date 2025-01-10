import json

def KYC(payload, rules, params):
    response = []
    return response
    
def CreditReportCheck(payload, rules, params):
    with open('/Users/arthurmedforth/Taktile work/experian.json', '+r') as experian_report:
        response = json.load(experian_report)         
    return response

def IncomeVerification(payload, rules, params):
    response = []
    return response