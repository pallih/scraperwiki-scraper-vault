import scraperwiki
html = scraperwiki.scrape('http://www.arnhem.nl/gemeenteraad/Over_de_gemeenteraad/De_raadsleden')       
# scrape leden van de raad in arnhem
import lxml.html
root = lxml.html.fromstring(html)
tds = root.cssselect('td')
for td in tds:
    #print lxml.html.tostring(h1)
    print td.text_content()
    record = { "td" : td.text_content()}
    scraperwiki.sqlite.save(["td"], record)
par = root.cssselect('h2')
for h2 in tds:
    #print lxml.html.tostring(h1)
    print h2.text_content()
    record = { "h2" : h2.text_content()}
    scraperwiki.sqlite.save(["h2"], record)
        


import scraperwiki
html = scraperwiki.scrape('http://www.arnhem.nl/gemeenteraad/Over_de_gemeenteraad/De_raadsleden')       
# scrape leden van de raad in arnhem
import lxml.html
root = lxml.html.fromstring(html)
tds = root.cssselect('td')
for td in tds:
    #print lxml.html.tostring(h1)
    print td.text_content()
    record = { "td" : td.text_content()}
    scraperwiki.sqlite.save(["td"], record)
par = root.cssselect('h2')
for h2 in tds:
    #print lxml.html.tostring(h1)
    print h2.text_content()
    record = { "h2" : h2.text_content()}
    scraperwiki.sqlite.save(["h2"], record)
        


import scraperwiki
html = scraperwiki.scrape('http://www.arnhem.nl/gemeenteraad/Over_de_gemeenteraad/De_raadsleden')       
# scrape leden van de raad in arnhem
import lxml.html
root = lxml.html.fromstring(html)
tds = root.cssselect('td')
for td in tds:
    #print lxml.html.tostring(h1)
    print td.text_content()
    record = { "td" : td.text_content()}
    scraperwiki.sqlite.save(["td"], record)
par = root.cssselect('h2')
for h2 in tds:
    #print lxml.html.tostring(h1)
    print h2.text_content()
    record = { "h2" : h2.text_content()}
    scraperwiki.sqlite.save(["h2"], record)
        


import scraperwiki
html = scraperwiki.scrape('http://www.arnhem.nl/gemeenteraad/Over_de_gemeenteraad/De_raadsleden')       
# scrape leden van de raad in arnhem
import lxml.html
root = lxml.html.fromstring(html)
tds = root.cssselect('td')
for td in tds:
    #print lxml.html.tostring(h1)
    print td.text_content()
    record = { "td" : td.text_content()}
    scraperwiki.sqlite.save(["td"], record)
par = root.cssselect('h2')
for h2 in tds:
    #print lxml.html.tostring(h1)
    print h2.text_content()
    record = { "h2" : h2.text_content()}
    scraperwiki.sqlite.save(["h2"], record)
        


