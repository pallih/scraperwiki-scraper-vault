import scraperwiki
import scraperwiki           
import lxml.html 
import uuid
import datetime

# Blank Python

ASINS = ["continental-gp-4000s.html"]
summary = ""

for asin in ASINS:

    root = lxml.html.fromstring(html)
    for title in root.cssselect('product-name'):  
        summary += title.text +":  "
        break
    for price in root.cssselect("div[class='price']"):
        summary += price .text +"<br>"
        break
    summary += url + "<br>"

now = datetime.datetime.now()
data = {
    'title': "Price Monitoring " + str(now),
    'description': summary,
    'pubDate': str(now) ,
}
scraperwiki.sqlite.save(unique_keys=['link'],data=data)
    

import scraperwiki
import scraperwiki           
import lxml.html 
import uuid
import datetime

# Blank Python

ASINS = ["continental-gp-4000s.html"]
summary = ""

for asin in ASINS:

    root = lxml.html.fromstring(html)
    for title in root.cssselect('product-name'):  
        summary += title.text +":  "
        break
    for price in root.cssselect("div[class='price']"):
        summary += price .text +"<br>"
        break
    summary += url + "<br>"

now = datetime.datetime.now()
data = {
    'title': "Price Monitoring " + str(now),
    'description': summary,
    'pubDate': str(now) ,
}
scraperwiki.sqlite.save(unique_keys=['link'],data=data)
    

