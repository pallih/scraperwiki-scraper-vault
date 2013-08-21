import scraperwiki
import lxml.html

## url to operate on
baseurl = "http://www.olympus.co.uk/site/en/c/cameras/pen_cameras/"
## fetch overview-page
html = scraperwiki.scrape(baseurl + "index.html")

page = lxml.html.fromstring(html)
for cam in page.cssselect("div.item-list ul li.item-list-item")[0:5]:
    ## extract link of detail-page
    detailLink = cam.cssselect("div.article a")[0].attrib['href']
    ## save model-name of camera from overview-page
    camData = {
        "title": cam.cssselect("div.article p.item-category")[0].text_content(),
        "href": detailLink
    }
    
    print camData["title"]
    print detailLink
    
    ## fetch detail-page
    detailPage = lxml.html.fromstring(scraperwiki.scrape(baseurl + detailLink))
    ## extract link to specification page
    specLink = detailPage.cssselect("div.nav3 div.pane ul li a")[2]
    ## make specification-link absolute
    specLink.make_links_absolute(baseurl + detailLink, resolve_base_href=False)
    
    print specLink.attrib['href']
    
    ## fetch specification-page
    specPage = lxml.html.fromstring(scraperwiki.scrape(specLink.attrib['href']))
    
    ## iterate over specification-data and extract to "compAttributes"-dict
    components = specPage.cssselect("div.module div p.header4")
    for c in components:
        compTitle = c.text_content().replace("/", "")
        #print compTitle
        specData = c.getnext().getchildren()
        compAttributes = {}
        for propSet in specData:
            values = propSet.getchildren()
            if ((len(values) == 2) and (len(values[0].text_content()) > 1)):
                #print str(values[1].text_content().encode('utf-8'))
                compKey = values[0].text_content().replace(u"/", "")
                compKey = str(compKey.encode("ascii", errors="ignore"))
                compAttributes[compKey] = str(values[1].text_content().encode('utf-8'))
        if compAttributes:
            camData[str(compTitle)] = compAttributes
    
    ## store data to DB with model-name as unique-key    
    scraperwiki.sqlite.save(unique_keys=['title'], data=camData)    

print "end"

