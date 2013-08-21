import scraperwiki
import mechanize
import re
import lxml.html
import string

property_content_base_url = "http://www.yamu.lk/placecategory/restaurants/page/2/"
property_url = "http://www.yamu.lk/placecategory/restaurants/page/"

property_length=list(range(1,10))

print "Yamu base Url " + property_url

idx = 0
for i in property_length:
    current_page_url = property_url + (str(i)) 
    print current_page_url
    html = scraperwiki.scrape(current_page_url)
    print html

    root = lxml.html.fromstring(html)

    
    for table in root.cssselect(".place.type-place.status-publish.hentry.post"):
        idx += 1
        row=[]
        adHeader = table.cssselect(".post_content h2 a")[0].text_content()
        print adHeader

        locations = table.cssselect(".address")

        if(len(locations) > 0):
            location = table.cssselect(".address")[0].text_content()
            print location
        else:
            location = ""
            print location

        thumbnailUrl = table.cssselect("a.post_img img")[0].attrib['src']
        print thumbnailUrl

        price = ""#table.cssselect("span.normalTxtLarge")[0].text_content()
        print price #todo extract price

        content_url = table.cssselect(".post_content h2 a")[0].attrib['href']
        print content_url

        #try to grab the coordinates
        content_html = scraperwiki.scrape(content_url)

        #content_tree = lxml.html.fromstring(content_html)

        #m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", content_html)
        #m  = re.search(r"(?P<latitude>\d+)\.(?P<latitude_dec>\d+), (?P<longitude>\d+)\.(?P<longitude_dec>\d+)", content_html)
        m  = re.search(r"\\maps?ll=(?P<latitude>\d+)\.(?P<latitude_dec>\d+),(?P<longitude>\d+)\.(?P<longitude_dec>\d+)&", content_html)
        print m
           
        latitude = m.group('latitude') + "." + m.group('latitude_dec')
        print latitude
        longitude = m.group('longitude') + "." + m.group('longitude_dec')
        print longitude

        scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"YMU", "lat":latitude, "lon": longitude, "thumbnail_url":thumbnailUrl})

print "completed scrapping"

