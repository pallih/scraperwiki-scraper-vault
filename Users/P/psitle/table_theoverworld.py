import scraperwiki
from lxml.etree import tostring
import re
import lxml.html

html = scraperwiki.scrape("http://www.minecraftwiki.net/wiki/The_Overworld")
root = lxml.html.fromstring(html)

record = {}

tables = root.cssselect("table")
num = 0
for table in tables:
    ths = table.cssselect("th")
    if len(ths) == 0:
        continue
    if ths[0].text == 'Icon':
        trs = table.cssselect("tr")
        for tr in trs:
            tds = tr.cssselect("td")
            if len(tds) == 4:
                title = tds[3].cssselect("a")
                if len(title) >= 1:
                    record['title'] = title[0].text

                if title != 'Air':
                    image = tds[0].cssselect("img")
                if len(image) == 1:
                    if title == 'Air':
                        img = None
                    else:
                        img = image[0].get('src')
                    record['img'] = img
                else:
                    record['img'] = None
                ID = tds[1].text
                if ID is None:
                    span = tds[1].cssselect("span")
                    ID = span[0].text
                record['ID'] = ID            
                record['num'] = num  
                num = num + 1
                scraperwiki.sqlite.save(['num'],record)
            
        



