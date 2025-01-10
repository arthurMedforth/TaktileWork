from pydantic import BaseModel
from typing import Optional

# Submodels for personal details, address, employment, etc.
class PersonalDetails(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str  # You can use `datetime.date` if you want proper validation
    ssn: str
    email: str
    phone_number: str

class Address(BaseModel):
    street_address: str
    city: str
    state: str
    zip_code: str
    country: str

class BankAccount(BaseModel):
    account_type: str
    bank_name: str
    account_number: str
    routing_number: str

class FinancialDetails(BaseModel):
    existing_debt: float
    monthly_expenses: float
    credit_score: int
    bank_account: BankAccount

class EmploymentDetails(BaseModel):
    employer_name: str
    job_title: str
    annual_income: float
    employment_status: str
    work_phone: str

class AdditionalInfo(BaseModel):
    desired_credit_limit: float
    purpose_of_credit: str
    referred_by: str

class Consent(BaseModel):
    terms_accepted: bool
    credit_check_consent: bool
    data_sharing_consent: bool

# Main CreditApplication model
class CreditApplication(BaseModel):
    application_id: str
    personal_details: PersonalDetails
    address: Address
    employment_details: EmploymentDetails
    financial_details: FinancialDetails
    additional_info: AdditionalInfo
    consent: Consent

# Example usag
