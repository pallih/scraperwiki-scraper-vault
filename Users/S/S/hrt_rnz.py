import scraperwiki
import lxml.html
import datetime

urls = ["http://rnz.hrt.hr/index.php?sel_mreza=1.+Program", "http://rnz.hrt.hr/index.php?sel_mreza=2.+Program", "http://rnz.hrt.hr/index.php?sel_mreza=Radio+Pula&sel_ciklus=EXPLORA"]

for url in urls:
    
    html = scraperwiki.scrape(url)
    
    root = lxml.html.fromstring(html)
    for emisija in root.cssselect("h4.ciklus"):
        if emisija.text_content() in ('ANDROMEDA', 'PROFIT', 'EKSPLORA', 'OKO ZNANOSTI', 'OTVORENA SRIJEDA', u'POVIJEST \u010CETVRTKOM'):
            for epizoda in emisija.getnext().cssselect("tr"):
                tds = epizoda.cssselect("td")
                print  emisija.text_content()
                data = {
                  'emisija' : emisija.text_content(),
                  'datum' : datetime.datetime.strptime(tds[0].text_content(), '%d.%m.%Y').date(),
                  'naslov' : tds[3].text_content(),
                  'trajanje' : tds[5].text_content(),
                  'velicina' : tds[6].text_content(),
                  'link' : tds[1].cssselect("a")[0].get('href')
                }
                scraperwiki.sqlite.save(unique_keys=['emisija', 'naslov'], data=data)

