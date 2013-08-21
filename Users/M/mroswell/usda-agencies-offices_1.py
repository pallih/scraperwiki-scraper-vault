mport scraperwiki
import lxml.html   

html = scraperwiki.scrape("http://www.usda.gov/wps/portal/usda/usdahome?navid=AGENCIES_OFFICES_C")
root = lxml.html.fromstring(html)


for item in root.cssselect(".BodyTextBlack"):
    links = item.cssselect('a')
    group = item.cssselect('strong')
    descrip = item.cssselect('p')
#    for link in links:
#        url = link.attrib.get('href')
        url = "http://www.usda.gov" + url
    for agency in group:
        agency = agency.text_content()
    for description in descrip:
        description = description.text_content()

    entity = {'agency' : agency,
              'description' : description,
              'url' : url
             }


    scraperwiki.sqlite.save(unique_keys=['description'], data=entity)mport scraperwiki
import lxml.html   

html = scraperwiki.scrape("http://www.usda.gov/wps/portal/usda/usdahome?navid=AGENCIES_OFFICES_C")
root = lxml.html.fromstring(html)


for item in root.cssselect(".BodyTextBlack"):
    links = item.cssselect('a')
    group = item.cssselect('strong')
    descrip = item.cssselect('p')
#    for link in links:
#        url = link.attrib.get('href')
        url = "http://www.usda.gov" + url
    for agency in group:
        agency = agency.text_content()
    for description in descrip:
        description = description.text_content()

    entity = {'agency' : agency,
              'description' : description,
              'url' : url
             }


    scraperwiki.sqlite.save(unique_keys=['description'], data=entity)import scraperwiki
import lxml.html   

html = scraperwiki.scrape("http://www.usda.gov/wps/portal/usda/usdahome?navid=AGENCIES_OFFICES_C")
root = lxml.html.fromstring(html)


for item in root.cssselect(".BodyTextBlack"):
    url = item.cssselect('a')[0]
    agency = item.cssselect('strong')[0]
    description = item.cssselect('p')[0]
#    for link in links:
#        url = link.attrib.get('href')
#    url = "http://www.usda.gov" + url
#    for agency in group:
#        agency = agency.text_content()
#    for description in descrip:
#        description = description.text_content()

    entity = {'agency' : agency,
              'description' : description,
              'url' : url
             }


    scraperwiki.sqlite.save(unique_keys=['description'], data=entity)

