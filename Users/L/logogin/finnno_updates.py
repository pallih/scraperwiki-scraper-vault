import scraperwiki
import lxml.html
from datetime import datetime

html = scraperwiki.scrape("http://www.finn.no/finn/torget/tilsalgs/resultat?sort=1&CATEGORY/SUBCATEGORY=3215&periode=3&SEGMENT=1&areaId=20061&CATEGORY/MAINCATEGORY=93&rows=75")
root = lxml.html.fromstring(html)
scraperwiki.sqlite.execute("drop table if exists swdata") 
for item in root.cssselect("div#resultList div[class='item']"):
    #print lxml.html.tostring(item)
    #print lxml.html.tostring(item.cssselect('> div')[0])
    id = item.cssselect('> div')[0].attrib['id']
    img = item.cssselect("div[class='img'] img")[0].attrib['src']
    heading = item.cssselect("*[data-automation-id='heading'] a")[0].text
    url = "http://www.finn.no/finn/torget/tilsalgs/" + item.cssselect("*[data-automation-id='heading'] a")[0].attrib['href']
    if len(item.cssselect("div[class='strong sharp']")) > 0:
        price = item.cssselect("div[class='strong sharp']")[0].text
    else:
        price = 'N/A'
    published = item.cssselect("*[data-automation-id='dateinfo']")[0].text.strip()
    published_date = datetime.strptime(published, '%d.%m.%Y %H:%M')
    scraperwiki.sqlite.save(unique_keys=["id"], data={"id":id, "title":heading, "price": price, "published": published, "published_date": published_date, "img": img, "url": url})

