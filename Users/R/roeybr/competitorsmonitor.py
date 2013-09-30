import scraperwiki
import scraperwiki           
import lxml.html 
import uuid
import datetime

# Blank Python

ASINS = ["B005QJ7OR2","B0078Y0BAK","B002XOHZWC","B0000DE2SS"]
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

ASINS = ["B0018AA9CU","B0018A7F8Q","B000KNFR2S","B00112VEA6","B000CO89T8"]
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
    

