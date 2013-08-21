import scraperwiki
import scraperwiki           
import lxml.html 
import uuid
import datetime

# Blank Python

ASINS = ["B000BPF0EA","B0050SVNP8","B009EUUYYY"]
summary = ""

for asin in ASINS:
    url = "http://www.amazon.com/dp/"+asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    for price in root.cssselect("span[id='availGreen'] b"):
        summary += price .text +"<br>"
        break
    

now = datetime.datetime.now()
data = {
    
    'description': summary,

}
scraperwiki.sqlite.save(unique_keys=['link'],data=data)
    

