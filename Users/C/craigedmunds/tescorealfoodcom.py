import scraperwiki
import lxml.html           
from urlparse import urljoin

process_existing = False

def scrape_recipe_list(url) :
    
    print "Scraping " + url

    html = scraperwiki.scrape(url)
    
    root = lxml.html.fromstring(html)
    
    recipes = root.cssselect(".articleItem")

    process_recipe_list(url, recipes)

def process_recipe_list(url, recipes):

    print "process_recipe_list : " + str(len(recipes)) + " recipes found"
    
    for recipe in recipes :
        
        recipe_link = recipe.cssselect("a")[0]
    
        recipe_url_relative = recipe_link.attrib.get('href')
    
        recipe_url = urljoin(url, recipe_url_relative)
    
        print recipe_url

        scrape_recipe(recipe_url)

def scrape_recipe(recipe_url) :

    if not process_existing and recipe_exists(recipe_url):        

        print "Not Scraping " + recipe_url + ", already exists"

    else:

        print "Scraping " + recipe_url

        html = scraperwiki.scrape(recipe_url)
        root = lxml.html.fromstring(html)
        
        recipe_header = root.cssselect(".recipeHeader")[0]
        recipe_name = recipe_header.cssselect("h1")[0].text_content()
        ingredients = root.cssselect(".ingredientList li")
    
        print recipe_name, str(len(ingredients)) + " ingredients"
    
        recipe_model = { "url" : recipe_url, "name" : recipe_name, "ingredients" : list() }
    
        for ingredient in ingredients:
            recipe_model["ingredients"].append(process_ingredient(ingredient))
    
        scraperwiki.sqlite.save(unique_keys=["url"], table_name="recipes", data=recipe_model)    

def process_ingredient(element) :
    
    ingredient = element.text_content() #lxml.html.text_content(
    ingredient_model = { "name" : ingredient }
    
    print ingredient

    scraperwiki.sqlite.save(unique_keys=["name"], table_name="ingredients", data=ingredient_model)

    return ingredient_model

def recipe_exists (url):
    
    print "recipe_exists : " + url

    count = 0

    try:
        result = scraperwiki.sqlite.execute("select count(*) from recipes where url = ?", (url))
        count = int(result["data"][0][0])  

        #print "result : " + str(result)
        #print "result['data'] : " + str(result["data"])
        #print "result['data'][0] : " + str(result["data"][0])
        #print "result['data'][0][0] : " + str(result["data"][0][0])
    
        #print "result is list : " + str(type(result) is list)
        #print "result['data'] is list : " + str(type(result["data"]) is list)
        #print "result['data'][0][0] is list : " + str(type(result["data"][0][0]) is list)
        
        #print "Count : " + str(count)

    except scraperwiki.sqlite.SqliteError, e:
        print "Unexpected error:" + str(e)

    return count > 0
        
def scrape_recipe_results():

    print "Scraping recipe results"
    
    #246 pages at the moment
    for i in range(1, 246):

        #print i , chr(i) 
        page = "http://www.tescorealfood.com/recipes/search.html?page=" + str(i)
        
        print "Scraping page : " + page

        scrape_recipe_list(page)

scrape_recipe_results()import scraperwiki
import lxml.html           
from urlparse import urljoin

process_existing = False

def scrape_recipe_list(url) :
    
    print "Scraping " + url

    html = scraperwiki.scrape(url)
    
    root = lxml.html.fromstring(html)
    
    recipes = root.cssselect(".articleItem")

    process_recipe_list(url, recipes)

def process_recipe_list(url, recipes):

    print "process_recipe_list : " + str(len(recipes)) + " recipes found"
    
    for recipe in recipes :
        
        recipe_link = recipe.cssselect("a")[0]
    
        recipe_url_relative = recipe_link.attrib.get('href')
    
        recipe_url = urljoin(url, recipe_url_relative)
    
        print recipe_url

        scrape_recipe(recipe_url)

def scrape_recipe(recipe_url) :

    if not process_existing and recipe_exists(recipe_url):        

        print "Not Scraping " + recipe_url + ", already exists"

    else:

        print "Scraping " + recipe_url

        html = scraperwiki.scrape(recipe_url)
        root = lxml.html.fromstring(html)
        
        recipe_header = root.cssselect(".recipeHeader")[0]
        recipe_name = recipe_header.cssselect("h1")[0].text_content()
        ingredients = root.cssselect(".ingredientList li")
    
        print recipe_name, str(len(ingredients)) + " ingredients"
    
        recipe_model = { "url" : recipe_url, "name" : recipe_name, "ingredients" : list() }
    
        for ingredient in ingredients:
            recipe_model["ingredients"].append(process_ingredient(ingredient))
    
        scraperwiki.sqlite.save(unique_keys=["url"], table_name="recipes", data=recipe_model)    

def process_ingredient(element) :
    
    ingredient = element.text_content() #lxml.html.text_content(
    ingredient_model = { "name" : ingredient }
    
    print ingredient

    scraperwiki.sqlite.save(unique_keys=["name"], table_name="ingredients", data=ingredient_model)

    return ingredient_model

def recipe_exists (url):
    
    print "recipe_exists : " + url

    count = 0

    try:
        result = scraperwiki.sqlite.execute("select count(*) from recipes where url = ?", (url))
        count = int(result["data"][0][0])  

        #print "result : " + str(result)
        #print "result['data'] : " + str(result["data"])
        #print "result['data'][0] : " + str(result["data"][0])
        #print "result['data'][0][0] : " + str(result["data"][0][0])
    
        #print "result is list : " + str(type(result) is list)
        #print "result['data'] is list : " + str(type(result["data"]) is list)
        #print "result['data'][0][0] is list : " + str(type(result["data"][0][0]) is list)
        
        #print "Count : " + str(count)

    except scraperwiki.sqlite.SqliteError, e:
        print "Unexpected error:" + str(e)

    return count > 0
        
def scrape_recipe_results():

    print "Scraping recipe results"
    
    #246 pages at the moment
    for i in range(1, 246):

        #print i , chr(i) 
        page = "http://www.tescorealfood.com/recipes/search.html?page=" + str(i)
        
        print "Scraping page : " + page

        scrape_recipe_list(page)

scrape_recipe_results()