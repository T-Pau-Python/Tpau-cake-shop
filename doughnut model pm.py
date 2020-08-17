import json
import csv
import copy
import random
from math import floor

   

starting_conditions = {
    "capital": 250000,
    "rental_space_cost" : 1000,
    "rental_oven_cost" : 100,
    "oven_capacity" : 30000,
    "ingredient_cost_per_product": 0.5,
    "marketing_cost": 200,
    "product_sell_price" : 3.5, 
    "number_of_employees" : 2,
    "footfall" : 10000,
    "doughnuts_sold_per_acquired_customer" : 1,
    "per_employee_monthly_cost" : 3000,
    "employee_min_jobs_per_month" : 2,
    "employee_max_jobs_per_month" : 4,
    "new_customers" : 0,
    "total_monthly_costs" : 0,
    "monthly_costs" : {},
    "monthly_balance" : 0,
    "revenue" : 0 ,
    "month" : "",
    #"business_cost_min": 5000, 
    #"business_cost_max": 15000,
}

months = [
        "Jan 21","Feb 21","Mar 21","Apr 21",
        "May 21","Jun 21","Jul 21","Aug 21",
        "Sep 21","Oct 21","Nov 21","Dec 21",
        "Jan 22","Feb 22","Mar 22","Apr 22",
        "May 22","Jun 22","Jul 22","Aug 22",
        "Sep 22","Oct 22","Nov 22","Dec 22"
        ]

monthy_output = []

def run_month(conditions, month):    
    conditions["month"] = month
    
    #Tpau calculates how many doughnuts sold
    doughnuts_sold_monthly = conditions["footfall"] * conditions["number_of_employees"]

    #Tpau calculates margin per product
    margin_per_product = conditions["product_sell_price"] - conditions["ingredient_cost_per_product"]

    #Tpau caulculates monthly wages
    monthly_wages = conditions["per_employee_monthly_cost"] * conditions["number_of_employees"]

    #Tpau calculates total cost
    total_costs = monthly_wages + conditions["rental_space_cost"] + conditions["rental_oven_cost"] + conditions["ingredient_cost_per_product"] * doughnuts_sold_monthly

    #Tpau calculates Turnover
    turnover = margin_per_product * doughnuts_sold_monthly

    #Tpau calculates balance 
    monthly_balance = turnover - total_costs

    # Put the employees to work and calculate revenue
    doughnut_capacity = conditions["oven_capacity"] * conditions["number_of_employees"]
    revenue = 0
    
    # Calculate monthly costs
    total_monthly_costs = 0
    for cost in conditions["monthly_costs"].values():
        total_monthly_costs += cost
    conditions["total_monthly_costs"] = total_monthly_costs


    print(print(json.dumps(conditions, indent=4, sort_keys=True)))
    return conditions

output = []
input_conditions = starting_conditions
for month in months:
    input_conditions = run_month(input_conditions, month)
    output.append(copy.deepcopy(input_conditions))

with open('doughnutoutput.csv', 'w', encoding='utf8', newline='') as output_file:
    fc = csv.DictWriter(output_file, fieldnames=output[0].keys())
    fc.writeheader()
    fc.writerows(output)