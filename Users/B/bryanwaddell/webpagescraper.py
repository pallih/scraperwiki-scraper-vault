import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.facebook.com/makerfaire")
root = lxml.html.fromstring(html)
for el in root.cssselect("li .fbTimelineUnit"):
    mem = el.text
    print el
    print el.text
    if mem is not None:
        data = {
            'Posts' : mem,
           }
        print data
        scraperwiki.sqlite.save(unique_keys=['Posts'], data=data)