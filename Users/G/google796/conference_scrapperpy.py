import scraperwiki

# Blank Python
import scraperwiki
from lxml import etree
import urllib2
QUERY = "Cloud Computing"

base_url = "http://lanyrd.com"

search_url = base_url+"/search/?context=future&q=%s&type=conference"% (urllib2.quote(QUERY))
conferenceUrls = []

## TODO:
## 1. Handle multiple compilations
## 2. Check for multiple pages

conference_data = {}
count = 0
try:
    data = scraperwiki.scrape(search_url)
    data = etree.HTML(data)
    dxpath = data.xpath("/html/body/div[2]/div[4]/div/div[2]/div/ol/li/h3/a")
    for element in dxpath:
        href = element.get("href",None)
        c_url = base_url +href
        conferenceUrls.append(c_url)
    
    for url in conferenceUrls:
        print "URL:"+url
        data = scraperwiki.scrape(url)
        data = etree.HTML(data)
        try:
            city = data.xpath("//a[contains(@class,'sub-place')]/text()")[0]
            country = data.xpath("//a[contains(@class,'sub-place')]")[0]
            #country = country.getParent()
            #country = data.xpath("//p[contains(@class,'prominent-place')")[1]
            country = country.getparent()[2]
            country = country[0].text
            print "Country:",country
            name = data.xpath("//h1[contains(@class,'summary')]/text()")[0]
            tagLine = data.xpath("//h2[contains(@class,'tagline')]/text()")[0]
            date = data.xpath("//abbr[contains(@class,'dtstart')]")[0]
            date = date.get("title",None)
            conferenceUrl = data.xpath("//a[contains(@class,'icon url website')]")[0]
            conferenceUrl = conferenceUrl.get("href",None)
            count += 1
            conference_data["name"] = name
            conference_data["tagLine"] = tagLine
            conference_data["date"] = date
            conference_data["url"] = conferenceUrl
            conference_data["id"] = count
            conference_data["city"] = city
            #conference_data["country"] = country
            scraperwiki.sqlite.save(["id"], conference_data)
        except Exception,e:
            print "Exception:%s" %e

except Exception,e:
    print "Error fetching data. Exception:%s" %e
