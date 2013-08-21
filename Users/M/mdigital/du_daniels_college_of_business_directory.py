import scraperwiki
import lxml.html
html = scraperwiki.scrape('http://daniels.du.edu/about/directory/')
root = lxml.html.fromstring(html)
#for el in root.cssselect('.directory-list .entry .Thumbnail thumbnail directory-photo .directory-name a'):
for el in root.cssselect('.directory-name a'):
    mem = el.text
    print el
    print el.text
    if mem is not None:
        data = {
            'Member Name' : mem,
        }
    if 
        print data
        scraperwiki.sqlite.save(unique_keys=['Member Name'], data = data)