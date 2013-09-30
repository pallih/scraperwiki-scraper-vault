import scraperwiki
import dateutil.parser
import lxml.html 

html = scraperwiki.scrape("http://www.mumm.ac.be/NL/Models/Operational/Waves/table.php?station=hoekvanholland")
     
root = lxml.html.fromstring(html)
rows = root.cssselect('''table[width="100%"][border="0"][cellspacing="0"][cellpadding="2"] tr''')
for tr in rows[3:]:
    print tr.text_content()
    tds = tr.cssselect("td")
    if len(tds)==5:
        data = {
            'datetime' : dateutil.parser.parse(tds[0].text_content()+" "+tds[1].text_content()),
            #'time' : tds[1].text_content(),
            'waveheight' : float(tds[2].text_content()),
            'pctswell' : int(tds[3].text_content())
        }
        print data
        scraperwiki.sqlite.save(unique_keys=['datetime'], data=data)
import scraperwiki
import dateutil.parser
import lxml.html 

html = scraperwiki.scrape("http://www.mumm.ac.be/NL/Models/Operational/Waves/table.php?station=hoekvanholland")
     
root = lxml.html.fromstring(html)
rows = root.cssselect('''table[width="100%"][border="0"][cellspacing="0"][cellpadding="2"] tr''')
for tr in rows[3:]:
    print tr.text_content()
    tds = tr.cssselect("td")
    if len(tds)==5:
        data = {
            'datetime' : dateutil.parser.parse(tds[0].text_content()+" "+tds[1].text_content()),
            #'time' : tds[1].text_content(),
            'waveheight' : float(tds[2].text_content()),
            'pctswell' : int(tds[3].text_content())
        }
        print data
        scraperwiki.sqlite.save(unique_keys=['datetime'], data=data)
