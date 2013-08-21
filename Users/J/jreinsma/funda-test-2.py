import scraperwiki           
import lxml.html

city = "harlingen"
html = scraperwiki.scrape("http://www.funda.nl/koop/"+city)
root = lxml.html.fromstring(html)

#ul.link-list paging-list

#nav = root.cssselect("ul.paging-list li")
#cnt = len(nav)

#print nav.cssselect("li a")[0]

el = root.cssselect("ul.paging-list li")
print "el " + lxml.html.tostring(el)




