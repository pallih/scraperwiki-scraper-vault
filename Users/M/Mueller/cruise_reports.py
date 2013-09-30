import scraperwiki
import lxml.html
import dateutil.parser
import datetime

url = 'http://databases.sun-sentinel.com/news/broward/ftlaudcruise/ftlaudcruise_list.php?pagesize=500'
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
table = root.cssselect("tbody")[1]

i = 1
for tr in table:
    tds = tr.cssselect("td")
    data = {
        'id' : i,
        'incident' : tds[1].text_content(),
        'Ship' : tds[3].text_content(),
        'Line' : tds[4].text_content(),
        'Date' : tds[5].text_content(),
#        'Description' : tds[6].text_content(),
        }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    i += 1
import scraperwiki
import lxml.html
import dateutil.parser
import datetime

url = 'http://databases.sun-sentinel.com/news/broward/ftlaudcruise/ftlaudcruise_list.php?pagesize=500'
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
table = root.cssselect("tbody")[1]

i = 1
for tr in table:
    tds = tr.cssselect("td")
    data = {
        'id' : i,
        'incident' : tds[1].text_content(),
        'Ship' : tds[3].text_content(),
        'Line' : tds[4].text_content(),
        'Date' : tds[5].text_content(),
#        'Description' : tds[6].text_content(),
        }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    i += 1
