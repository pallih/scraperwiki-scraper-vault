import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.superhry.cz/")
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[class='g_list'] p"):
    td = tr.cssselect("span")
    if 1==1:   
        data = {
        'title' : tr.text_content(),
        }
        scraperwiki.sqlite.save(unique_keys=['title'], data=data)
        print data
import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.superhry.cz/")
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[class='g_list'] p"):
    td = tr.cssselect("span")
    if 1==1:   
        data = {
        'title' : tr.text_content(),
        }
        scraperwiki.sqlite.save(unique_keys=['title'], data=data)
        print data
