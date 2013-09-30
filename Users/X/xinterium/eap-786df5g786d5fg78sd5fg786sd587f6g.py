import scraperwiki
import mechanize
import re
import lxml.html
import string





THIS NEEDS TO BE CONTINUED


property_content_base_url = "http://www.eapmovies.com/component/eapmovies/?controller=theaters&view=theaterlist&Itemid=112"
property_url = "http://www.eapmovies.com/component/eapmovies/?controller=theaters&view=theaterlist&Itemid=112"

property_length=list(range(1,1))

print "NFC base Url " + property_url

idx = 0

current_page_url = property_url 
print current_page_url
html = scraperwiki.scrape(current_page_url)
print html

root = lxml.html.fromstring(html)

for district in root.cssselect(".district a"):
    
    district_url = district.attrib['href']
    print district_url

    current_page_html = scraperwiki.scrape(district_url)

    district_content = lxml.html.fromstring(current_page_html)
    for table in district_content.cssselect("ul.theatres li"):
        idx += 1
        row=[]
        adHeader = table.cssselect("label")[0].text_content()
        print adHeader
    
        location = table[4].text_content().strip()[:len(table[4].text_content()) -1]
        if len(location) > 0:
            location = location + ", Sri Lanka"
        else:
            continue
        print location
    
        price = ""#table.cssselect("span.normalTxtLarge")[0].text_content()
        print price #todo extract price
    
        content_url = district_url
        print content_url
        
        scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"NFC"})

print "completed scrapping"

import scraperwiki
import mechanize
import re
import lxml.html
import string





THIS NEEDS TO BE CONTINUED


property_content_base_url = "http://www.eapmovies.com/component/eapmovies/?controller=theaters&view=theaterlist&Itemid=112"
property_url = "http://www.eapmovies.com/component/eapmovies/?controller=theaters&view=theaterlist&Itemid=112"

property_length=list(range(1,1))

print "NFC base Url " + property_url

idx = 0

current_page_url = property_url 
print current_page_url
html = scraperwiki.scrape(current_page_url)
print html

root = lxml.html.fromstring(html)

for district in root.cssselect(".district a"):
    
    district_url = district.attrib['href']
    print district_url

    current_page_html = scraperwiki.scrape(district_url)

    district_content = lxml.html.fromstring(current_page_html)
    for table in district_content.cssselect("ul.theatres li"):
        idx += 1
        row=[]
        adHeader = table.cssselect("label")[0].text_content()
        print adHeader
    
        location = table[4].text_content().strip()[:len(table[4].text_content()) -1]
        if len(location) > 0:
            location = location + ", Sri Lanka"
        else:
            continue
        print location
    
        price = ""#table.cssselect("span.normalTxtLarge")[0].text_content()
        print price #todo extract price
    
        content_url = district_url
        print content_url
        
        scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"NFC"})

print "completed scrapping"

