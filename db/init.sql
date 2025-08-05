\c credit_approval_system

create table customer (
  customer_id serial primary key,
  first_name varchar, 
  last_name varchar, 
  age int, 
  phone_number varchar,
  monthly_salary decimal(20, 2),
  approved_limit decimal(20, 2)
);

create table loan (
  customer_id int,
  loan_id serial primary key,
  loan_amount decimal(20, 2),
  tenure int,
  interest_rate decimal(20,2),
  monthly_repayment decimal(20, 2),
  emis_paid_on_time int,
  date_of_approval date,
  end_date date
);
