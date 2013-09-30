import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.un.org/en/members/")
root = lxml.html.fromstring(html)
for el in root.cssselect("li.countryname a"):
    mem = el.text
    print el
    print el.text
    if mem is not None:
        data = {
            'Country' : mem,
          }
        print data
        scraperwiki.sqlite.save(unique_keys=['Country'], data=data)



import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.un.org/en/members/")
root = lxml.html.fromstring(html)
for el in root.cssselect("li.countryname a"):
    mem = el.text
    print el
    print el.text
    if mem is not None:
        data = {
            'Country' : mem,
          }
        print data
        scraperwiki.sqlite.save(unique_keys=['Country'], data=data)



