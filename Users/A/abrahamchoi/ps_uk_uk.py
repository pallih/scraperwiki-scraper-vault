import scraperwiki
import scraperwiki           
import lxml.html 
import uuid
import datetime

# Blank Python

ASINS = ["B0000A1VS3","B004QVYMDA","B0044XKUMC","B004Z7D01K","B000ARAPQW","B0001LJ392","B001LZDQWW","B00007EE9P","B0000CD7J0","B00009R6VS"]
summary = ""

for asin in ASINS:
    url = "http://www.amazon.co.uk/dp/"+asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for title in root.cssselect("span[id='btAsinTitle']"):  
        summary += title.text +":  "
        break
    for price in root.cssselect("span[id='actualPriceValue'] b"):
        summary += price.text +"<br>"
        break
    for merchantid in root.cssselect("span[id='merchantID'] b"):
        summary += merchantid.text +"<br>"
        break
    summary += url + "<br>"

now = datetime.datetime.now()
data = {
    'link': "http://www.amazon.co.uk/"+"&uuid="+str(uuid.uuid1()),
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

ASINS = ["B0000A1VS3","B004QVYMDA","B0044XKUMC","B004Z7D01K","B000ARAPQW","B0001LJ392","B001LZDQWW","B00007EE9P","B0000CD7J0","B00009R6VS"]
summary = ""

for asin in ASINS:
    url = "http://www.amazon.co.uk/dp/"+asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for title in root.cssselect("span[id='btAsinTitle']"):  
        summary += title.text +":  "
        break
    for price in root.cssselect("span[id='actualPriceValue'] b"):
        summary += price.text +"<br>"
        break
    for merchantid in root.cssselect("span[id='merchantID'] b"):
        summary += merchantid.text +"<br>"
        break
    summary += url + "<br>"

now = datetime.datetime.now()
data = {
    'link': "http://www.amazon.co.uk/"+"&uuid="+str(uuid.uuid1()),
    'title': "Price Monitoring " + str(now),
    'description': summary,
    'pubDate': str(now) ,
}
scraperwiki.sqlite.save(unique_keys=['link'],data=data)
    

