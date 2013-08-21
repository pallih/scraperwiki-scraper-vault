import scraperwiki

# Blank Python
print "Hello, coding in the cloud!"
import scraperwiki
html = scraperwiki.scrape("http://www.chestertoncc.net/Moodle/course/view.php?id=2389")


print html


import lxml.html
root = lxml.html.fromstring(html)
for el in root.cssselect("div.current *"):
    print el
   

