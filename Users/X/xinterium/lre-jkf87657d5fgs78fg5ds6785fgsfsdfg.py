import scraperwiki
import mechanize
import re
import lxml.html
import string
import urllib2

property_content_base_url = "http://www.lankarestaurants.com/show.php"
property_url = "http://www.lankarestaurants.com/show.php"

property_length=list(range(1,1))

print "SLRG base Url " + property_url
    

idx = 0

current_page_url = property_url #+ (str(i)) 
print current_page_url

data = "cmb1=All&cmb2=All&cmb3=All&cmb4=All&cmb5=All&cmb6=All&I2.x=53&I2.y=20&ST=B"
print data
response = urllib2.urlopen(urllib2.Request(property_url, data))
html = response.read()

print html

root = lxml.html.fromstring(html)


for table in root.cssselect("#table78"):
    idx += 1
    row=[]

    tds = table.cssselect("tr")
    adHeader = tds[0].text_content().strip()
    print adHeader

    x = 0
    for td in tds:
        x = x+1
        print str(x) + ":" + td.text_content()

    location = tds[8].text_content()
    print location

    price = ""#table.cssselect("span.normalTxtLarge")[0].text_content()
    print price #todo extract price

    original_content = ""
    content_url = ""
    urls = table.cssselect("a")
    for url in urls:
        print url.text_content()
        if (url.text_content() == "Review"):
            
            content_url = url.attrib['href']
            print "review found : " + content_url
        if (url.text_content() == "Web"):
            original_content = url.attrib['href']
            print "original found : " + original_content
    print content_url
    
    if(len(content_url) > 0):
        m  = re.search(r"'(?P<content_id>\d+)'", content_url)
        print m
    
        if(len(m.group('content_id')) > 0):
            content_url = "http://www.lankarestaurants.com/more1.php?RestName=" + m.group('content_id')
        print content_url
    else:
        if (len(original_content) > 0):
            content_url = original_content

    if (len(original_content) == 0 and len(content_url) == 0):
        content_url = "http://www.lankarestaurants.com"
        

    scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url, "original_url":original_content, "source":"LRE"})

print "completed scrapping"

import scraperwiki
import mechanize
import re
import lxml.html
import string
import urllib2

property_content_base_url = "http://www.lankarestaurants.com/show.php"
property_url = "http://www.lankarestaurants.com/show.php"

property_length=list(range(1,1))

print "SLRG base Url " + property_url
    

idx = 0

current_page_url = property_url #+ (str(i)) 
print current_page_url

data = "cmb1=All&cmb2=All&cmb3=All&cmb4=All&cmb5=All&cmb6=All&I2.x=53&I2.y=20&ST=B"
print data
response = urllib2.urlopen(urllib2.Request(property_url, data))
html = response.read()

print html

root = lxml.html.fromstring(html)


for table in root.cssselect("#table78"):
    idx += 1
    row=[]

    tds = table.cssselect("tr")
    adHeader = tds[0].text_content().strip()
    print adHeader

    x = 0
    for td in tds:
        x = x+1
        print str(x) + ":" + td.text_content()

    location = tds[8].text_content()
    print location

    price = ""#table.cssselect("span.normalTxtLarge")[0].text_content()
    print price #todo extract price

    original_content = ""
    content_url = ""
    urls = table.cssselect("a")
    for url in urls:
        print url.text_content()
        if (url.text_content() == "Review"):
            
            content_url = url.attrib['href']
            print "review found : " + content_url
        if (url.text_content() == "Web"):
            original_content = url.attrib['href']
            print "original found : " + original_content
    print content_url
    
    if(len(content_url) > 0):
        m  = re.search(r"'(?P<content_id>\d+)'", content_url)
        print m
    
        if(len(m.group('content_id')) > 0):
            content_url = "http://www.lankarestaurants.com/more1.php?RestName=" + m.group('content_id')
        print content_url
    else:
        if (len(original_content) > 0):
            content_url = original_content

    if (len(original_content) == 0 and len(content_url) == 0):
        content_url = "http://www.lankarestaurants.com"
        

    scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url, "original_url":original_content, "source":"LRE"})

print "completed scrapping"

