import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.tutorialspoint.com/python/index.htm")

root = lxml.html.fromstring(html)
for tr in root.cssselect("ul.menu li"):
    if len(tr)>0:
        detailLinkPart = tr[0].attrib['href']
        if not detailLinkPart.startswith('/', 0,len(detailLinkPart)):
            detailLinkPart = "/"+tr[0].attrib['href']
        htmlDetail = scraperwiki.scrape("http://www.tutorialspoint.com"+detailLinkPart )
        rootDetail = lxml.html.fromstring(htmlDetail)
        detailText = rootDetail.cssselect("p")
        data1 = {            
            'Detail' : detailText[0].text_content(),
            'Details_link' : "http://www.tutorialspoint.com"+detailLinkPart,
            'Tutorial' : tr[0].text_content()           
            }         
        scraperwiki.sqlite.save(unique_keys=['Tutorial'], data=data1)

        
import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.tutorialspoint.com/python/index.htm")

root = lxml.html.fromstring(html)
for tr in root.cssselect("ul.menu li"):
    if len(tr)>0:
        detailLinkPart = tr[0].attrib['href']
        if not detailLinkPart.startswith('/', 0,len(detailLinkPart)):
            detailLinkPart = "/"+tr[0].attrib['href']
        htmlDetail = scraperwiki.scrape("http://www.tutorialspoint.com"+detailLinkPart )
        rootDetail = lxml.html.fromstring(htmlDetail)
        detailText = rootDetail.cssselect("p")
        data1 = {            
            'Detail' : detailText[0].text_content(),
            'Details_link' : "http://www.tutorialspoint.com"+detailLinkPart,
            'Tutorial' : tr[0].text_content()           
            }         
        scraperwiki.sqlite.save(unique_keys=['Tutorial'], data=data1)

        
