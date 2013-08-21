import scraperwiki
from itertools import count
from lxml import html

BASE = "http://www.openpr.de/news/%s"


initial = scraperwiki.sqlite.get_var('num', 1)

for i in count(initial):
    url = BASE % i
    try:
        doc = html.parse(url)
        pm = doc.find('//div[@id="pm"]')
        pm_str = html.tostring(pm)
        scraperwiki.sqlite.save(["id"], {'id': i, 'pm': pm_str, 'url': url})
        print "AYE", i
    except:
        print "FAIL", i
    scraperwiki.sqlite.save_var('num', i)