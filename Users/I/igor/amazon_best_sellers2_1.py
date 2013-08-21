import scraperwiki

# Blank Python

import scraperwiki           
import lxml.html           
import xml.etree.ElementTree as ET
import datetime
import uuid

url = "http://www.amazon.com/Best-Sellers-Electronics-Camcorders/zgbs/electronics/172421/ref=zg_bs_nav_e_2_502394"
now = datetime.datetime.now()

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
description =""
for tr in root.cssselect("div[class='zg_item_normal']"): 
    for title in tr.cssselect("div[class='zg_title'] a"):
        itemurl = title.get("href")
        itemtext = title.text
        break
    for priceBlock in tr.cssselect("p[class='priceBlock']"):        
        if ET.tostring(priceBlock).find(">Price: ") != -1:
            for price in priceBlock.cssselect("span[class='price'] b"):
                itemprice = price.text
                description += itemtext+"<br>"
                break
            break

data = {
    'link': url+"&uuid="+str(uuid.uuid1()),
    'title': "hi",
    'description': description,
    'pubDate': str(now) ,
}
scraperwiki.sqlite.save(unique_keys=['link'],data=data)

