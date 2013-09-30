import scraperwiki

import lxml.html           
       
html = scraperwiki.scrape("https://www.retkitukku.fi")
         
root = lxml.html.fromstring(html)

for a in root.cssselect("ul#new-products li.item a"):
    href = a.attrib['href']
    if not "http" in href: continue
    print href

    detailPage = scraperwiki.scrape(href)
    detailPageRoot = lxml.html.fromstring(detailPage)
    details = []
    sku = ""
    for p in detailPageRoot.cssselect("p.product-ids"):
        sku = p.text_content()
        print sku

    data = {
    'href' : href,
    'sku' : sku
    }
    scraperwiki.sqlite.save(unique_keys=['href'], data=data, table_name="data")
    #detailPages.append(detailPage)

import scraperwiki

import lxml.html           
       
html = scraperwiki.scrape("https://www.retkitukku.fi")
         
root = lxml.html.fromstring(html)

for a in root.cssselect("ul#new-products li.item a"):
    href = a.attrib['href']
    if not "http" in href: continue
    print href

    detailPage = scraperwiki.scrape(href)
    detailPageRoot = lxml.html.fromstring(detailPage)
    details = []
    sku = ""
    for p in detailPageRoot.cssselect("p.product-ids"):
        sku = p.text_content()
        print sku

    data = {
    'href' : href,
    'sku' : sku
    }
    scraperwiki.sqlite.save(unique_keys=['href'], data=data, table_name="data")
    #detailPages.append(detailPage)

