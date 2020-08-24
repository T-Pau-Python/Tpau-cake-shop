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
    "ingredient_cost_per_product": 0.5,
    "marketing_cost": 200,
    "doughnut_sell_price": 3.5,
    "footfall": 10000,
    "doughnuts_per_person": 6,
    "per_employee_monthly_cost": 3000,
    "monthly_balance": 0,
    "revenue": 0,
    
    #"business_cost_min": 5000, 
    #"business_cost_max": 15000,
}

variables = {
    # "ingredient_cost_per_product" : 0.99

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
    {"month_name": "Dec", "temp": 5.5, "rainy_days": 10.2}
]


def weather_calculator(temp, rainy_days):
# we also use 'weather_weighting = weather_calculator(month_dict["temp"], month_dict["rainy_days"])' below in the next section. Why do we need both?

    # temp and rain effect on number bought. Obvs it doesnt like this unfinished code. This is where we need linear regression shizzle. 
    # will it be a diff multiplier for both variables? Or combined? Can't remember our rain factor?
    
    temperature_y = -0.06667 * month_dict["temp"] + 2.5
    
    rainy_days_y = month_dict["rainy days"] / 30 * 1.3 * actual_sold_monthly

    weather_weighting = 0.6 * rainy_days_y * 0.4 * temperature_y

    return

def run_month(conditions, month_dict): 
   
    #Under here, we have to handle this dictionary. it's not a string anymore
    conditions["month"] = month_dict["month_name"]
    #This is how we've unpacked the two values 

    #TODO use this fucking variable
    weather_weighting = weather_calculator(month_dict["temp"], month_dict["rainy_days"])


    # The number of ‘nuts that we can sell
    # check def of "doughnuts_made_monthly". delete proportions too. 
    conditions["doughnuts_capacity_monthly"] = conditions["number_of_ovens"] * conditions["oven_capacity"]

    # proportion of footfall that will buy
    conditions["will_buy"] = conditions["footfall"] * random.uniform(0.7, 1.0)
    
    # nuts people could buy (demand), based on proportion that will buy * how many they buy on average
    conditions["demand_that_month"] = conditions["will_buy"] * conditions["doughnuts_per_person"]
   
    # We’ll begin with one oven, and if demand is +6000 of capicity, then new oven. this comes later in the order.
    conditions["demand_v_capacity"] = conditions["demand_that_month"] - conditions["doughnuts_capacity_monthly"]

    # The actual number sold per month
    if conditions["demand_v_capacity"] > conditions["doughnuts_capacity_monthly"]:
        conditions["actual_sold_monthly"] = conditions["doughnuts_capacity_monthly"]
    else:
        conditions["actual_sold_monthly"] = conditions["demand_that_month"]



    #Tpau calculates margin per product
    conditions["margin_per_doughnut"] = conditions["doughnut_sell_price"] - conditions["ingredient_cost_per_product"]

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

    #Tpau calculates Turnover aka how much profit you make per nut x nuts sold QUESTION do the two turnover conditions need to be separate or can we use order of operations ()
    conditions["turnover"] = conditions["margin_per_doughnut"] * conditions["actual_sold_monthly"]


    # how do we apply oven to the next month, so that costs and capacity increase that month too? 
    if conditions["demand_v_capacity"] > 6000: 
        print("new oven purchased")
        conditions["number_of_ovens"] += 1

    
    conditions["capital"] += conditions["monthly_balance"]

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