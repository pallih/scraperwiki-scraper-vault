import scraperwiki
import lxml.html           
from urlparse import urljoin

print "1"
process_existing = False

def scrape_recipe_list(url) :
    
    print "Scraping " + url

    html = scraperwiki.scrape(page)
    
    root = lxml.html.fromstring(html)
    
    recipes = root.cssselect("#the-collection li")

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
        
        hrecipe_element = root.cssselect(".hrecipe")[0]
        hrecipe = lxml.html.tostring(hrecipe_element)
    
        print hrecipe
    
        recipe_name = hrecipe_element.cssselect(".fn")[0].text_content()
        ingredients = hrecipe_element.cssselect("#ingredients .ingredient")
    
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

def scrape_dishes_az() :
    print "Scraping dishes a-z"
    
    #For a-z - 97, 122
    for i in range(97, 122):

        #print i , chr(i) 
        page = "http://www.bbc.co.uk/food/dishes/by/letter/" + chr(i)
        
        print "Scraping page : " + page

        html = scraperwiki.scrape(page)
        
        root = lxml.html.fromstring(html)
        
        recipe_categories = root.cssselect(".resource.food")

        for category in recipe_categories:
        
            recipes_link = category.cssselect("a")[0]
            category_name = recipes_link.text_content()
        
            recipes_url_relative = recipes_link.attrib.get('href')
        
            recipes_url = urljoin(page, recipes_url_relative)
        
            print recipes_url, category_name

            category_model = { "url" : recipes_url, "name" : category_name }
            
            scraperwiki.sqlite.save(unique_keys=["url"], table_name="categories", data=category_model)

            html = scraperwiki.scrape(recipes_url)
            
            root = lxml.html.fromstring(html)
            
            recipes = root.cssselect(".resource-list li")
            
            print str(len(recipes)) + " found"
    
            for category in recipe_categories:
            
                process_recipe_list(page, recipes)


        
page = "http://www.bbc.co.uk/food/collections/slow_cooker_recipes"
print "2"
scrape_recipe_list(page)
#scrape_dishes_az()