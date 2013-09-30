import scraperwiki 
import lxml.html

html = scraperwiki.scrape("http://labs.nixmc.com/~steve/List_of_Countries.html") 

root = lxml.html.fromstring(html)
for span in root.cssselect("#sortable_table_id_0 span.flagicon"):
    img = span.cssselect("img")
    print img.src
import scraperwiki 
import lxml.html

html = scraperwiki.scrape("http://labs.nixmc.com/~steve/List_of_Countries.html") 

root = lxml.html.fromstring(html)
for span in root.cssselect("#sortable_table_id_0 span.flagicon"):
    img = span.cssselect("img")
    print img.src
