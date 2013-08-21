import scraperwiki
import lxml.html
from lxml import etree

html = scraperwiki.scrape("http://www.lonelyplanet.com/searchResult?q=burma")



root = lxml.html.fromstring(html)
ol = root.get_element_by_id("globalList")

print etree.tostring(ol)

