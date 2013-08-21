import requests
import scraperwiki           
import lxml.html           
import re


root = "http://www.amazon.com/Kindle-eBooks/"

borrowVerbiage = "Borrow this book"

def handleSearch(url, limit = 1):
    r = requests.get(url)
    page = lxml.html.fromstring(r.text)
    print r.text
    page.make_links_absolute(url)
    products = page.cssselect(".product")
    print products
    for productDiv in products:
        price = productDiv.cssselect(".rsltL span.bld.lrg.red")[0].text_content().trim().replace('$', '')
        title = productDiv.cssselect("h3 a span.lrg.bold").text_content()
        lending = borrowVerbiage in productDiv.text_content()
        data = { "title" : title,
                 "price" : price,
                 "lending" : lending }
        print data
        #scraperwiki.sqlite.save(unique_keys=['detailUrl'], data=data)

def findCategoryUrl(category):
    r = requests.get(root)
    page = lxml.html.fromstring(r.text)
    page.make_links_absolute(root)
    links = page.cssselect("div.left_nav a")
    for link in links:
        if category == link.text_content():
            return link.attrib['href']

fictionUrl = findCategoryUrl("Fiction")
print fictionUrl
handleSearch(fictionUrl)
