import scraperwiki
import lxml.html

# Blank Python
html = scraperwiki.scrape("http://www.finn.no/finn/torget/tilsalgs/resultat?SEGMENT=1&screen_size=8&areaId=20061&PRICE_FROM=&PRICE_TO=&CATEGORY%2FMAINCATEGORY=93&CATEGORY%2FSUBCATEGORY=3215&CATEGORY%2FPRODUCTCATEGORY=45&sort=3")
root = lxml.html.fromstring(html)
for item in root.cssselect("ul#resultlist li"):
    id = item.cssselect('a')[0].attrib['name']
    img = item.cssselect("div[class='image'] img")[0].attrib['src']
    #print lxml.html.tostring(item.cssselect("a[class='heading']")[0])
    heading = item.cssselect("a[class='heading']")[0].text
    print heading
    price = item.cssselect("div[class='price']")[0].attrib['data-obj-price']
    published = item.cssselect("div[class='published']")[0].text
    print published
    print "%s %s %s %s" % (id, heading, price, published)

    scraperwiki.sqlite.save(unique_keys=["id"], data={"id":id, "title":heading, "price": price, "published": published, "img": img})

import scraperwiki
import lxml.html

# Blank Python
html = scraperwiki.scrape("http://www.finn.no/finn/torget/tilsalgs/resultat?SEGMENT=1&screen_size=8&areaId=20061&PRICE_FROM=&PRICE_TO=&CATEGORY%2FMAINCATEGORY=93&CATEGORY%2FSUBCATEGORY=3215&CATEGORY%2FPRODUCTCATEGORY=45&sort=3")
root = lxml.html.fromstring(html)
for item in root.cssselect("ul#resultlist li"):
    id = item.cssselect('a')[0].attrib['name']
    img = item.cssselect("div[class='image'] img")[0].attrib['src']
    #print lxml.html.tostring(item.cssselect("a[class='heading']")[0])
    heading = item.cssselect("a[class='heading']")[0].text
    print heading
    price = item.cssselect("div[class='price']")[0].attrib['data-obj-price']
    published = item.cssselect("div[class='published']")[0].text
    print published
    print "%s %s %s %s" % (id, heading, price, published)

    scraperwiki.sqlite.save(unique_keys=["id"], data={"id":id, "title":heading, "price": price, "published": published, "img": img})

