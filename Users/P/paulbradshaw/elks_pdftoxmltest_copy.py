import scraperwiki
import urllib2
import lxml.etree
from geopy import geocoders  

url = "http://www.staffssaferroads.co.uk/media/114997/03092012_forwebsite.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print xmldata

data_cull = []

def geoCode(address):
    #base_url = http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20geo.placefinder%20where%20text%3D%22sfo%22&diagnostics=true 
    #http://where.yahooapis.com/geocode?q=1600+Pennsylvania+Avenue,+Washington,+DC&appid=[yourappidhere]
    url_part1 = "http://where.yahooapis.com/geocode?q="
    url_part2 = "&appid=LKeT9Q4k"
    address = "Staffordshire: " +address+", United Kingdom"
    address = address.replace(" ", "+")
    address = address.replace (".", "")
    
    combined_url = url_part1+address+url_part2
    
    
    #print combined_url
    address_xml = scraperwiki.scrape(combined_url)
    #print address_xml
    address_root = lxml.etree.fromstring(address_xml)
    longitude = address_root.xpath("//longitude")
    latitude = address_root.xpath("//latitude")
    return longitude[0].text, latitude[0].text


root = lxml.etree.fromstring(xmldata)
#scoop every <text element with font attribute into lines array
lines = root.findall('.//text')
index = 0
day_data = ""
for li in lines:
    record = {}
    numb = li.get("font")
    #print index
    
    if numb == "3":
        day_data = li.xpath("string()")#leave the text behind.
        continue
    if numb =="5" and len(li.text)>4:
        index += 1
        locale = geoCode(li.text)
        record['index'] = index
        record['Date'] = day_data
        record['Camera_Location'] = li.text
        record['latitude'] = locale[0]
        record['longitude'] = locale[1]
        print index, day_data, li.text, locale[0], locale[1]  
        scraperwiki.sqlite.save(['index'], record)
            

        
        



print len(data_cull)
print data_cull



import scraperwiki
import urllib2
import lxml.etree
from geopy import geocoders  

url = "http://www.staffssaferroads.co.uk/media/114997/03092012_forwebsite.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print xmldata

data_cull = []

def geoCode(address):
    #base_url = http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20geo.placefinder%20where%20text%3D%22sfo%22&diagnostics=true 
    #http://where.yahooapis.com/geocode?q=1600+Pennsylvania+Avenue,+Washington,+DC&appid=[yourappidhere]
    url_part1 = "http://where.yahooapis.com/geocode?q="
    url_part2 = "&appid=LKeT9Q4k"
    address = "Staffordshire: " +address+", United Kingdom"
    address = address.replace(" ", "+")
    address = address.replace (".", "")
    
    combined_url = url_part1+address+url_part2
    
    
    #print combined_url
    address_xml = scraperwiki.scrape(combined_url)
    #print address_xml
    address_root = lxml.etree.fromstring(address_xml)
    longitude = address_root.xpath("//longitude")
    latitude = address_root.xpath("//latitude")
    return longitude[0].text, latitude[0].text


root = lxml.etree.fromstring(xmldata)
#scoop every <text element with font attribute into lines array
lines = root.findall('.//text')
index = 0
day_data = ""
for li in lines:
    record = {}
    numb = li.get("font")
    #print index
    
    if numb == "3":
        day_data = li.xpath("string()")#leave the text behind.
        continue
    if numb =="5" and len(li.text)>4:
        index += 1
        locale = geoCode(li.text)
        record['index'] = index
        record['Date'] = day_data
        record['Camera_Location'] = li.text
        record['latitude'] = locale[0]
        record['longitude'] = locale[1]
        print index, day_data, li.text, locale[0], locale[1]  
        scraperwiki.sqlite.save(['index'], record)
            

        
        



print len(data_cull)
print data_cull



import scraperwiki
import urllib2
import lxml.etree
from geopy import geocoders  

url = "http://www.staffssaferroads.co.uk/media/114997/03092012_forwebsite.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print xmldata

data_cull = []

def geoCode(address):
    #base_url = http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20geo.placefinder%20where%20text%3D%22sfo%22&diagnostics=true 
    #http://where.yahooapis.com/geocode?q=1600+Pennsylvania+Avenue,+Washington,+DC&appid=[yourappidhere]
    url_part1 = "http://where.yahooapis.com/geocode?q="
    url_part2 = "&appid=LKeT9Q4k"
    address = "Staffordshire: " +address+", United Kingdom"
    address = address.replace(" ", "+")
    address = address.replace (".", "")
    
    combined_url = url_part1+address+url_part2
    
    
    #print combined_url
    address_xml = scraperwiki.scrape(combined_url)
    #print address_xml
    address_root = lxml.etree.fromstring(address_xml)
    longitude = address_root.xpath("//longitude")
    latitude = address_root.xpath("//latitude")
    return longitude[0].text, latitude[0].text


root = lxml.etree.fromstring(xmldata)
#scoop every <text element with font attribute into lines array
lines = root.findall('.//text')
index = 0
day_data = ""
for li in lines:
    record = {}
    numb = li.get("font")
    #print index
    
    if numb == "3":
        day_data = li.xpath("string()")#leave the text behind.
        continue
    if numb =="5" and len(li.text)>4:
        index += 1
        locale = geoCode(li.text)
        record['index'] = index
        record['Date'] = day_data
        record['Camera_Location'] = li.text
        record['latitude'] = locale[0]
        record['longitude'] = locale[1]
        print index, day_data, li.text, locale[0], locale[1]  
        scraperwiki.sqlite.save(['index'], record)
            

        
        



print len(data_cull)
print data_cull



import scraperwiki
import urllib2
import lxml.etree
from geopy import geocoders  

url = "http://www.staffssaferroads.co.uk/media/114997/03092012_forwebsite.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print xmldata

data_cull = []

def geoCode(address):
    #base_url = http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20geo.placefinder%20where%20text%3D%22sfo%22&diagnostics=true 
    #http://where.yahooapis.com/geocode?q=1600+Pennsylvania+Avenue,+Washington,+DC&appid=[yourappidhere]
    url_part1 = "http://where.yahooapis.com/geocode?q="
    url_part2 = "&appid=LKeT9Q4k"
    address = "Staffordshire: " +address+", United Kingdom"
    address = address.replace(" ", "+")
    address = address.replace (".", "")
    
    combined_url = url_part1+address+url_part2
    
    
    #print combined_url
    address_xml = scraperwiki.scrape(combined_url)
    #print address_xml
    address_root = lxml.etree.fromstring(address_xml)
    longitude = address_root.xpath("//longitude")
    latitude = address_root.xpath("//latitude")
    return longitude[0].text, latitude[0].text


root = lxml.etree.fromstring(xmldata)
#scoop every <text element with font attribute into lines array
lines = root.findall('.//text')
index = 0
day_data = ""
for li in lines:
    record = {}
    numb = li.get("font")
    #print index
    
    if numb == "3":
        day_data = li.xpath("string()")#leave the text behind.
        continue
    if numb =="5" and len(li.text)>4:
        index += 1
        locale = geoCode(li.text)
        record['index'] = index
        record['Date'] = day_data
        record['Camera_Location'] = li.text
        record['latitude'] = locale[0]
        record['longitude'] = locale[1]
        print index, day_data, li.text, locale[0], locale[1]  
        scraperwiki.sqlite.save(['index'], record)
            

        
        



print len(data_cull)
print data_cull



