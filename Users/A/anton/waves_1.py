import scraperwiki
import dateutil.parser
import lxml.html 

html = scraperwiki.scrape("http://www.mumm.ac.be/NL/Models/Operational/Wind/table.php?station=hoekvanholland")
     
root = lxml.html.fromstring(html)
rows = root.cssselect('''table[width="100%"][border="0"][cellspacing="0"][cellpadding="3"] tr''')
for tr in rows[4:]:
    tds = tr.cssselect("td")
    if len(tds)==8:
        data = {
            'datetime' : dateutil.parser.parse(tds[0].text_content()+" "+tds[1].text_content()),
            'Bft' : int(tds[4].text_content()),
            'Direction_degrees' : int(tds[5].text_content())
        }
        scraperwiki.sqlite.save(unique_keys=['datetime'], data=data)
