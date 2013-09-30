import scraperwiki

# Blank Python
           
import lxml.html
html = scraperwiki.scrape("https://etherpad.mozilla.org/animatedgifs")
root = lxml.html.fromstring(html)
for el in root.cssselect("a"):           
    print lxml.html.tostring(el)
    data = {'link' : lxml.html.tostring(el)
        }
    scraperwiki.sqlite.save(unique_keys=['link'], data=data)
print dataimport scraperwiki

# Blank Python
           
import lxml.html
html = scraperwiki.scrape("https://etherpad.mozilla.org/animatedgifs")
root = lxml.html.fromstring(html)
for el in root.cssselect("a"):           
    print lxml.html.tostring(el)
    data = {'link' : lxml.html.tostring(el)
        }
    scraperwiki.sqlite.save(unique_keys=['link'], data=data)
print data