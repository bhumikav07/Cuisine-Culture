import sqlite3
import json

def create_table():
    conn = sqlite3.connect('recipes.db')
    create_ingredients_query = '''
        CREATE TABLE IF NOT EXISTS ingredient(
            ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredient_name TEXT,
            ingredient_type INT DEFAULT 0
        );
    '''
    conn.execute(create_ingredients_query)
    create_food_query = '''
        CREATE TABLE IF NOT EXISTS food(
            food_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            total_time TEXT,
            procedure TEXT,
            image_link TEXT
        );
    '''
    conn.execute(create_food_query)
    create_ingredient_food_query = '''
        CREATE TABLE IF NOT EXISTS ingredient_food(
            ingredient_food_id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_id INT REFERENCES food(food_id),
            ingredient_id INT REFERENCES ingredient(ingredient_id),
            quantity TEXT
        );
    '''
    conn.execute(create_ingredient_food_query)
    conn.close()

def insert_into_food(title, description, total_time, procedure, image_link):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    insert_food_query = f'''
        INSERT INTO food(title, description, total_time, procedure, image_link) VALUES(?, ?, ?, ?, ?);
    '''
    cursor.execute(insert_food_query, (title, description, total_time, procedure, image_link))
    food_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return food_id

def insert_into_ingredient(ingredient_name):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    insert_ingredient_query = f'''
        INSERT INTO ingredient(ingredient_name) VALUES(?);
    '''
    cursor.execute(insert_ingredient_query, (ingredient_name, ))
    ingredient_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return ingredient_id

def insert_into_ingredient_food(food_id, ingredient_id, quantity):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    insert_ingredient_food_query = f'''
        INSERT INTO ingredient_food(food_id, ingredient_id, quantity) VALUES(?, ?, ?);
    '''
    cursor.execute(insert_ingredient_food_query, (food_id, ingredient_id, quantity))
    ingredint_food_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return ingredint_food_id
    
def get_food_details(food_id = None, title = True, description = True, image_link = True, total_time = True, procedure = False, ingredients = False):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    query = "SELECT food_id, "
    if title:
        query += "title, "
    if description:
        query += "description, "
    if image_link:
        query += "image_link,  "
    if total_time:
        query += "total_time, "
    if procedure:
        query += "procedure, "
    query = query[:-2] + " FROM food "
    if food_id is not None:
        query += f"WHERE food_id = ? "
        cursor.execute(query, (food_id, ))
    else:
        cursor.execute(query)
    data = cursor.fetchall()
    if ingredients:
        for i in range(len(data)):
            food_id = data[i][0]
            ingredients_query = f'''
                SELECT i.ingredient_id AS ingredient_id, ingredient_type, ingredient_name, quantity FROM ingredient i, ingredient_food if WHERE if.ingredient_id = i.ingredient_id AND if.food_id = ?
            '''
            cursor.execute(ingredients_query, (food_id, ))
            data[i] = list(data[i])
            data[i].append(cursor.fetchall())
    conn.close()
    return data

def get_ingredient_details(ingredient_id = None, ingredient_name = True, ingredient_name_data = None, ingredient_type = True):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    query = "SELECT ingredient_id, "
    if ingredient_name:
        query += "ingredient_name, "
    if ingredient_type:
        query += "ingredient_type, "
    query = query[:-2] + " FROM ingredient "
    if ingredient_id is not None:
        query += f"WHERE ingredient_id = ?"
        cursor.execute(query, (ingredient_id, ))
    elif ingredient_name_data is not None:
        query += f"WHERE ingredient_name = ?"
        cursor.execute(query, (ingredient_name_data, ))
    else:
        cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data
    
def update_ingredient_type(ingredient_type, ingredient_id): 
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    query = '''
        UPDATE ingredient SET ingredient_type = ? WHERE ingredient_id = ?
    '''
    cursor.execute(query, (ingredient_type, ingredient_id))
    conn.commit()
    conn.close()
    return True
