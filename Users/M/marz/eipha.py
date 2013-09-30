import scraperwiki

# Blank Python

url="https://webgate.ec.europa.eu/eipaha/initiative/index/index/page/";

n=30
ll=[]

for i in range(1,n):

    ll.append( url+str(i)+"/")

print ll[0]

dom=scraperwiki.scrape(ll[0])

print dom

root2 = lxml.html.fromstring(dom)
td=root2.cssselect(".DataTableEditable tbody tr td")

print td


# for link in ll:
import scraperwiki

# Blank Python

url="https://webgate.ec.europa.eu/eipaha/initiative/index/index/page/";

n=30
ll=[]

for i in range(1,n):

    ll.append( url+str(i)+"/")

print ll[0]

dom=scraperwiki.scrape(ll[0])

print dom

root2 = lxml.html.fromstring(dom)
td=root2.cssselect(".DataTableEditable tbody tr td")

print td


# for link in ll:
