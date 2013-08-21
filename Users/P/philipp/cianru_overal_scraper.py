import scraperwiki

# Blank Python

import scraperwiki
html = scraperwiki.scrape("http://www.cian.ru/cat.php?deal_type=2&obl_id=1&room1=1")

import lxml.html
root = lxml.html.fromstring(html)

var = root.cssselect("div.np td") 

tex = var[5].text_content()
Tex = tex.split("|")
B = Tex[len(Tex) - 2]
intB = int(B)
print (B)
   

for tr in root.cssselect("table.cat tr"):
    tds = tr.cssselect("td")
    if len(tds)==9:
        data = {
            'number' : tds[0].text_content(),
            'adress' : tds[1].text_content(),
            'type' : tds[2].text_content(),
            'area' : tds[3].text_content(),
            'price' : tds[4].text_content(),
            'floor' : tds[5].text_content(),
            'details' : tds[6].text_content(),
            'contacts' : tds[7].text_content(),
            'text' : tds[8].text_content(),
            'id' : "1p" + tds[0].text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)

for i in range(80,intB+1):
    html2 = scraperwiki.scrape("http://www.cian.ru/cat.php?deal_type=2&obl_id=1&room1=1&p=" + str(i))
    root = lxml.html.fromstring(html)

    for tr in root.cssselect("table.cat tr"):
        tds = tr.cssselect("td")
        if len(tds)==9:
            data = {
                'number' : tds[0].text_content(),
                'adress' : tds[1].text_content(),
                'type' : tds[2].text_content(),
                'area' : tds[3].text_content(),
                'price' : tds[4].text_content(),
                'floor' : tds[5].text_content(),
                'details' : tds[6].text_content(),
                'contacts' : tds[7].text_content(),
                'text' : tds[8].text_content(),
                'id' : str(i)+"p" + tds[0].text_content()
            }
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)