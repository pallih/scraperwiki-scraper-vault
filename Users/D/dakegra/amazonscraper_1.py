import scraperwiki          
import lxml.html
import uuid
import datetime

# Variables

wishlist = "2J0GVYRVJGRKG"
limit = 1.50
asins = []
status = "Is not going cheap."
cheap = status

# Get ASINs from your Amazon Wish List

url = "http://www.amazon.co.uk/wishlist/" + wishlist + "/ref=cm_wl_act_print_o?_encoding=UTF8&disableNav=1&items-per-page=200&layout=standard-print&page=1&visitor-view=1"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
for element in root.cssselect("tbody.itemWrapper"):
    string = element.attrib["name"]
    pieces = string.split(".")
    asins.append(pieces[3])

# Process ASINs for further details

for asin in asins:
    url = "http://www.amazon.co.uk/dp/" + asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    title = root.cssselect("span[id='btAsinTitle']")
    for element in root.cssselect("div.buying input"):
        if(element.attrib["name"] == "displayedPrice"):
            price = float(element.attrib["value"])
    if(price < limit):
        cheap = "Is going cheap!" # Text to search for within IFTTT
    now = datetime.datetime.now()
    data = {
        "title": title[0].text_content(),
        "link": url,
        "description": cheap,
        "guid": url + "&uuid=" + str(uuid.uuid1()),
        "pubDate": str(now)
    }
    cheap = status
    scraperwiki.sqlite.save(unique_keys=['link'], data=data)