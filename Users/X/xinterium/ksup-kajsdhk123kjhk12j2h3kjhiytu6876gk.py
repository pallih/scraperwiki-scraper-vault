import scraperwiki

# Blank Python


import scraperwiki
import mechanize
import re
import lxml.html
import string

keells_content_base_url = "https://www.keellssuper.com/contentsv2/ContactUs/contactusnew.asp"
keells_url = "https://www.keellssuper.com/contentsv2/ContactUs/contactusnew.asp"

print "Keells Super base Url " + keells_url

current_page_url = keells_url
print current_page_url
html = scraperwiki.scrape(current_page_url)
print html

root = lxml.html.fromstring(html)

idx = 0
for table in root.cssselect("div p")[1:]:

    idx += 1
    row=[]
    adHeader = table.text_content().split(",")[0]
    print adHeader

    location = ",".join(table.text_content().split(",")[1:])
    print location

    price = "" 
    print price #todo extract price

    content_url = keells_url
    print content_url
   
    scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"KSUP"})

print "completed scrapping"