import scraperwiki
import lxml.html


print "Hello, coding in the cloud!"

#html = scraperwiki.scrape("http://fpv-community.de/forumdisplay.php?25-Biete") 
#print html

html = scraperwiki.scrape("http://fpv-community.de/forumdisplay.php?25-Biete")
root = lxml.html.fromstring(html)


