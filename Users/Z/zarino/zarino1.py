import scraperwiki
xml = scraperwiki.scrape("http://scraperwiki.com/feeds/all_code_objects/")
import lxml.html    
from lxml.etree import tostring       
root = lxml.html.fromstring(xml)


L = []

def getmode(li):
    li.sort()
    numbers = {}
    for x in li:
        num = li.count(x)
        numbers[x] = num
    highest = max(numbers.values())
    n = []
    for m in numbers.keys():
        if numbers[m] == highest:
            n.append(m)
    return n

def median(numericValues):
    theValues = sorted(numericValues)
    if len(theValues) % 2 == 1:
        return theValues[(len(theValues)+1)/2-1]
    else:
        lower = theValues[len(theValues)/2-1]
        upper = theValues[len(theValues)/2]
        return (float(lower + upper)) / 2  



for i in root.cssselect("channel item"):
    title = i.cssselect("title")[0].text_content()
    data = {
        'title' : title
    }
    scraperwiki.sqlite.save(unique_keys=['title'], data=data)
    L.append(len(title))

print "average title length = " + str((float(sum(L)) / len(L))) + " letters"

print "median title length = " + str(median(L)) + " letters"

print "most common title length = " + str(getmode(L)[0]) + " letters"