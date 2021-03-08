import numpy as np
from database_operations import *

def get_priority_scores(x, item_name_id = 2, item_type_id = 1):
    priority_0 = set([item[item_name_id] for item in x[-1] if item[item_type_id] == 0])
    priority_1 = set([item[item_name_id] for item in x[-1] if item[item_type_id] == 1])
    priority_2 = set([item[item_name_id] for item in x[-1] if item[item_type_id] == 2])
    priority_3 = set([item[item_name_id] for item in x[-1] if item[item_type_id] == 3])
    return [priority_0, priority_1, priority_2, priority_3]

def initialise_food_details():
    food_details = get_food_details(ingredients=True)
    for i in range(len(food_details)):
        x = list(food_details[i])
        x.append(get_priority_scores(x))
        food_details[i] = x
    return food_details
