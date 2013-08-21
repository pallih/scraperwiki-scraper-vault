import scraperwiki




import scraperwiki
import mechanize
import re
import lxml.html
import string

bocbnk_content_base_url = "http://web.boc.lk/phpsqlajax_genxml.php?area="
bocbnk_url = "http://web.boc.lk/phpsqlajax_genxml.php?area="

print "BOC locations base Url " + bocbnk_url

current_page_url = bocbnk_url
print current_page_url
html = scraperwiki.scrape(current_page_url)
print html

root = lxml.html.fromstring(html)

idx = 0
for table in root.cssselect("marker"):

    idx += 1
    row=[]
    adHeader = table.attrib['name']
    print adHeader

    location = table.attrib['address'] +  ", " + table.attrib['office']+  ", " + table.attrib['name']
    print location

    price = "" 
    print price #todo extract price

    content_url = "http://web.boc.lk/index.php?route=information/ournetwork"
    print content_url

    latLon = table.attrib['lat'] + ", " + table.attrib['lng']
    print latLon
   
    scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"BOCBNK", "latLon":latLon})

print "completed scrapping"