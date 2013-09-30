import scraperwiki
import lxml.html
a=[2086,1507,1831,1832,1910,1825,2513,2252,9028,1288,1626,2098,1439,1489,2823,1483,808,1760,1379]
b=0
o=0
while b != 19:
    html = scraperwiki.scrape("http://amerpages.com/spa/brasil/items/search/category:"+str(a[b]))
    root = lxml.html.fromstring(html)
    for el in root.cssselect("div.resultsInfo strong"):
        if el.text != 'Ordenar por:':
            categoria=int(el.text)
    f=html.count('listing featured')
    f=0
    scraperwiki.sqlite.save(unique_keys=['orden'],data={'orden':o,'featured':f,'categoria':categoria,'nombre':a[b]},table_name='xtra',verbose=2)
    o=o+1
    b=b+1import scraperwiki
import lxml.html
a=[2086,1507,1831,1832,1910,1825,2513,2252,9028,1288,1626,2098,1439,1489,2823,1483,808,1760,1379]
b=0
o=0
while b != 19:
    html = scraperwiki.scrape("http://amerpages.com/spa/brasil/items/search/category:"+str(a[b]))
    root = lxml.html.fromstring(html)
    for el in root.cssselect("div.resultsInfo strong"):
        if el.text != 'Ordenar por:':
            categoria=int(el.text)
    f=html.count('listing featured')
    f=0
    scraperwiki.sqlite.save(unique_keys=['orden'],data={'orden':o,'featured':f,'categoria':categoria,'nombre':a[b]},table_name='xtra',verbose=2)
    o=o+1
    b=b+1