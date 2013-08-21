import scraperwiki          
import lxml.html
import uuid
import datetime

# Variables

wishlist = "3URX1NVLU209E"
limit = 1.50
ratio = 0.5
asins = []

# Functions

def is_bargain(price, list_price, kindle_price):
    bargain = "Not a bargain."
    if(price == 9999999):
        bargain = "Price not found."
    elif(price < float(limit)):
        bargain = "Nice. Going cheap!"
    elif(list_price != 9999999):
        if((price / list_price) < float(ratio)):
            bargain = "Nice. Bargain!" # Text to search for within IFTTT
        elif (kindle_price != 9999999):
            if((kindle_price / list_price) < float(ratio)):
                bargain = "Nice. Kindle bargain!"
    return bargain

def save(title, link, description, price, discount, kindle_discount):
    now = datetime.datetime.now()
    if price == 9999999:
        price = ""
        discount = ""
    else:
        price = "£" + "%0.2f" % price
        discount = str(int((discount * 100))) + "%"
    if kindle_discount == 0:
        kindle_discount = ""
    else:
        kindle_discount = str(int((kindle_discount * 100))) + "%"
    data = {
        "title": title,
        "link": link,
        "description": description,
        "price": price,
        "discount": discount,
        "kindleDiscount": kindle_discount,
        "guid": link + "&uuid=" + str(uuid.uuid1()),
        "pubDate": str(now)
    }
    scraperwiki.sqlite.save(unique_keys=['link'], data=data)
    return "Saved!"

try: # Try and get ASINs from your Amazon Wish List
    url = "http://www.amazon.co.uk/wishlist/" + wishlist + "/ref=cm_wl_act_print_o?_encoding=UTF8&disableNav=1&items-per-page=2500&layout=standard-print&page=1&visitor-view=1"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for element in root.cssselect("tbody[class='itemWrapper']"):
        string = element.attrib["name"]
        pieces = string.split(".")
        asins.append(pieces[3])
except:
    print "There was an error. Did you provide a working Amazon Wish List identifier?"
    exit;

# Process ASINs for further details

for asin in asins:
    price = 9999999
    list_price = 9999999
    kindle_price = 9999999
    url = "http://www.amazon.co.uk/dp/" + asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    title = root.cssselect("span[id='btAsinTitle']")[0].text_content()
    if(title.find("Kindle Edition") > 0): # Check if this is an item for the Amazon Kindle
        for element in root.cssselect("div[class='buying'] input"):
            if(element.attrib["name"] == "displayedPrice"):
                price = float(element.attrib["value"])
        bargain = is_bargain(price, 99999999, 9999999)
    else:
        try: # Try and get the price of the item. Some items throw back garbage so the price is listed as cannot be found.
            price = float(root.cssselect("span[id='actualPriceValue'] b")[0].text_content()[1:])
        except(IndexError):
            print "Price not found for: " + title
            print "Try camelcamelcamel: http://uk.camelcamelcamel.com/product/" + asin
        try:
            list_price = float(root.cssselect("span[id='listPriceValue']")[0].text_content()[1:])
        except(IndexError):
            list_price = price
        try:
            kindle_node = root.cssselect("tbody[id='kindle_meta_binding_winner']")
            kindle_price = float(kindle_node[0].cssselect("td[class=' price ']")[0].text_content().strip()[1:])
        except(IndexError):
            kindle_price = 0
        bargain = is_bargain(price, list_price, kindle_price)
    print save(title, url, bargain, price, price / list_price, kindle_price / list_price)