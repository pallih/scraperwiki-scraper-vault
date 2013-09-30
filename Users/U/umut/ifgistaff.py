import scraperwiki

# Blank Pythonhttps://scraperwiki.com/scrapers/new/python

html = scraperwiki.scrape("http://ifgi.uni-muenster.de/staff/") 
print html


import lxml.html
html = html.decode("latin1")
root = lxml.html.fromstring(html)
print root
for tr in root.cssselect("div[class='abstand'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==3:
        data = {
            'name' : tds[0].text_content(),
            'room' : tds[1].text_content(),
            'phone' : tds[2].text_content()
        }
        print data
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)
import scraperwiki

# Blank Pythonhttps://scraperwiki.com/scrapers/new/python

html = scraperwiki.scrape("http://ifgi.uni-muenster.de/staff/") 
print html


import lxml.html
html = html.decode("latin1")
root = lxml.html.fromstring(html)
print root
for tr in root.cssselect("div[class='abstand'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==3:
        data = {
            'name' : tds[0].text_content(),
            'room' : tds[1].text_content(),
            'phone' : tds[2].text_content()
        }
        print data
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)
