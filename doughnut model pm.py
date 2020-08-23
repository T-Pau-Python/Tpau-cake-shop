import json
import csv
import copy
import random
from math import floor


starting_conditions = {
    "month": "",
    "number_of_employees": 2,
    "rental_space_cost": 1000,
    "rental_oven_cost": 100,
    "oven_capacity": 30000,
    "capital": 250000,
    "ingredient_cost_per_doughnut": 0.5,
    "ingredient_cost_per_cronut": 0.5,
    "marketing_cost": 200,
    "doughnut_sell_price": 3.5,
    "cronut_sell_price": 4, 
    "footfall": 10000,
    "per_employee_monthly_cost": 3000,
    "monthly_balance": 0,
    "revenue": 0,
    "doughnuts_made_monthly": 0,
    "cronuts_made_monthly": 0,
    "proportion_doughnut": 0.5,
    "proportion_cronut": 0.5,
    "employee_selling_capacity": 10000,
    "interest_in_dough": 0.7,
    "total_sales_capacity": 0,
    "total_market": 0
    
    #"business_cost_min": 5000, 
    #"business_cost_max": 15000,
}

variables = {
    "ingredient_cost_per_product" : 0.99

}


monthy_output = []

months = [
    {"month_name": "Jan", "temp": 5.2, "rainy_days": 11.1},
    {"month_name": "Feb", "temp": 5.3, "rainy_days": 8.5},
    {"month_name": "Mar", "temp": 7.6, "rainy_days": 9.3},
    {"month_name": "Apr", "temp": 9.9, "rainy_days": 8.5},
    {"month_name": "May", "temp": 13.3, "rainy_days": 8.8},
    {"month_name": "Jun", "temp": 16.4, "rainy_days": 8.2},
    {"month_name": "Jul", "temp": 18.7, "rainy_days": 7.7},
    {"month_name": "Aug", "temp": 18.5, "rainy_days": 7.5},
    {"month_name": "Sep", "temp": 15.7, "rainy_days": 8.1},
    {"month_name": "Oct", "temp": 12.0, "rainy_days": 10.8},
    {"month_name": "Nov", "temp": 8.0, "rainy_days": 10.3},
    {"month_name": "Dec", "temp": 5.5, "rainy_days": 10.2},
]


def weather_calculator(temp, rainy_days):
# do stuff here. invalid syntax here.

    # rain effect on liklihood to buy. Obvs it doesnt like this unfinished code. 
    weighting =
    return weighting

def run_month(conditions, month_dict): 
   
    #Under here, we have to handle this dictionary. it's not a string anymore
    conditions["month"] = month_dict["month"]

    weather_weighting = weather_calculator(month_dict["temp"], month_dict["rainy_days"])

    #footfall that month
    conditions["footfall_that_month"] = conditions["footfall"] * random.uniform(0.5, 0.7)

    #'nuts made
    conditions["doughnuts_made_monthly"] = conditions["proportion_doughnut"] * conditions["oven_capacity"]
    conditions["cronuts_made_monthly"] = conditions["proportion_cronut"] * conditions["oven_capacity"]
    
    #Tpau calculates how many doughnuts sold
    conditions["total_sales_capacity"] = conditions["employee_selling_capacity"] * conditions["number_of_employees"]
    conditions["total_market"] = conditions["footfall_that_month"] * conditions["interest_in_dough"]
    conditions["doughnuts_sold_monthly"] = conditions["employee_selling_capacity"] * conditions["number_of_employees"] * conditions["proportion_doughnut"]
    conditions["cronuts_sold_monthly"] = conditions["employee_selling_capacity"] * conditions["number_of_employees"] * conditions["proportion_cronut"]

    #Tpau calculates margin per product
    conditions["margin_per_doughnut"] = conditions["doughnut_sell_price"] - conditions["ingredient_cost_per_doughnut"]
    conditions["margin_per_cronut"] = conditions["cronut_sell_price"] - conditions["ingredient_cost_per_cronut"]

    #Tpau caulculates monthly wages
    conditions["monthly_wages"] = conditions["per_employee_monthly_cost"] * conditions["number_of_employees"]

    #Tpau revenueeee
    conditions["revenue"] += (conditions["doughnuts_sold_monthly"]* conditions["doughnut_sell_price"]) + (conditions["cronuts_sold_monthly"]* conditions["cronut_sell_price"])
    
    #Tpau calculates total cost
    conditions["total_costs"] = conditions["monthly_wages"] + conditions["rental_space_cost"] + conditions["rental_oven_cost"] + conditions["ingredient_cost_per_doughnut"] + conditions["ingredient_cost_per_cronut"] * conditions["doughnuts_sold_monthly"]

    #Tpau calculates Turnover aka how much profit you make per nut x nuts sold QUESTION do the two turnover conditions need to be separate or can we use order of operations ()
    conditions["turnover"] = conditions["margin_per_doughnut"] * conditions["doughnuts_sold_monthly"] + conditions["margin_per_cronut"] * conditions["cronuts_sold_monthly"]

    #Tpau calculates balance 
    conditions["monthly_balance"] = conditions["turnover"] - conditions["total_costs"]

    # Put the employees to work and calculate revenue
    conditions["doughnut_capacity"] = conditions["oven_capacity"] * conditions["number_of_employees"]
    
    conditions["capital"] += conditions["monthly_balance"]

    conditions["ingredient_cost_per_cronut"] *= variables["ingredient_cost_per_product"]
    conditions["ingredient_cost_per_doughnut"] *= variables["ingredient_cost_per_product"]

    print(print(json.dumps(conditions, indent=4, sort_keys=True)))
    return conditions


output = []
input_conditions = starting_conditions
#Now we have to iterate over a dictionary, not a list
for month in months:
    input_conditions = run_month(input_conditions, month)
    #Write the updates to ledger
    output.append(copy.deepcopy(input_conditions))

with open('doughnutoutput.csv', 'w', encoding='utf8', newline='') as output_file:
    fc = csv.DictWriter(output_file, fieldnames=output[0].keys())
    fc.writeheader()
    fc.writerows(output)