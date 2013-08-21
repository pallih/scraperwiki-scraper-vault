import scraperwiki
html = scraperwiki.scrape("http://www.allanaaa.com/yelpscraper/search.htm")
print html

import lxml.html
root = lxml.html.fromstring(html)
bznesses = [[0]*3 for i in range(10)]
a = 0

l = 0
names = root.cssselect("h4.itemheading a")
for name in names:    
    bznesses[l][a] = name.text
    l += 1

a += 1
l = 0
for rating in root.cssselect("div.rating i"):
    stars = int(filter(str.isdigit, rating.attrib['title']))
    bznesses[l][a] = stars 
    l += 1

a += 1
l = 0
for popularity in root.cssselect("span.reviews"):
    value = int(filter(str.isdigit, popularity.text))
    bznesses[l][a] = value 
    l += 1



print bznesses
data = bznesses.pop()
print data
scraperwiki.sqlite.save(value, data)
