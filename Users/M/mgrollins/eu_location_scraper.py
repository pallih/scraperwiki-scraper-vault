import scraperwiki
import lxml.html
from lxml import etree


html = scraperwiki.scrape("http://www.edd.ca.gov/jobs_and_training/Experience_Unlimited_Local_Information.htm")
root = lxml.html.fromstring(html)

locations = []
#for lel in root.cssselect("div.main_content"):
print "in lel loop"
for el in root.cssselect("div.content_left_column h2"):
    if el.text_content() != "More Information":
        locations.append(el.text_content())
 
        print "in el loop"
#       for lel in el.cssselect("*"):
#           print lel.text_content()
#           break

# place holder          

for loc in locations:
    print loc +",",

# scraperwiki.sqlite.save(unique_keys = ['locations'], data = locations)

#    print lxml.html.tostring(el)import scraperwiki
import lxml.html
from lxml import etree


html = scraperwiki.scrape("http://www.edd.ca.gov/jobs_and_training/Experience_Unlimited_Local_Information.htm")
root = lxml.html.fromstring(html)

locations = []
#for lel in root.cssselect("div.main_content"):
print "in lel loop"
for el in root.cssselect("div.content_left_column h2"):
    if el.text_content() != "More Information":
        locations.append(el.text_content())
 
        print "in el loop"
#       for lel in el.cssselect("*"):
#           print lel.text_content()
#           break

# place holder          

for loc in locations:
    print loc +",",

# scraperwiki.sqlite.save(unique_keys = ['locations'], data = locations)

#    print lxml.html.tostring(el)