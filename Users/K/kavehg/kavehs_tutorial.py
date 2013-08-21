import scraperwiki

# Blank Python

import scraperwiki           
# html = scraperwiki.scrape("http://www.etsy.com/category/toys/waldorf")
broken_html = "<html><head><title>test<body><h1>page title</h3>"
import lxml.html
from lxml import etree
import StringIO
parser = etree.HTMLParser()
tree   = etree.parse(StringIO(broken_html), parser)
result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
print result

# for tr in root.cssselect("div[align='left'] tr.tcont"):
#    tds = tr.cssselect("td")
#    data = {
#      'country' : tds[0].text_content(),
#      'years_in_school' : int(tds[4].text_content())
#    }
#    scraperwiki.sqlite.save(unique_keys=['country'], data=data)