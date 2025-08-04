from django.urls import path, include
from . import views

urlpatterns = [
  path("register", views.register_customer, name="register_customer"),
  path("view_loan/<int:loan_id>", views.view_loan, name="view_loan"),
  path("view_loans/<int:customer_id>", views.view_loans, name="view_loans"),
]