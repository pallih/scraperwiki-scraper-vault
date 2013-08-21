import scraperwiki
import lxml

xml = lxml.parsefile("https://github.com/mlaa/nvs-challenge/blob/master/xml/coe_playtext.xml") 
print xml
