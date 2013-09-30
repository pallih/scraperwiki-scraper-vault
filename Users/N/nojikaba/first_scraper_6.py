import scraperwiki
import lxml.html
html = scraperwiki.scrape("https://scraperwiki.com/")
root = lxml.html.fromstring(html)

el = root.cssselect("h1 a")[0]
print el.textimport scraperwiki
import lxml.html
html = scraperwiki.scrape("https://scraperwiki.com/")
root = lxml.html.fromstring(html)

el = root.cssselect("h1 a")[0]
print el.text