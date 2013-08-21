import scraperwiki
import lxml.html   
          
pageCounter =  1

while True:
    page = scraperwiki.scrape("http://essen.vol.at/welcome.asp?page=%d" % (pageCounter))        
    root = lxml.html.fromstring(page)

    for entry in root.cssselect('div[class="Entry"]'):
        data={
            "Name":entry.cssselect('div[class="CompanyName"]')[0].text_content(),
            "Street": entry.cssselect('div[class="CompanyStreet"]')[0].text_content(),
            "City" : entry.cssselect('div[class="CompanyPlace"]')[0].text_content()
        }
        scraperwiki.sqlite.save(unique_keys=["Name"], data=data)
    if root.cssselect('a[class="Next"]'):
        pageCounter=pageCounter+1
    else:
        break 