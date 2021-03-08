from flask import Flask, render_template, url_for, request
import json
from database_operations import *
from initializer import *

food_details = initialise_food_details()
app = Flask(__name__)

def get_top_matches(input_ingredients, top_n = 50):
    for ingredient_name in input_ingredients:
        input_ingredients_data = []
        temp = get_ingredient_details(ingredient_name_data=ingredient_name)
        if len(temp) > 0:
            input_ingredients_data.append(temp[0])
    priorities = get_priority_scores([input_ingredients_data], item_name_id=1, item_type_id=2)
    result = []
    for each_food in food_details:
        priority_0_score = round(len(priorities[0].intersection(each_food[-1][0])) / (len(each_food[-1][0]) + 1), 4) * 1
        priority_1_score = round(len(priorities[1].intersection(each_food[-1][1])) / (len(each_food[-1][0]) + 1), 4) * 2
        priority_2_score = round(len(priorities[2].intersection(each_food[-1][2])) / (len(each_food[-1][0]) + 1), 4) * 3
        priority_3_score = round(len(priorities[3].intersection(each_food[-1][3])) / (len(each_food[-1][0]) + 1), 4) * 4
        total_score = priority_0_score + priority_1_score + priority_2_score + priority_3_score
        result.append([total_score, each_food[0]])
    return sorted(result, reverse = True, key = lambda x: x[0])[:top_n]

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/allrecipes')
def all_recipes():
    return render_template('allrecipe.html')


@app.route('/recipe')
def recipe():
    return render_template('recipe.html')

@app.route('/update_recipe')
def update_recipe():
    return render_template('mark_ingredients.html')

@app.route('/rank_recipes', methods=['POST'])
def rank_recipes():
    data = request.form.get("data")
    data = data.split(",")
    res = get_top_matches(data) ##list of food ids
    ret_data = []
    for i in res:
        ret_data.append(get_food_details(food_id=i[1])[0])
    return json.dumps(ret_data)
    ## [[foo_id, food_title, image, descri], [foo_id, food_title, image, descri], [foo_id, food_title, image, descri]]


@app.route('/get_recipe', methods=['GET'])
def get_recipe():
    food_id = request.args.get('food_id')
    data = get_food_details(food_id=food_id, ingredients=True, procedure=True)
    return json.dumps(data[0])


@app.route('/get_all_ingredients', methods=['GET'])
def get_ingrs():
    data = get_ingredient_details(ingredient_type=False) #[[1, "TOMATO"], [2, "CARROT"]]
    data = [i[1] for i in data]
    return json.dumps(data)

@app.route('/update_type', methods=['POST'])
def get_type():
    data = get_ingredient_details()
    return json.dumps(data)

@app.route('/update_i_type', methods=['POST'])
def update_i_type():
    data = request.form.get('data')
    data = json.loads(data)
    for i_id, i_type in data:
        update_ingredient_type(i_type, i_id)
    return 1

if __name__ == "__main__":
    app.run(debug=True)
