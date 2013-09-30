import scraperwiki          
import lxml.html
import uuid
import datetime

# Variables

wishlist = "2J0GVYRVJGRKG"
limit = 1.50
asins = []

# Functions

def is_cheap(price):
    if(price < limit):
        cheap = "Is going cheap!" # Text to search for within IFTTT
    elif(price == 9999999):
        cheap = "We can't get a price."
    else:
        cheap = "Is not going cheap."
    return cheap

def save(title, link, description):
    now = datetime.datetime.now()
    data = {
        "title": title,
        "link": link,
        "description": description,
        "guid": link + "&uuid=" + str(uuid.uuid1()),
        "pubDate": str(now)
    }
    scraperwiki.sqlite.save(unique_keys=['link'], data=data)
    return "Saved!"

# Get ASINs from your Amazon Wish List

url = "http://www.amazon.co.uk/wishlist/" + wishlist + "/ref=cm_wl_act_print_o?_encoding=UTF8&disableNav=1&items-per-page=2500&layout=standard-print&page=1&visitor-view=1"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
for element in root.cssselect("tbody.itemWrapper"):
    string = element.attrib["name"]
    pieces = string.split(".")
    asins.append(pieces[3])

# Process ASINs for further details

for asin in asins:
    price = 9999999
    url = "http://www.amazon.co.uk/dp/" + asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    title = root.cssselect("span[id='btAsinTitle']")[0].text_content()
    if(title.find("Kindle Edition") > 0):
        print "KINDLE " + asin
        for element in root.cssselect("div.buying input"):
            if(element.attrib["name"] == "displayedPrice"):
                price = float(element.attrib["value"])
        cheap = is_cheap(price)
    else:
        try:
            print "NOT kindle " + asin
            price = float(root.cssselect("span#actualPriceValue b")[0].text_content()[1:])
            cheap = is_cheap(price)
        except:
            print "<<<<<<<<<<<<<<<exception for " + asin
            price = 9999999
            cheap = is_cheap(price)
            
    print save(title, url, cheap)import scraperwiki          
import lxml.html
import uuid
import datetime

# Variables

wishlist = "2J0GVYRVJGRKG"
limit = 1.50
asins = []

# Functions

def is_cheap(price):
    if(price < limit):
        cheap = "Is going cheap!" # Text to search for within IFTTT
    elif(price == 9999999):
        cheap = "We can't get a price."
    else:
        cheap = "Is not going cheap."
    return cheap

def save(title, link, description):
    now = datetime.datetime.now()
    data = {
        "title": title,
        "link": link,
        "description": description,
        "guid": link + "&uuid=" + str(uuid.uuid1()),
        "pubDate": str(now)
    }
    scraperwiki.sqlite.save(unique_keys=['link'], data=data)
    return "Saved!"

# Get ASINs from your Amazon Wish List

url = "http://www.amazon.co.uk/wishlist/" + wishlist + "/ref=cm_wl_act_print_o?_encoding=UTF8&disableNav=1&items-per-page=2500&layout=standard-print&page=1&visitor-view=1"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
for element in root.cssselect("tbody.itemWrapper"):
    string = element.attrib["name"]
    pieces = string.split(".")
    asins.append(pieces[3])

# Process ASINs for further details

for asin in asins:
    price = 9999999
    url = "http://www.amazon.co.uk/dp/" + asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    title = root.cssselect("span[id='btAsinTitle']")[0].text_content()
    if(title.find("Kindle Edition") > 0):
        print "KINDLE " + asin
        for element in root.cssselect("div.buying input"):
            if(element.attrib["name"] == "displayedPrice"):
                price = float(element.attrib["value"])
        cheap = is_cheap(price)
    else:
        try:
            print "NOT kindle " + asin
            price = float(root.cssselect("span#actualPriceValue b")[0].text_content()[1:])
            cheap = is_cheap(price)
        except:
            print "<<<<<<<<<<<<<<<exception for " + asin
            price = 9999999
            cheap = is_cheap(price)
            
    print save(title, url, cheap)