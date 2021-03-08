from selenium import webdriver
import time
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import json
import urllib.request
import pickle
import uuid
import os

BASE_URL = "https://www.archanaskitchen.com"
GLOBAL_OBJECT = []
RECIPE_COUNTER = 0

def scroll_until_end(time_end = 300):
    a = datetime.now()
    b = a
    SCROLL_PAUSE_TIME = 4
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True and (b-a).seconds < time_end:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        b = datetime.now()
def scrape_each_post(each_post):
    try:
        link = each_post.find('div', class_="caption").find('a', class_="recipe-title")['href']
        final_link = BASE_URL + link
        r2 = requests.get(final_link, timeout = 5)
        if r2.status_code == 200:
            inner_soup = BeautifulSoup(r2.content, 'html.parser')
            title = inner_soup.find('h1', class_ = "recipe-title").get_text()
            recipe_image_url = BASE_URL + inner_soup.find('div', class_='recipe-image').find('img')['src']
            ingredients = []
            procedure = []
            cook_time = inner_soup.find('span', attrs={"itemprop": "totalTime"}).find('p').get_text()
            description = inner_soup.find('div', class_ = "recipedescription").get_text().strip()
            for each_list in inner_soup.find('div', class_="recipeingredients").find_all('li'):
                item = each_list.find('span', class_="ingredient_name").get_text().strip()
                quantity = each_list.get_text().strip()
                quantity = quantity[:quantity.find(item)].strip()
                ingredients.append([item, quantity])
            for each_step in inner_soup.find('div', class_="recipeinstructions").find_all('li'):
                procedure.append(each_step.get_text().strip())
            print("Retreived data for", title)
            return {
                    "title": title,
                    "image_url": recipe_image_url,
                    "description": description,
                    "cook_time": cook_time,
                    "ingredients": ingredients,
                    "procedure": procedure
                }
        else:
            print("Bad Request")
            return None
    except Exception as e:
        print("Error occured", e)
        return None
def add_to_global_object(each_post):
    try:
        global GLOBAL_OBJECT
        resp = scrape_each_post(each_post)
        if resp is None:
            return False
        else:
            image_link = resp['image_url']
            image_path = str(uuid.uuid4()) + "." + image_link.split(".")[-1]
            urllib.request.urlretrieve(image_link, os.path.join("images", image_path))
            resp['image_url'] = image_path
            GLOBAL_OBJECT.append(resp)
            return True
    except Exception as e1:
        print("Error occured", e1)
        return False
def main_scrape(source):
    global RECIPE_COUNTER
    soup = BeautifulSoup(source, 'html.parser')
    blog_posts = soup.find_all('div', class_ = "blogRecipe")
    for each_post in blog_posts:
        resp = add_to_global_object(each_post)
        if resp:
            RECIPE_COUNTER += 1

driver = webdriver.Chrome(executable_path=r"chromedriver.exe")
driver.get('https://www.archanaskitchen.com/recipes/page-2?output=774')
_ = input()
scroll_until_end()
main_scrape(driver.page_source)

with open('data.pickle', 'wb') as handle:
    pickle.dump(GLOBAL_OBJECT, handle, protocol=pickle.HIGHEST_PROTOCOL)
print(GLOBAL_OBJECT)
print(RECIPE_COUNTER)
driver.close()