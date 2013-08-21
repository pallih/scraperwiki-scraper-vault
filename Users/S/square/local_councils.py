import scraperwiki
from lxml.html import tostring, fromstring

base_url = "http://local.direct.gov.uk/"

def process_maplink(name, url, region, parent_region, country):
    print "Processing link", name, region, parent_region, country
    html = scraperwiki.scrape(base_url + url)
    root = fromstring(html)
    links = root.cssselect("div#mapLinks ul li a")
    if len(links) > 0:
        for maplink in links:
            url = maplink.attrib["href"]
            print 'calling process_maplink', name, region, parent_region, country
            process_maplink(maplink.text_content(), url, name, region, country)
    else:
        links = root.cssselect("div#bodyContent div.rowContainer ul li a")
        contact_us_url = links[0].attrib["href"]      
        homepage_url = links[1].attrib["href"]

        data = {
            'name' : name,
            'contact_us_url' : contact_us_url,
            'homepage_url' : homepage_url, 
            'sub_region' : region if parent_region != None else None,
            'region' : parent_region if parent_region != None else region,
            'country' : country
        }
        print data
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)
        if len(links) > 2:
            raise Error

def run_scraper():
    html = scraperwiki.scrape(base_url + "/LDGRedirect/MapLocationSearch.do?mode=1.1")
    root = fromstring(html)
    maplinks = root.cssselect("div#mapLinks ul li a")
    for maplink in maplinks:
        name = maplink.text_content()
        url = maplink.attrib["href"]
        print 'Top level:', name
        process_maplink(name, url, None, None, 'England')

run_scraper()
