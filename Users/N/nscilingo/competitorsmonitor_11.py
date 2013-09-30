import scraperwiki
import scraperwiki           
import lxml.html 
import uuid
import datetime

# Blank Python

ASINS = ["B000EQ815G","B000EQ813S","B000I6L0PK","B002LPTOAE","B002PB2KK0","B002PAV7A0","B0028M26GE"]
summary = ""

for asin in ASINS:
    url = "http://www.amazon.com/dp/"+asin
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
    

import scraperwiki
import scraperwiki           
import lxml.html 
import uuid
import datetime

# Blank Python

ASINS = ["B000EQ815G","B000EQ813S","B000I6L0PK","B002LPTOAE","B002PB2KK0","B002PAV7A0","B0028M26GE"]
summary = ""

for asin in ASINS:
    url = "http://www.amazon.com/dp/"+asin
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
    

