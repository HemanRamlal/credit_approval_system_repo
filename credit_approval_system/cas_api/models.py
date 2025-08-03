from django.db import models

class Customer(models.Model):
    class Meta:
        db_table="customer"

    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=20)
    monthly_salary = models.DecimalField(max_digits=20, decimal_places=2)
    approved_limit = models.DecimalField(max_digits=20, decimal_places=2)

class Loan(models.Model):
    class Meta:
        db_table="loan"

    customer_id = models.IntegerField()
    loan_id = models.AutoField(primary_key=True)
    loan_amount = models.DecimalField(max_digits=20, decimal_places=2)
    tenure = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=20, decimal_places=2)
    monthly_repayment = models.DecimalField(max_digits=20, decimal_places=2)
    emis_paid_on_time = models.IntegerField()
    date_of_approval = models.DateField()
    end_date = models.DateField()