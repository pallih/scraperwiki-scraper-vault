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

    lat = table.attrib['lat'] 
    print lat

    lon = table.attrib['lng'] 
    print lon
   
    scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"BOCBNK", "lat":lat, "lon": lon})

print "completed scrapping bank of ceylon"

import scraperwiki
import mechanize
import re
import lxml.html
import string

combank_content_base_url = "http://www.combank.net/newweb/branch-network/branch-directory"
combank_url = "http://www.combank.net/newweb/branch-network/branch-directory"

print "Combank base Url " + combank_url

current_page_url = combank_url
print current_page_url
html = scraperwiki.scrape(current_page_url)
print html

root = lxml.html.fromstring(html)

idx = 0
for table in root.cssselect(".branch-office"):

    idx += 1
    row=[]
    adHeader = table.cssselect("p.branch-name")[0].text_content()
    print adHeader

    location = table.cssselect("p")[1].text_content() + ", " + table.cssselect("p")[2].text_content()
    print location

    price = "" 
    print price #todo extract price

    content_url = "http://www.combank.net/newweb/branch-network/branch-directory#branch-" + adHeader[:1].lower()
    print content_url
   
    scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"CBNK"})

print "completed scrapping combank"import scraperwiki




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

    lat = table.attrib['lat'] 
    print lat

    lon = table.attrib['lng'] 
    print lon
   
    scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"BOCBNK", "lat":lat, "lon": lon})

print "completed scrapping bank of ceylon"

import scraperwiki
import mechanize
import re
import lxml.html
import string

combank_content_base_url = "http://www.combank.net/newweb/branch-network/branch-directory"
combank_url = "http://www.combank.net/newweb/branch-network/branch-directory"

print "Combank base Url " + combank_url

current_page_url = combank_url
print current_page_url
html = scraperwiki.scrape(current_page_url)
print html

root = lxml.html.fromstring(html)

idx = 0
for table in root.cssselect(".branch-office"):

    idx += 1
    row=[]
    adHeader = table.cssselect("p.branch-name")[0].text_content()
    print adHeader

    location = table.cssselect("p")[1].text_content() + ", " + table.cssselect("p")[2].text_content()
    print location

    price = "" 
    print price #todo extract price

    content_url = "http://www.combank.net/newweb/branch-network/branch-directory#branch-" + adHeader[:1].lower()
    print content_url
   
    scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"CBNK"})

print "completed scrapping combank"