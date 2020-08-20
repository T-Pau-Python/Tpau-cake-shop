import json
import csv
import copy
import random
from math import floor

   

starting_conditions = {
    "month": "",
    "number_of_employees": 2,
    "number_of_ovens": 1,
    "rental_space_cost": 1000,
    "rental_oven_cost": 100,
    "oven_capacity": 30000,
    "capital": 250000,
    "ingredient_cost_per_doughnut": 0.5,
    "marketing_cost": 200,
    "doughnut_sell_price": 3.5,
    "doughnuts_per_person": 6,
    "footfall": 30000,
    "per_employee_monthly_cost": 3000,
    "monthly_balance": 0,
    "revenue": 0
    
    #"business_cost_min": 5000, 
    #"business_cost_max": 15000,
}

variables = {
    #"ingredient_cost_per_product" : 0.99


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

# still need to define the actual sold number bought cannot be more than the number we can sell. 
# We’ll begin with one oven, and if demand of ‘nuts is greater than 20% of our maximum number we can sell, we’d rent an additional oven. Our current rental space is infinite.

def run_month(conditions, month):    
    conditions["month"] = month

    # proportion of footfall that will buy
    conditions["will_buy"] = conditions["footfall"] * random.uniform(0.7, 1.0)

    # nuts people could buy (demand), based on proportion that will buy * how many they buy on average
    conditions["demand_that_month"] = conditions["will_buy"] * conditions["doughnuts_per_person"]

    # The number of ‘nuts that we can sell
    # check def of "doughnuts_made_monthly". delete proportions too. 
    conditions["doughnuts_capacity_monthly"] = conditions["number_of_ovens"] * conditions["oven_capacity"]
    
    # We’ll begin with one oven, and if demand is +6000 of capicity, then new oven
    conditions["demand_v_capacity"] = conditions["demand_that_month"] - conditions["doughnuts_capacity_monthly"]

    # The actual number sold per month.
    if conditions["demand_v_capacity"] > conditions["doughnuts_capacity_monthly"]:
        conditions["actual_sold_monthly"] = conditions["doughnuts_capacity_monthly"]
    else:
        conditions["actual_sold_monthly"] = conditions["demand_that_month"]

    #Tpau calculates margin per product
    conditions["margin_per_doughnut"] = conditions["doughnut_sell_price"] - conditions["ingredient_cost_per_doughnut"]
    #Tpau calculates Turnover aka how much profit you make per nut x nuts sold QUESTION do the two turnover conditions need to be separate or can we use order of operations ()
    conditions["margin_doughnuts_monthly"] = conditions["margin_per_doughnut"] * conditions["actual_sold_monthly"]

    #Tpau revenueeee
    conditions["revenue"] += (conditions["actual_sold_monthly"] * conditions["doughnut_sell_price"])

    #Tpau caulculates monthly wages
    conditions["monthly_wages"] = conditions["per_employee_monthly_cost"] * conditions["number_of_employees"]
    #Tpau caulculates monthly oven cost
    conditions["total_monthly_oven_cost"] = conditions["rental_oven_cost"] * conditions["number_of_ovens"]

    #Tpau calculates total fixed costs
    conditions["total_fixed_costs"] = conditions["monthly_wages"] + conditions["rental_space_cost"] + conditions["total_monthly_oven_cost"] + conditions["marketing_cost"]

    #Tpau calculates balance 
    conditions["monthly_balance"] = conditions["margin_doughnuts_monthly"] - conditions["total_fixed_costs"]

    # how do we apply oven to the next month, so that costs and capacity increase that month too? 
    if conditions["demand_v_capacity"] > 6000: 
        print("new oven purchased")
        conditions["number_of_ovens"] += 1


    #conditions["capital"] += conditions["monthly_balance"]


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