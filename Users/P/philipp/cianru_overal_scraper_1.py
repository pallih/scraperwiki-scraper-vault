import scraperwiki    

# Blank Python

import scraperwiki
# html = scraperwiki.scrape("http://www.cian.ru/cat.php?deal_type=2&obl_id=1&room1=1")

import lxml.html
#root = lxml.html.fromstring(html)


for i in range(1,280):
    html2 = scraperwiki.scrape("http://www.mosgorzdrav.ru/mgz/komzdravsite.nsf/fa_MainForm?OpenForm&type=ka_numberslist&page=" + str(i))
    root = lxml.html.fromstring(html)

    for tr in root.cssselect("div.content tr"):
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