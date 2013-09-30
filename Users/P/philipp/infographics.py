import scraperwiki
import lxml.html      
rows = []

print "hello"
html = scraperwiki.scrape("http://gibddmoscow.ru/")

root = lxml.html.fromstring(html)import scraperwiki
import lxml.html      
rows = []

print "hello"
html = scraperwiki.scrape("http://gibddmoscow.ru/")

root = lxml.html.fromstring(html)