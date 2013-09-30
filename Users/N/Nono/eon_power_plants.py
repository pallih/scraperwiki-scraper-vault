import scraperwiki
import lxml.html
from urllib import urlencode
import urlparse
import sys
import demjson


url = "http://www.eon.com/en/about-us/structure/asset-finder.html"


def retrieveCountres(url):

    try:
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
    
    except:
        print sys.exc_info()[0]
        print "Can't download " + url
        return []

    countries = root.xpath("//select[@id='search-area']/option")
    return countries [1:]
        

def parseCountryPage(country, name):

    params = {
        '_charset_': 'UTF-8',
        'arearegion': country,
        'business-area-scope': 'on',
        'go': 'Find Assets'
    }

    global url
    page = url + '?%s' % urlencode(params)

    try:
        html = scraperwiki.scrape(page)
        root = lxml.html.fromstring(html)
    
    except:
        print sys.exc_info()[0]
        print "Can't download " + page
        return

    json = root.xpath("//div[@class='map-canvas']/@data-gmap-options")
    if len(json) > 0:
        data = demjson.decode(json[0].encode('latin1').decode("utf-8"))
        entries = data["marker"][name]
        
        for entry in entries:
            entry["country"] = name
            saveEntry(entry)

        
def saveEntry(entry):
    pplInfo = dict()
    pplInfo["name"] = entry["title"]
    pplInfo["latitude"] = entry["latLng"][0]
    pplInfo["longitude"] = entry["latLng"][1]
    pplInfo["country"] = entry["country"]
    content = entry["tooltipContent"]
    pplInfo.update(content["contact"])
    pplInfo["fuel_type"] = content.get("generationmethod", entry["assetType"].capitalize())
    info = content["information"].replace('<br />','')
    if '<br/>' in info:
        for item in info.split('<br/>'):
            pplInfo.update(dict([item.split(": ")]))
    else:
        pplInfo["information"] = info
    if pplInfo["url"]:
        pplInfo["url"] = urlparse.urljoin(url, pplInfo["url"])
    scraperwiki.sqlite.save(unique_keys=["name"], data=pplInfo)

    

countries = retrieveCountres(url)
for country in countries:
    parseCountryPage(country.xpath("@value")[0], country.xpath("text()")[0])