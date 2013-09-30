import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://services.co.benton.ar.us/dcn/inmateGrid.aspx?&d=1")
print html

root = lxml.html.fromstring(html)

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("td[id='tdInmates'] tr[class='upper']"):
    tds = tr.cssselect("td")
    data = {
        'years-old' : int(tds[4].text_content()),
        'name' : tds[1].text_content() + " " + tds[3].text_content()
    }
    scraperwiki.sqlite.save(unique_keys=['name'], data=data)
    print dataimport scraperwiki
import lxml.html

html = scraperwiki.scrape("http://services.co.benton.ar.us/dcn/inmateGrid.aspx?&d=1")
print html

root = lxml.html.fromstring(html)

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("td[id='tdInmates'] tr[class='upper']"):
    tds = tr.cssselect("td")
    data = {
        'years-old' : int(tds[4].text_content()),
        'name' : tds[1].text_content() + " " + tds[3].text_content()
    }
    scraperwiki.sqlite.save(unique_keys=['name'], data=data)
    print data