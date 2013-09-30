import scraperwiki
import lxml.html           

def process_ingredient(element) :
    
    ingredient = element.text_content() #lxml.html.text_content(
    ingredient_model = { "name" : ingredient }
    
    print ingredient

    scraperwiki.sqlite.save(unique_keys=["name"], table_name="ingredients", data=ingredient_model)

    return ingredient_model
    

def scrape_recipe(recipe) :

    html = scraperwiki.scrape(recipe["url"])
    root = lxml.html.fromstring(html)
    

    hrecipe_element = root.cssselect(".hRecipe")[0]
    hrecipe = lxml.html.tostring(hrecipe_element)

    print hrecipe

    ingredients = hrecipe_element.cssselect(".ingredients .ingredient")

    print str(len(ingredients)) + " ingredients"

    for ingredient in ingredients:
        recipe["ingredients"].append(process_ingredient(ingredient))

    recipe["raw_hrecipe"] = hrecipe

    scraperwiki.sqlite.save(unique_keys=["url"], table_name="recipes", data=recipe)


html = scraperwiki.scrape("http://allrecipes.com/recipes/ViewAll.aspx")

root = lxml.html.fromstring(html)

recipes = root.cssselect(".recipes")

print str(len(recipes)) + " recipes"

for recipe in recipes:
    recipe_div = recipe.cssselect(".rectitlediv")[0]
    
    recipe_title = recipe_div.cssselect("h3")[0]

    recipe_link = recipe_title.cssselect("a")[0]

    recipe_name = recipe_title.text_content()
    recipe_url = recipe_link.attrib.get('href')

    print recipe_name
    print recipe_url

    recipe_model = { "url" : recipe_url, "name" : recipe_name, "raw_hrecipe" : "", "processed_hrecipe" : "", "ingredients" : list() }

    scrape_recipe(recipe_model)    import scraperwiki
import lxml.html           

def process_ingredient(element) :
    
    ingredient = element.text_content() #lxml.html.text_content(
    ingredient_model = { "name" : ingredient }
    
    print ingredient

    scraperwiki.sqlite.save(unique_keys=["name"], table_name="ingredients", data=ingredient_model)

    return ingredient_model
    

def scrape_recipe(recipe) :

    html = scraperwiki.scrape(recipe["url"])
    root = lxml.html.fromstring(html)
    

    hrecipe_element = root.cssselect(".hRecipe")[0]
    hrecipe = lxml.html.tostring(hrecipe_element)

    print hrecipe

    ingredients = hrecipe_element.cssselect(".ingredients .ingredient")

    print str(len(ingredients)) + " ingredients"

    for ingredient in ingredients:
        recipe["ingredients"].append(process_ingredient(ingredient))

    recipe["raw_hrecipe"] = hrecipe

    scraperwiki.sqlite.save(unique_keys=["url"], table_name="recipes", data=recipe)


html = scraperwiki.scrape("http://allrecipes.com/recipes/ViewAll.aspx")

root = lxml.html.fromstring(html)

recipes = root.cssselect(".recipes")

print str(len(recipes)) + " recipes"

for recipe in recipes:
    recipe_div = recipe.cssselect(".rectitlediv")[0]
    
    recipe_title = recipe_div.cssselect("h3")[0]

    recipe_link = recipe_title.cssselect("a")[0]

    recipe_name = recipe_title.text_content()
    recipe_url = recipe_link.attrib.get('href')

    print recipe_name
    print recipe_url

    recipe_model = { "url" : recipe_url, "name" : recipe_name, "raw_hrecipe" : "", "processed_hrecipe" : "", "ingredients" : list() }

    scrape_recipe(recipe_model)    