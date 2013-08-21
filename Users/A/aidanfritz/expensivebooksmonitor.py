import scraperwiki
import scraperwiki           
import lxml.html 
import uuid
import datetime

# Blank Python

ASINS = [
        "B008DYIEN0", "B002O0K6VC", "B006XWYGUY", "B008LDJW66"
    ]
summary = ""

for asin in ASINS:
    url = "http://www.amazon.com/dp/"+asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    localsummary = ""
    for title in root.cssselect("span[id='btAsinTitle']"):  
        localsummary += title.text +":  "
        break
    for price in root.cssselect("b[class='priceLarge']"):
        foundprice = price.text
        break
    #summary += url + "<br>"

    flour = float(foundprice.strip(' \t\n$'))
    if(flour<12):
        summary += "Low price book: " + localsummary + "; link = " + url + " @ $" + str(flour) + "<br>"
#    now = datetime.datetime.now()
#    if(flour<10):
#        data = {
#            'link': url,
#            'title': "Price monitor: " + str(now),
#            'description': summary,
#            'price': flour,
#            'pubDate': str(now) ,
#        }
#        scraperwiki.sqlite.save(unique_keys=['link'],data=data)
#    summary = "";


now = datetime.datetime.now()
data = {
    'link': "http://www.amazon.com/"+"&uuid="+str(uuid.uuid1()),
    'title': "Price Monitoring " + str(now),
    'description': summary,
    'pubDate': str(now) ,
}
scraperwiki.sqlite.save(unique_keys=['link'],data=data)
    

