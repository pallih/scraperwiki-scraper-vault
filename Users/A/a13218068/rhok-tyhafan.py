import scraperwiki
import lxml.html
import dateutil.parser
import datetime
import string
import re


html = scraperwiki.scrape("http://www.tyhafan.org/our-events/");
root = lxml.html.fromstring(html)
for el in root.cssselect("div.wysiwyg table tr"):
    print lxml.html.tostring(el)
    tds = el.getchildren()
    d = tds[0].text_content()
    if( d.startswith("Date")):
        continue
    e = tds[1].text_content()
    det = tds[2].text_content()
    d = re.sub("[^a-zA-Z0-9.]", " ", d)
    print d
    startdate = datetime.datetime.strptime(d,"%d %B %Y")
    data = {
        'title' : e,
        'datestart' : startdate.strftime('%Y-%m-%d')
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['title'], data=data)


