from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer, Loan
from decimal import Decimal
from datetime import date
from dateutil.relativedelta import relativedelta
@api_view(['POST'])
def register_customer(request):
  data = request.data
  approved_limit = nearest_lakh(Decimal(data['monthly_salary'] * 36))
  customer = Customer.objects.create(
    customer_id=data['customer_id'],
    first_name=data['first_name'],
    last_name=data['last_name'],
    age=data['age'],
    phone_number=data['phone_number'],
    monthly_salary=data['monthly_salary'],
    approved_limit=approved_limit
  )
  return Response({
    'customer_id': customer.customer_id,
    'name' : customer.first_name + ' ' + customer.last_name,
    'age' : customer.age,
    'monthly_income' : customer.monthly_salary,
    'phone_number' : customer.phone_number,
    'approved_limit' : customer.approved_limit,
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def view_loan(request, loan_id):
  try:
    loan = Loan.objects.get(loan_id=loan_id)
    customer = Customer.objects.get(customer_id=loan.customer_id)
    customerJSON = {
      'customer_id': customer.customer_id,
      'first_name': customer.first_name,
      'last_name': customer.last_name,
      'age': customer.age,
      'phone_number': customer.phone_number
    }
    return Response({
      'loan_id': loan.loan_id,
      'customer': customerJSON,
      'loan_amount': loan.loan_amount,
      'tenure': loan.tenure,
      'interest_rate': loan.interest_rate,
      'monthly_repayment': loan.monthly_repayment,
      'emis_paid_on_time': loan.emis_paid_on_time,
      'date_of_approval': loan.date_of_approval,
      'end_date': loan.end_date
    }, status=status.HTTP_200_OK)
  except Loan.DoesNotExist:
    return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)
  except Customer.DoesNotExist:
    return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def check_eligibility(request):
  eligible_loan = make_eligible_loan(request)
  return Response(eligible_loan[0], status=eligible_loan[1])

@api_view(['POST'])
def create_loan(request):
  eligible_loan = make_eligible_loan(request)
  data = request.data
  if eligible_loan[0]['approval']==False :
    return Response({
      'loan_id': None,
      'customer_id' : data['customer_id'],
      'loan_approved' : False,
      'message' : 'Loan not approved due to insufficient credit score or exceeding approved limit.'
    }, status=status.HTTP_400_BAD_REQUEST)
  
  newloan = Loan.objects.create(
    customer_id=data['customer_id'],
    loan_amount=data['loan_amount'],
    tenure=data['tenure'],
    interest_rate=eligible_loan[0]['corrected_interest_rate'],
    monthly_repayment=eligible_loan[0]['monthly_installment'],
    emis_paid_on_time=0,
    date_of_approval=date.today(),
    end_date=date.today()+relativedelta(months=data['tenure'])
  )
  
  return Response({
    'loan_id' : newloan.loan_id,
    'customer_id' : newloan.customer_id,
    'loan_approved' : True,
    'message' : 'Loan approved.',
    'monthly_installment' : newloan.monthly_repayment
  }, status=status.HTTP_201_CREATED)

def make_eligible_loan(request):
  data = request.data
  loans = Loan.objects.filter(customer_id=int(data['customer_id']))

  pending_loan_amount = 0
  for loan in loans:
    loan_amount = loan.loan_amount
    pending_loan_amount += loan_amount - (loan.monthly_repayment * loan.emis_paid_on_time)
  
  customer = Customer.objects.get(customer_id=data['customer_id'])

  if pending_loan_amount + data['loan_amount'] > customer.approved_limit:
    return [
      {
      'customer_id': data['customer_id'],
      'approval' : False
      },
      status.HTTP_200_OK
    ]
  
  fill_score = (pending_loan_amount + data['loan_amount'])/Decimal(customer.approved_limit)
  credit_score = (1-fill_score)*100
  
  if credit_score > 50:
    return [{
      'customer_id': data['customer_id'],
      'approval' : True,
      'interest_rate' : data['interest_rate'],
      'corrected_interest_rate' : data['interest_rate'],
      'tenure' : data['tenure'],
      'monthly_installment' : calc_emi(data['loan_amount'], data['interest_rate'], data['tenure']),
    }, status.HTTP_200_OK]
  if credit_score > 30:
    corrected_interest_rate = data['interest_rate'] if data['interest_rate'] >= 12 else 12
    return [{
      'customer_id': data['customer_id'],
      'approval' : True,
      'interest_rate' : data['interest_rate'],
      'corrected_interest_rate' : corrected_interest_rate,
      'tenure' : data['tenure'],
      'monthly_installment' : calc_emi(data['loan_amount'], corrected_interest_rate, data['tenure']),
    }, status.HTTP_200_OK]
  if credit_score > 10:
    corrected_interest_rate = data['interest_rate'] if data['interest_rate'] >= 16 else 16
    return [{
      'customer_id': data['customer_id'],
      'approval' : True,
      'interest_rate' : data['interest_rate'],
      'corrected_interest_rate' : corrected_interest_rate,
      'tenure' : data['tenure'],
      'monthly_installment' : calc_emi(data['loan_amount'], corrected_interest_rate, data['tenure']),
    }, status.HTTP_200_OK]
  else:
    return [{
      'customer_id': data['customer_id'],
      'approval' : False
    }, status.HTTP_200_OK]

@api_view(['GET'])
def view_loans(request, customer_id):
  try:
    loans = Loan.objects.filter(customer_id=customer_id)
    loan_list = []
    for loan in loans:
      loan_list.append({
        'loan_id': loan.loan_id,
        'loan_amount': loan.loan_amount,
        'interest_rate': loan.interest_rate,
        'monthly_installment': loan.monthly_repayment,
        'repayments_left' : loan.tenure - loan.emis_paid_on_time
      })
    
    return Response(loan_list, status=status.HTTP_200_OK)
  except Loan.DoesNotExist:
    return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

def nearest_lakh(amount):
  return round(amount/(10**5)) * (10**5)

def calc_emi(loan_amount, interest_rate, tenure):
  interest_rate /= 100
  numerator = loan_amount * interest_rate * (1 + interest_rate) ** tenure
  denominator = (1 + interest_rate) ** tenure - 1
  if denominator == 0:
    return 0
  return numerator / denominator