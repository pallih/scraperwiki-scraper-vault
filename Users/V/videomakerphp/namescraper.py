import string
import scraperwiki           
import lxml.html

html = scraperwiki.scrape("http://www.coolchaineurope.com/Event.aspx?id=721898")
#root = lxml.html.fromstring(html)

#ASINS = ["B001JDHR4Y","B00688FQXY","B001F51Q5M"]
ASINS = ["B005F1ISR6"]

def getThis(asin):
    url = "http://www.amazon.com/dp/"+asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    el=[]
    fd=[]
    for el1 in root.cssselect("div.buying a"):
        if el1=='':
            continue
        el.append(el1.text)
    for el2 in root.cssselect("div.buying strong"):
        if el2=='':
            continue
        fd.append(el2.text)
    return el


root = lxml.html.fromstring(html)

for el1 in root.cssselect("ul#SpeakrsList li"):
    if el1=='':
        continue
        #el.append(string.strip(lxml.html.tostring(el1)))
    name=el1.cssselect("a")
    position=el1.cssselect("strong")
    company=el1.cssselect("li")
    print el1.text_content()
    


import string
import scraperwiki           
import lxml.html

html = scraperwiki.scrape("http://www.coolchaineurope.com/Event.aspx?id=721898")
#root = lxml.html.fromstring(html)

#ASINS = ["B001JDHR4Y","B00688FQXY","B001F51Q5M"]
ASINS = ["B005F1ISR6"]

def getThis(asin):
    url = "http://www.amazon.com/dp/"+asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    el=[]
    fd=[]
    for el1 in root.cssselect("div.buying a"):
        if el1=='':
            continue
        el.append(el1.text)
    for el2 in root.cssselect("div.buying strong"):
        if el2=='':
            continue
        fd.append(el2.text)
    return el


root = lxml.html.fromstring(html)

for el1 in root.cssselect("ul#SpeakrsList li"):
    if el1=='':
        continue
        #el.append(string.strip(lxml.html.tostring(el1)))
    name=el1.cssselect("a")
    position=el1.cssselect("strong")
    company=el1.cssselect("li")
    print el1.text_content()
    


