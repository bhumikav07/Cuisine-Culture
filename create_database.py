import sqlite3
import json
import pickle
from database_operations import *

create_table()

def add_row(data):
    food_id = insert_into_food(data['title'], data['description'], data['cook_time'], " ".join(data['procedure']), data['image_url'])
    for item, quantity in data['ingredients']:
        ingredient_exists = get_ingredient_details(ingredient_name_data= item)
        if len(ingredient_exists) > 0:
            ingredient_id = ingredient_exists[0][0]
        else:
            ingredient_id = insert_into_ingredient(item)
        insert_into_ingredient_food(food_id, ingredient_id, quantity)
    print("Inserted", data['title'])

f = open("data.pickle", "rb")
DATA = pickle.load(f)
f.close()
"""
[
{
    "title": .....,
    "description": ....,
    "cook_time": .....
    "procedure": ["kshcgkah alchcs"],
    "ingredients": [(item, quantity), (item, quantity)],
    "image_url": ........
}, ..........
]
"""
for each_row in DATA:
    add_row(each_row)
