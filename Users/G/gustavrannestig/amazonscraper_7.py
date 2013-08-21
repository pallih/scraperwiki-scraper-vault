import scraperwiki
import mechanize
import lxml.html
import urlparse
import re

base_url = "http://www.amazon.com/"
br = mechanize.Browser()

#Parameters:
#How do you want to limit your result
percentage_threshold = 5.0
price_threshold = 9.0
game_list = ["Tropico 3"]

#Used to turn of the use of parameters and return all results
PARAMETERSOFF = True

def check_game_list(title):
    for game in game_list:
        if title.lower() in game.lower() or game.lower() in title.lower():
            return True
    return False

def price_threshold_test(price):
    if price <= price_threshold:
        return True

def percentage_test(new_price, old_price):
    percentage = (old_price - new_price)/old_price
    if percentage >= percentage_threshold/100:
        return True

def navigate_to_digital_games():
    
    #Open www.amazon.com
    response = br.open(base_url)
    
    #test functionality
    #print "all forms: ", [ form.name  for form in br.forms() ]
    #the only form on page 1 'is site-search'

    #select the site search form on top of the page
    br.select_form(name='site-search')
    #print br.form

    #set the category to videogames and search with no keywords
    br["url"] = ["search-alias=videogames"]

    response = br.submit()
    
    #print response.read()

    #Test
    #print "all video-game forms: " , [form.name for form in br.forms()]

    #get the root of the response
    html = response.read()
    root = lxml.html.fromstring(html)
    
    #find the link to digital games and navigate to that
    link = find_refinement_link_2level(root,"Department", "Digital Games")    
    new_url = urlparse.urljoin(base_url, link)    
    response = br.open(new_url)
    
    #once again get the root from the response
    html = response.read()
    root = lxml.html.fromstring(html)
    print html

    #on this new page navigate to the discount page, this will now give us the page with only digital games that have a discount
    #it looks like this on the amazon page: Video Games › Digital Games › 10% Off or More
    link = find_refinement_link(root, "Discount")
    new_url = urlparse.urljoin(base_url, link)
    
    #response = br.open(new_url)

    return new_url

       
#This function runs the scrape() function on a page and then looks for the nextpage link    
def scrape_page_and_look_for_next(url):
    response = br.open(url)
    html = response.read()
    root = lxml.html.fromstring(html)
    scrape(root)
    if len(root.cssselect("a#pagnNextLink")) > 0:
        next_link = root.cssselect("a#pagnNextLink")[0].get("href")
        new_url = urlparse.urljoin(base_url, next_link)
        scrape_page_and_look_for_next(new_url)

#this function pulls out some information about the games using cssselection    
def scrape(root):
    
    for game in root.cssselect("div.result"):
        if len(game.cssselect("div.productTitle a")) > 0:
            title = game.cssselect("div.productTitle a")[0].text_content()
            link = game.cssselect("div.productTitle a")[0].get("href")
        else:
            title = "N/A"
            link = "N/A"
        
        #There are about 3 to 4 games in the loot that doesn't have a price so I just did this to
        #avoid that problem, its probably not the best way to do it though
        if len(game.cssselect("div.newPrice span")) > 0:
            price = re.sub('[^0-9.]','',game.cssselect("div.newPrice span")[0].text_content())
        else:
            price = "N/A"
        if len(game.cssselect("div.newPrice strike")) > 0:
            oldprice =  re.sub('[^0-9.]','',game.cssselect("div.newPrice strike")[0].text_content())
        else:
            oldprice = "N/A"

        #This function makes it realy slow, and I can't get it to work everytime so I leave it commented out
        #desc = dep_scrape(urlparse.urljoin(base_url,link)
        
        if len(game.cssselect("img")) > 0:
            img = game.cssselect("img")[0].get("src")
        else:
            img = "N/A"
        
        pthcheck = True
        pcheck = True
        gcheck = True
        if not PARAMETERSOFF:
            if price != "N/A":
                pthcheck =  price_threshold_test(float(price))
            if price != "N/A" and oldprice != "N/A":
                pcheck = percentage_test(float(price),float(oldprice))

            gcheck = check_game_list(title)
        
        
        if gcheck and pcheck and pthcheck or PARAMETERSOFF:
        
            data = {
                    'oldprice' : oldprice.encode('utf-8'),
                    'price' : price.encode('utf-8'),
                    'title' : title.encode('utf-8'),
                    'link' : link.encode('utf-8'),
                    'img_link' : img.encode('utf-8')
                }
            scraperwiki.sqlite.save(["link",], data)


#This function makes the scraping incredibly slow :) and seems to stall at random games everytime I test it so I leave it commented out for now
def dep_scrape(game_url):
    response = br.open(game_url)
    html = response.read()
    root = lxml.html.fromstring(html)
    desc = root.cssselect("div.productDescriptionWrapper")[0].text_content()
    return desc  

#These two functions are really messy and you could realy just go to the page and find the
 #url by hand, but I wanted to try and navigate the page as if I couldn't do that           
    
def find_refinement_link_2level(root,refinement_parameter1, refinement_parameter2):
    refinements = root.cssselect("#refinements")
    counter = 0
    for node in refinements[0]:
        counter += 1
        if node.text_content() == refinement_parameter1:
            for new_node in refinements[0][counter]:
                #print new_node.text_content()
                if refinement_parameter2 in new_node.text_content():
                    link = new_node.cssselect("a")[0].get("href")
                    return link
                    


def find_refinement_link(root,refinement_parameter):
    refinements = root.cssselect("#refinements")
    counter = 0 
    for branch in refinements[0]:
        counter += 1
        if branch.text_content() == refinement_parameter:    
            link_list = refinements[0][counter].cssselect("a")
            #10% of or more is element 0 in the list, 20% element 1 etc
            link = link_list[0].get("href")
            return link
                   

#First navigate to the page to start scraping at and then go through the pagination    
url = navigate_to_digital_games()
scrape_page_and_look_for_next(url)

    




