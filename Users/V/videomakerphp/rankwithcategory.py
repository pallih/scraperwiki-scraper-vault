import string
import scraperwiki           
import lxml.html

html = scraperwiki.scrape("http://www.coolchaineurope.com/Event.aspx?id=721898")
#root = lxml.html.fromstring(html)

ASINS = ['B0019ANSAO', 'B000BJBH48']

def checkParen(res):
    if '(' in  res: return True
    else: return False
    

#url = "http://www.amazon.com/dp/"+'B005F1ISR6'
#html = scraperwiki.scrape(url)
#root = lxml.html.fromstring(html)

#res = root.cssselect("li#SalesRank")[0].text_content()
#res = res[26:]
#print res[res.find('#'):res.find('(')]
el=[]
for asin in ASINS:
    url = "http://www.amazon.com/dp/"+asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    res = root.cssselect("li#SalesRank")[0].text_content()
    if checkParen(res):
        el.append(res[res.find('#'):res.find('(')])
    else:
        el.append(res[res.find('#'):res.find('>')])

for e in el:
    print e
    


import string
import scraperwiki           
import lxml.html

html = scraperwiki.scrape("http://www.coolchaineurope.com/Event.aspx?id=721898")
#root = lxml.html.fromstring(html)

ASINS = ['B0019ANSAO', 'B000BJBH48']

def checkParen(res):
    if '(' in  res: return True
    else: return False
    

#url = "http://www.amazon.com/dp/"+'B005F1ISR6'
#html = scraperwiki.scrape(url)
#root = lxml.html.fromstring(html)

#res = root.cssselect("li#SalesRank")[0].text_content()
#res = res[26:]
#print res[res.find('#'):res.find('(')]
el=[]
for asin in ASINS:
    url = "http://www.amazon.com/dp/"+asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    res = root.cssselect("li#SalesRank")[0].text_content()
    if checkParen(res):
        el.append(res[res.find('#'):res.find('(')])
    else:
        el.append(res[res.find('#'):res.find('>')])

for e in el:
    print e
    


