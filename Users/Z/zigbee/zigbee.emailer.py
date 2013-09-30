import scraperwiki          
import lxml.html
import uuid
import datetime

# Variables

wishlist = "3DYAE9EHMW8AS"
limit = 1000
asins = []
summary = ""

# Functions

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

try: # Try and get ASINs from your Amazon Wish List
    url = "http://amzn.com/w/" + wishlist + "/ref=cm_wl_act_print_o?_encoding=UTF8&disableNav=1&items-per-page=2500&layout=standard-print&page=1&visitor-view=1"
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
    url = "http://www.amazon.com/dp/" + asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for title in root.cssselect("span[id='btAsinTitle']"):  
        summary += title.text +":  "
        break
    for price in root.cssselect("span[id='actualPriceValue'] b"):
        summary += price .text +"<br>"
        break
    summary += url + "<br>"

now = datetime.datetime.now()
data = {
    'link': "http://www.amazon.com/"+"&uuid="+str(uuid.uuid1()),
    'title': "Price Monitoring " + str(now),
    'description': summary,
    'pubDate': str(now) ,
}
scraperwiki.sqlite.save(unique_keys=['link'],data=data)

