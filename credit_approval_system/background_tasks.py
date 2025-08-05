from cas_api.tasks import load_customers, load_loans

load_customers.delay()
load_loans.delay()