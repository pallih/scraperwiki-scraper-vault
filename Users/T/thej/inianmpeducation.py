import scraperwiki          
import lxml.html
html = scraperwiki.scrape("http://india.gov.in/govt/loksabha.php?alpha=all")
root = lxml.html.fromstring(html)
lis = root.cssselect('li > a') 
print "before for loop"
for li in lis:
    print "inside"
    print li.href 
    import scraperwiki          
import lxml.html
html = scraperwiki.scrape("http://india.gov.in/govt/loksabha.php?alpha=all")
root = lxml.html.fromstring(html)
lis = root.cssselect('li > a') 
print "before for loop"
for li in lis:
    print "inside"
    print li.href 
    