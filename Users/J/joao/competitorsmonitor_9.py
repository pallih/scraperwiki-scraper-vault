import scraperwiki
import scraperwiki           
import lxml.html 
import uuid
import datetime

# Blank Python

ASINS = ["B006ZS4SXQ","B001V7RF9U"]
summary = ""

for asin in ASINS:
    url = "http://www.amazon.co.uk/dp/"+asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for title in root.cssselect("span[id='btAsinTitle']"):  
        summary += title.text +":  "
        break
    for price in root.cssselect("span[id='actualPriceValue'] b"):
        summary += price .text +"<br>"
        break
    summary += "<a href='"+url+"'>" + url + "</a><br><br>"

now = datetime.datetime.now()
data = {
    'title': "Price Monitoring " + str(now),
    'description': summary,
    'pubDate': str(now) ,
}
scraperwiki.sqlite.save(unique_keys=['pubDate'],data=data)
    

