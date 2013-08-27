# MyFitnessPal Public Food Diary Scraper
# This Scraper is meant to be used for self-quantifying, personal science, journalism, or public health research ONLY

"""
Data Store Information

entry_date: text
username: text
meal_name: text
food_description: text
food_brand: text
quantity: real
weight_name: text
calories: int
total_fat: real
saturated_fat: real
polyunsaturated_fat: real
monounsaturated_fat: real
trans_fat: real
cholesterol: real
sodium: real
potassium: real
total_carbs: real
dietary_fiber: real
sugars: real
protein: real
vitamin_a_dv: real
vitamin_c_dv: real
calcium_dv: real
iron_dv: real
"""


# Import Libraries
import scraperwiki
import datetime
from datetime import date, timedelta
import lxml.html


# User & URL Information
username = "JacobJWalker"
base_url = "http://www.myfitnesspal.com/food/diary/"


# Date Range of Scraper
start_date = datetime.date(2013, 5, 5)
end_date = datetime.date.today()
next_date = timedelta(1)


# Load myfitnesspal.db SQLite database, as saved on Android app
# NOTE: This is a planned future feature of the scraper



# Crawl Through MyFitnessPal Food Diary Entries, Getting and Storing Basic Nutrition Data

d = start_date
unique_key = 0
while d <= end_date:
    url = base_url + username + "?date=" + str(d)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    for tr in root.cssselect("tr"):
        tds = tr.cssselect("td")


        # Checks to see if the table row contains a meal name, and sets the variable meal to the name, to be used until a new meal name is found
        if tr.attrib == {'class': 'meal_header'}:
            meal = tds[0].text_content()

        # Checks to see if the table row contains a food entry and puts this data into the data variable
        if "-" in tds[0].text_content(): #Food Entries always have a "-" seperating Brand from Description

            unique_key = unique_key + 1
            full_food_description = tds[0].text_content().strip()
            data = {
                'id' : unique_key,
                'date' : str(d),
                'meal_name' : meal,
                'full_food_description' : full_food_description,
                'food_brand' : full_food_description[0:full_food_description.find(" - ")],
                'food_description' : full_food_description[full_food_description.find(" - ")+3:full_food_description.rfind(", ")],
                'full_quantity' : full_food_description[full_food_description.rfind(", ")+2:],
                'calories' : int(tds[1].text_content().replace(',', '')),
                'total_carbs' : int(tds[2].text_content().replace(',', '')),
                'total_fat' : int(tds[3].text_content().replace(',', '')),
                'protein' : int(tds[4].text_content().replace(',', '')),
                'sodium' : int(tds[5].text_content().replace(',', '')),
                'sugar' : int(tds[6].text_content().replace(',', ''))
            }
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)

    d = d + next_date


# Get Full Nutrition Data from MyFitnessPal Food Database
# NOTE: This is a planned future feature of the scraper

"""
MyFitnessPal Food Database Data Entry
-------------------------------------
1. Enter Entry into "Search our food database by name:"
2. Select Food from "Matching Foods:"
3. Select Serving Size and Type of Serving from "Servings:"


MyFitnessPal Food Database Column Layout
----------------------------------------
Calories              Sodium
Total Fat             Potassium
Saturated             Total Carbs
Polyunsaturated       Dietary Fiber
Monounsaturated       Sugars
Trans                 Protein
Cholesterol           
Vitamin A             Calcium
Vitamin C             Iron

"""


# MyFitnessPal Public Food Diary Scraper
# This Scraper is meant to be used for self-quantifying, personal science, journalism, or public health research ONLY

"""
Data Store Information

entry_date: text
username: text
meal_name: text
food_description: text
food_brand: text
quantity: real
weight_name: text
calories: int
total_fat: real
saturated_fat: real
polyunsaturated_fat: real
monounsaturated_fat: real
trans_fat: real
cholesterol: real
sodium: real
potassium: real
total_carbs: real
dietary_fiber: real
sugars: real
protein: real
vitamin_a_dv: real
vitamin_c_dv: real
calcium_dv: real
iron_dv: real
"""


# Import Libraries
import scraperwiki
import datetime
from datetime import date, timedelta
import lxml.html


# User & URL Information
username = "JacobJWalker"
base_url = "http://www.myfitnesspal.com/food/diary/"


# Date Range of Scraper
start_date = datetime.date(2013, 5, 5)
end_date = datetime.date.today()
next_date = timedelta(1)


# Load myfitnesspal.db SQLite database, as saved on Android app
# NOTE: This is a planned future feature of the scraper



# Crawl Through MyFitnessPal Food Diary Entries, Getting and Storing Basic Nutrition Data

d = start_date
unique_key = 0
while d <= end_date:
    url = base_url + username + "?date=" + str(d)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    for tr in root.cssselect("tr"):
        tds = tr.cssselect("td")


        # Checks to see if the table row contains a meal name, and sets the variable meal to the name, to be used until a new meal name is found
        if tr.attrib == {'class': 'meal_header'}:
            meal = tds[0].text_content()

        # Checks to see if the table row contains a food entry and puts this data into the data variable
        if "-" in tds[0].text_content(): #Food Entries always have a "-" seperating Brand from Description

            unique_key = unique_key + 1
            full_food_description = tds[0].text_content().strip()
            data = {
                'id' : unique_key,
                'date' : str(d),
                'meal_name' : meal,
                'full_food_description' : full_food_description,
                'food_brand' : full_food_description[0:full_food_description.find(" - ")],
                'food_description' : full_food_description[full_food_description.find(" - ")+3:full_food_description.rfind(", ")],
                'full_quantity' : full_food_description[full_food_description.rfind(", ")+2:],
                'calories' : int(tds[1].text_content().replace(',', '')),
                'total_carbs' : int(tds[2].text_content().replace(',', '')),
                'total_fat' : int(tds[3].text_content().replace(',', '')),
                'protein' : int(tds[4].text_content().replace(',', '')),
                'sodium' : int(tds[5].text_content().replace(',', '')),
                'sugar' : int(tds[6].text_content().replace(',', ''))
            }
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)

    d = d + next_date


# Get Full Nutrition Data from MyFitnessPal Food Database
# NOTE: This is a planned future feature of the scraper

"""
MyFitnessPal Food Database Data Entry
-------------------------------------
1. Enter Entry into "Search our food database by name:"
2. Select Food from "Matching Foods:"
3. Select Serving Size and Type of Serving from "Servings:"


MyFitnessPal Food Database Column Layout
----------------------------------------
Calories              Sodium
Total Fat             Potassium
Saturated             Total Carbs
Polyunsaturated       Dietary Fiber
Monounsaturated       Sugars
Trans                 Protein
Cholesterol           
Vitamin A             Calcium
Vitamin C             Iron

"""


# MyFitnessPal Public Food Diary Scraper
# This Scraper is meant to be used for self-quantifying, personal science, journalism, or public health research ONLY

"""
Data Store Information

entry_date: text
username: text
meal_name: text
food_description: text
food_brand: text
quantity: real
weight_name: text
calories: int
total_fat: real
saturated_fat: real
polyunsaturated_fat: real
monounsaturated_fat: real
trans_fat: real
cholesterol: real
sodium: real
potassium: real
total_carbs: real
dietary_fiber: real
sugars: real
protein: real
vitamin_a_dv: real
vitamin_c_dv: real
calcium_dv: real
iron_dv: real
"""


# Import Libraries
import scraperwiki
import datetime
from datetime import date, timedelta
import lxml.html


# User & URL Information
username = "JacobJWalker"
base_url = "http://www.myfitnesspal.com/food/diary/"


# Date Range of Scraper
start_date = datetime.date(2013, 5, 5)
end_date = datetime.date.today()
next_date = timedelta(1)


# Load myfitnesspal.db SQLite database, as saved on Android app
# NOTE: This is a planned future feature of the scraper



# Crawl Through MyFitnessPal Food Diary Entries, Getting and Storing Basic Nutrition Data

d = start_date
unique_key = 0
while d <= end_date:
    url = base_url + username + "?date=" + str(d)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    for tr in root.cssselect("tr"):
        tds = tr.cssselect("td")


        # Checks to see if the table row contains a meal name, and sets the variable meal to the name, to be used until a new meal name is found
        if tr.attrib == {'class': 'meal_header'}:
            meal = tds[0].text_content()

        # Checks to see if the table row contains a food entry and puts this data into the data variable
        if "-" in tds[0].text_content(): #Food Entries always have a "-" seperating Brand from Description

            unique_key = unique_key + 1
            full_food_description = tds[0].text_content().strip()
            data = {
                'id' : unique_key,
                'date' : str(d),
                'meal_name' : meal,
                'full_food_description' : full_food_description,
                'food_brand' : full_food_description[0:full_food_description.find(" - ")],
                'food_description' : full_food_description[full_food_description.find(" - ")+3:full_food_description.rfind(", ")],
                'full_quantity' : full_food_description[full_food_description.rfind(", ")+2:],
                'calories' : int(tds[1].text_content().replace(',', '')),
                'total_carbs' : int(tds[2].text_content().replace(',', '')),
                'total_fat' : int(tds[3].text_content().replace(',', '')),
                'protein' : int(tds[4].text_content().replace(',', '')),
                'sodium' : int(tds[5].text_content().replace(',', '')),
                'sugar' : int(tds[6].text_content().replace(',', ''))
            }
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)

    d = d + next_date


# Get Full Nutrition Data from MyFitnessPal Food Database
# NOTE: This is a planned future feature of the scraper

"""
MyFitnessPal Food Database Data Entry
-------------------------------------
1. Enter Entry into "Search our food database by name:"
2. Select Food from "Matching Foods:"
3. Select Serving Size and Type of Serving from "Servings:"


MyFitnessPal Food Database Column Layout
----------------------------------------
Calories              Sodium
Total Fat             Potassium
Saturated             Total Carbs
Polyunsaturated       Dietary Fiber
Monounsaturated       Sugars
Trans                 Protein
Cholesterol           
Vitamin A             Calcium
Vitamin C             Iron

"""


