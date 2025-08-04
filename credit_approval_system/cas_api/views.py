from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer, Loan
from decimal import Decimal
@api_view(['POST'])
def register_customer(request):
  data = request.data
  approved_limit = nearest_lakh(Decimal(data.get('monthly_salary') * 36))
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
  except Customer.DoesNotExist:
    return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

def nearest_lakh(amount):
  return round(amount/10**5) * 10**5