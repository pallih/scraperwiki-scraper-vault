import scraperwiki
html = scraperwiki.scrape('http://www.denieuwereporter.nl/')
# scrape headlines van denieuwereporter-alle h1 koppen

import lxml.html
root = lxml.html.fromstring(html)
tds = root.cssselect('h1')
for h1 in tds:
    #print lxml.html.tostring(h1)
    print h1.text_content()
    record = {'h1': h1.text_content()}
    scraperwiki.sqlite.save(["h1"], record)
    
