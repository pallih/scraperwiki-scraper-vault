import scraperwiki 
import lxml.html
from lxml import etree

html = scraperwiki.scrape("http://www.roughguides.com/website/search/DestinationSearch.aspx?q=france") 



root = lxml.html.fromstring(html)
table = root.get_element_by_id('ctl00_cphMidlePanel_GridView1')
#print table.text_content()
print etree.tostring(table)
#print table.find_class('NormalText')
        
#for child in table.find_class('NormalText'):
 #print(child.tag)
#print etree.tostring(child)
import scraperwiki 
import lxml.html
from lxml import etree

html = scraperwiki.scrape("http://www.roughguides.com/website/search/DestinationSearch.aspx?q=france") 



root = lxml.html.fromstring(html)
table = root.get_element_by_id('ctl00_cphMidlePanel_GridView1')
#print table.text_content()
print etree.tostring(table)
#print table.find_class('NormalText')
        
#for child in table.find_class('NormalText'):
 #print(child.tag)
#print etree.tostring(child)
