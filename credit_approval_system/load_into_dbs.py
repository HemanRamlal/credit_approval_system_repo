import pandas as pd
from cas_api.models import Customer, Loan


def load_customers():
  customers = pd.read_excel('customer_data.xlsx')
  for _, row in customers.iterrows():
    customer = Customer(
        customer_id=row['Customer ID'],
        first_name=row['First Name'],
        last_name=row['Last Name'],
        age=row['Age'],
        phone_number=row['Phone Number'],
        monthly_salary=row['Monthly Salary'],
        approved_limit=row['Approved Limit']
    )
    customer.save()
  

def load_loans():
  loans = pd.read_excel('loan_data.xlsx')
  for _, row in loans.iterrows():
    loan = Loan(
      customer_id=row['Customer ID'],
      loan_id=row['Loan ID'],
      loan_amount=row['Loan Amount'],
      tenure=row['Tenure'],
      interest_rate=row['Interest Rate'],
      monthly_repayment=row['Monthly payment'],
      emis_paid_on_time=row['EMIs paid on Time'],
      date_of_approval=row['Date of Approval'],
      end_date=row['End Date']
    )
    loan.save()

load_loans()