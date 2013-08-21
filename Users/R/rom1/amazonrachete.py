import scraperwiki
import scraperwiki           
import lxml.html 
import uuid
import datetime

# Blank Python

ASINS = ["9782709643740","9782253129905","B002XOHZWC","B0000DE2SS"]
summary = "abc--"

for asin in ASINS:
    url = "http://www.amazon.fr/gp/search/s/ref=tradeinavs?url=rh%3Dn%3A1850500031%26i%3Dbooks-tradein&field-keywords="+asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for title in root.cssselect("span[class='bld lrg red']"):  
        summary += title.text +":  "
        print (summary )
        break

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

ASINS = ["9782709643740","9782253129905","B002XOHZWC","B0000DE2SS"]
summary = "abc--"

for asin in ASINS:
    url = "http://www.amazon.fr/gp/search/s/ref=tradeinavs?url=rh%3Dn%3A1850500031%26i%3Dbooks-tradein&field-keywords="+asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for title in root.cssselect("span[class='bld lrg red']"):  
        summary += title.text +":  "
        print (summary )
        break

now = datetime.datetime.now()
data = {
    'link': "http://www.amazon.com/"+"&uuid="+str(uuid.uuid1()),
    'title': "Price Monitoring " + str(now),
    'description': summary,
    'pubDate': str(now) ,
}
scraperwiki.sqlite.save(unique_keys=['link'],data=data)

