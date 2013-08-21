import string
import scraperwiki           
import lxml.html

html = scraperwiki.scrape("http://www.coolchaineurope.com/Event.aspx?id=721898")
#root = lxml.html.fromstring(html)

ASINS = ['B004TXY0TG']

#======Special Functions==========
def checkParen(res):
    if '(' in  res: return True
    else: return False

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
    #return el[len(el)-4]
    return str(el[len(el)-4]) + ' and ' + str(fd[1])

def getThis10(asin):
    url = "http://www.amazon.com/dp/"+asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    el=[]
    fd=[]
    for el1 in root.cssselect("div.buying a"):
        if el1=='':
            continue
        #print el1.text
        el.append(el1.text)
    for el2 in root.cssselect("div.buying strong"):
        if el2=='':
            continue
        fd.append(el2.text)
    #return el[len(el)-4]
    return str(el[len(el)-3]) + ' and ' + str(fd[1])

def getThis10(asin):
    url = "http://www.amazon.com/dp/"+asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    el=[]
    fd=[]
    for el1 in root.cssselect("div.buying a"):
        if el1=='':
            continue
        #print el1.text
        el.append(el1.text)
    for el2 in root.cssselect("div.buying strong"):
        if el2=='':
            continue
        fd.append(el2.text)
    #return el[len(el)-4]
    return str(el[len(el)-3]) + ' and ' + str(fd[1])

#======End of Special functions===


#======Getters Functions==========

def getName(root):
    res = root.cssselect("title")[0].text_content()
    res = res[res.find(':')+2:]
    return (res[:res.find(':')])
        
def getBy(root):
    res = root.cssselect("span.bxgy-byline-text")[0].text_content()
    return res[3:]

def getPrice(root):
    res = root.cssselect("b.priceLarge")[0].text_content()
    return res
    
def getSoldBy(root):
    el=[]
    i=0
    for el1 in root.cssselect("div.buying b"):
        if el1=='':
            continue
        el.append(el1.text)
    if len(el)<1: return 'Many Sellers.....'
    elif len(el)==13:
        if el[7]!='or':         
            return(el[7])
        else:
            return str(el[2]) + ' and ' + str(el[3])
    elif len(el)<=11 and el[2]!='Amazon Prime members enjoy:':
        return(el[2])
    elif len(el)==11 and el[2]=='Amazon Prime members enjoy:':
        return(el[6])
    elif len(el)==10:
        return(getThis10(asin))
    elif el[len(el)-5]==None:
        return(getThis(asin))
    else:
        return(el[len(el)-5])


def getRank(root):
    #if  len(root.cssselect("li#SalesRank"))<1: return None
    res = root.cssselect("li#SalesRank")[0].text_content()
    if checkParen(res):
        return (res[res.find('#'):res.find('(')])
    else:
        return (res[res.find('#'):res.find('>')])

def getUPC(root):
    el=[]
    i=0
    #if  len(root.cssselect("td#bucket"))<1: return None
    for el1 in root.cssselect("td.bucket ul li"):
        if el1=='':
            continue
        if 'UPC:' in str(el1[0].text):
            return str(el1.text_content())
        #print str(el1[0].text)
        #el.append(el1.text)
    return None

#======End Of Getters functions===
el=[]
for asin in ASINS:
    url = "http://www.amazon.com/dp/"+asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    el.append(getSoldBy(root)+' <-+-> '+getRank(root) +' <-+-> '+ getUPC(root))
    #el.append(getUPC(root))

for e in el:
    print e
    


