import string
import scraperwiki           
import lxml.html

#html = scraperwiki.scrape("http://www.amazon.com/Genome-Autobiography-Species-Chapters-P-S/dp/0060894083")
#root = lxml.html.fromstring(html)

#ASINS =["B005NI0QSA"]
ASINS = ['B0019ANSAO', 'B00062NVSA', 'B000BJBH48', 'B000PEAMP4', 'B0015IS6K2', 'B003YDFYSI', 'B004FJ3QQM', 'B004LVM8U4', 'B001CZWNUC', 'B000FEO61A', 'B002DUD6RO', 'B004NXYP5G', 'B000OOLYO8', 'B004USKDKA', 'B004X9BRRO', 'B0019SQWWC', 'B00641RE7G', 'B004GJRG3K', 'B0013FKZ3S', 'B003LW4LJK', 'B0026XT71M', 'B007A2YQV0', 'B000E5S648', 'B0007YHBHO']

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

sellers=[]

for asin in ASINS:
    url = "http://www.amazon.com/dp/"+asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    el=[]
    for el1 in root.cssselect("div.buying b"):
        if el1=='':
            continue
        #el.append(string.strip(lxml.html.tostring(el1)))
        #print el1.text
        el.append(el1.text)
    if len(el)<1: sellers.append('Many Sellers.....')
    elif len(el)==13:
        sellers.append(el[7])
    elif len(el)==11 and el[2]!='Amazon Prime members enjoy:':
        sellers.append(el[2])
    elif len(el)==11 and el[2]=='Amazon Prime members enjoy:':
        sellers.append(el[6])
    elif len(el)==10:
        sellers.append(getThis10(asin))
    elif el[len(el)-5]==None:
        sellers.append(getThis(asin))
    else:
        sellers.append(el[len(el)-5])

print '================FINAL PRINT============'
for i in sellers:
    print i
#print sellers
import string
import scraperwiki           
import lxml.html

#html = scraperwiki.scrape("http://www.amazon.com/Genome-Autobiography-Species-Chapters-P-S/dp/0060894083")
#root = lxml.html.fromstring(html)

#ASINS =["B005NI0QSA"]
ASINS = ['B0019ANSAO', 'B00062NVSA', 'B000BJBH48', 'B000PEAMP4', 'B0015IS6K2', 'B003YDFYSI', 'B004FJ3QQM', 'B004LVM8U4', 'B001CZWNUC', 'B000FEO61A', 'B002DUD6RO', 'B004NXYP5G', 'B000OOLYO8', 'B004USKDKA', 'B004X9BRRO', 'B0019SQWWC', 'B00641RE7G', 'B004GJRG3K', 'B0013FKZ3S', 'B003LW4LJK', 'B0026XT71M', 'B007A2YQV0', 'B000E5S648', 'B0007YHBHO']

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

sellers=[]

for asin in ASINS:
    url = "http://www.amazon.com/dp/"+asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    el=[]
    for el1 in root.cssselect("div.buying b"):
        if el1=='':
            continue
        #el.append(string.strip(lxml.html.tostring(el1)))
        #print el1.text
        el.append(el1.text)
    if len(el)<1: sellers.append('Many Sellers.....')
    elif len(el)==13:
        sellers.append(el[7])
    elif len(el)==11 and el[2]!='Amazon Prime members enjoy:':
        sellers.append(el[2])
    elif len(el)==11 and el[2]=='Amazon Prime members enjoy:':
        sellers.append(el[6])
    elif len(el)==10:
        sellers.append(getThis10(asin))
    elif el[len(el)-5]==None:
        sellers.append(getThis(asin))
    else:
        sellers.append(el[len(el)-5])

print '================FINAL PRINT============'
for i in sellers:
    print i
#print sellers
