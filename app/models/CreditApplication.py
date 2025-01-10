from pydantic import BaseModel
from typing import Optional

# Define Address model
class Address(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str

# Define User model
class User(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    dob: str
    address: Address

# Define Employment model
class Employment(BaseModel):
    status: str  # employed, self-employed, unemployed
    employer_name: str
    position: str
    annual_income: float
    employment_start_date: str

# Define Financial Info model
class FinancialInfo(BaseModel):
    requested_credit_limit: float
    existing_debt: float
    monthly_expenses: float

# Define Credit History model
class CreditHistory(BaseModel):
    credit_score: int
    total_credit_available: float
    open_credit_lines: int

# Define the main CreditApplication model that combines everything
class CreditApplication(BaseModel):
    application_id: str
    user: User
    employment: Employment
    financial_info: FinancialInfo
    credit_history: CreditHistory
    other: Optional[dict] = None  # This is for any other additional info (e.g., referral_code, marketing_opt_in)
