import scraperwiki
import mechanize
import re
import lxml.html
import string
import urllib
import urllib2
import json

nearby_content_base_url = "http://www.nearby.lk"
property_url = "http://www.nearby.lk/s/Restaurants"

property_length=list(range(1,2))

print "Nearby base Url " + property_url

idx = 0

current_page_url = property_url
print current_page_url
html = scraperwiki.scrape(current_page_url)
print html

root = lxml.html.fromstring(html)


for table in root.cssselect("div.row.result"):
    idx += 1
    row=[]
    adHeader = table.cssselect("h3.name")[0].text_content()
    print adHeader

    locations = table.cssselect(".address")

    if(len(locations) > 0):
        location=""
        for location_part in locations:
            if(len(location_part.text_content().strip())> 0):
                location = location + ", "+ location_part.text_content()
        location = location[2:]
        print location
    else:
        location = ""
        print location

    thumbnails = table.cssselect(".span2 img.icon_image")
    
    thumbnailUrl = ""
    if(len(thumbnails) > 0):
        thumbnailUrl = nearby_content_base_url + table.cssselect(".span2 img.icon_image")[0].attrib['src']
    
    print thumbnailUrl

    price = ""#table.cssselect("span.normalTxtLarge")[0].text_content()
    print price #todo extract price

    content_url = nearby_content_base_url + table.cssselect("a")[0].attrib['href']
    print content_url

    
    #try to grab the coordinates
    content_html = scraperwiki.scrape(content_url)

    entity_name = content_url.split("/")[3]

    url = nearby_content_base_url + "/"
    
    data = "session_id=uXPrdO6rQ0&method=get_entity&data={\"handle\":\"" +  entity_name + "\"}"
        
    response = urllib2.urlopen(urllib2.Request(url, data))

    resp_html = response.read()
    print resp_html
    
    d = json.loads(resp_html)
    latitude = d['data']['lat']
    print latitude

    longitude = d['data']['lng']
    print longitude

    scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"NBY", "lat":latitude, "lon": longitude, "thumbnail_url" : thumbnailUrl})

print "completed scrapping"

