import scraperwiki

# Blank Python


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

print "completed scrapping"