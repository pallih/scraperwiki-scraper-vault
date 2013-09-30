import scraperwiki 
import mechanize
import lxml.html
import re
import urlparse

base_url = "http://store.steampowered.com/search/?specials=1&cc=us"
prev_urls = []
prev_urls.append(base_url)

#Parameters:
#How do you want to limit your result
percentage_threshold = 5.0
price_threshold = 9.0
game_list = ['Post Apocalyptic Mayhem']

#Used to turn of the use of parameters and return all results
PARAMETERSOFF = True

br = mechanize.Browser()

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

def scrape_page_and_look_for_next(url):
    #br = mechanize.Browser()
    response = br.open(url)
    root = lxml.html.fromstring(response.read())
    scrape(root)
    next_link = root.cssselect("div.search_pagination_right a")
    next_link_url = next_link[-1].attrib.get('href')
    if (next_link and str(next_link_url) not in prev_urls):
        prev_urls.append(next_link_url)
        next_url = urlparse.urljoin(base_url, next_link_url)
        scrape_page_and_look_for_next(next_url + "&cc=us") #Need to add the location here, should fix this :)
    

def scrape(root):
    for title in root.cssselect("div#search_result_container a"):
        if len(title) > 5:
            #Getting all the info using some messy selections and splits :)    
            
            #The first div inside the result_container includes both prices. The old price
            #is inside <strike></strike>
            oldprice = title[0].cssselect("strike")[0].text_content()

            #get the new price by spliting on the old and new price
            price = title[0].text_content().split(oldprice)[1]

            oldprice = re.sub('[^0-9.]','',oldprice)
            price = re.sub('[^0-9.]','',price)

            #the link is the href attribute
            link = title.get('href')

            #the images is in the 5th div 
            img = title[4].cssselect("img")[0].get('src')

            # the release date is in the 4th
            reldate = title[3].text_content()

            #The actual name of the game is in the 6th div
            title = title[5].cssselect('h4')[0].text_content()
            
            #Get the game description by following the game link
            game_desc = dep_scrape(link)
            
            #check against the parameters
            if percentage_test(float(price),float(oldprice)) and price_threshold_test(float(price)) and check_game_list(title) or PARAMETERSOFF:
                data = {
                    'oldprice' : oldprice.encode('utf-8'),
                    'price' : price.encode('utf-8'),
                    'releasedate' : reldate.encode('utf-8'),
                    'title' : title.encode('utf-8'),
                    'link' : link.encode('utf-8'),
                    'img_link' : img.encode('utf-8'),
                    'game_desc' : game_desc.encode('utf-8')
                }
                scraperwiki.sqlite.save(["link"], data)

#Follow the link to each game and try to extract a description of the game                        
def dep_scrape(game_url):
    response = br.open(game_url)
    root = lxml.html.fromstring(response.read())
    game_desc = root.cssselect("div#game_area_description p")
    game_desc_text = ""
    for p in game_desc:
        game_desc_text += p.text_content()
    return game_desc_text
    

scrape_page_and_look_for_next(base_url)


import scraperwiki 
import mechanize
import lxml.html
import re
import urlparse

base_url = "http://store.steampowered.com/search/?specials=1&cc=us"
prev_urls = []
prev_urls.append(base_url)

#Parameters:
#How do you want to limit your result
percentage_threshold = 5.0
price_threshold = 9.0
game_list = ['Post Apocalyptic Mayhem']

#Used to turn of the use of parameters and return all results
PARAMETERSOFF = True

br = mechanize.Browser()

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

def scrape_page_and_look_for_next(url):
    #br = mechanize.Browser()
    response = br.open(url)
    root = lxml.html.fromstring(response.read())
    scrape(root)
    next_link = root.cssselect("div.search_pagination_right a")
    next_link_url = next_link[-1].attrib.get('href')
    if (next_link and str(next_link_url) not in prev_urls):
        prev_urls.append(next_link_url)
        next_url = urlparse.urljoin(base_url, next_link_url)
        scrape_page_and_look_for_next(next_url + "&cc=us") #Need to add the location here, should fix this :)
    

def scrape(root):
    for title in root.cssselect("div#search_result_container a"):
        if len(title) > 5:
            #Getting all the info using some messy selections and splits :)    
            
            #The first div inside the result_container includes both prices. The old price
            #is inside <strike></strike>
            oldprice = title[0].cssselect("strike")[0].text_content()

            #get the new price by spliting on the old and new price
            price = title[0].text_content().split(oldprice)[1]

            oldprice = re.sub('[^0-9.]','',oldprice)
            price = re.sub('[^0-9.]','',price)

            #the link is the href attribute
            link = title.get('href')

            #the images is in the 5th div 
            img = title[4].cssselect("img")[0].get('src')

            # the release date is in the 4th
            reldate = title[3].text_content()

            #The actual name of the game is in the 6th div
            title = title[5].cssselect('h4')[0].text_content()
            
            #Get the game description by following the game link
            game_desc = dep_scrape(link)
            
            #check against the parameters
            if percentage_test(float(price),float(oldprice)) and price_threshold_test(float(price)) and check_game_list(title) or PARAMETERSOFF:
                data = {
                    'oldprice' : oldprice.encode('utf-8'),
                    'price' : price.encode('utf-8'),
                    'releasedate' : reldate.encode('utf-8'),
                    'title' : title.encode('utf-8'),
                    'link' : link.encode('utf-8'),
                    'img_link' : img.encode('utf-8'),
                    'game_desc' : game_desc.encode('utf-8')
                }
                scraperwiki.sqlite.save(["link"], data)

#Follow the link to each game and try to extract a description of the game                        
def dep_scrape(game_url):
    response = br.open(game_url)
    root = lxml.html.fromstring(response.read())
    game_desc = root.cssselect("div#game_area_description p")
    game_desc_text = ""
    for p in game_desc:
        game_desc_text += p.text_content()
    return game_desc_text
    

scrape_page_and_look_for_next(base_url)


