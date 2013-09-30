import scraperwiki
import lxml.html 

html = scraperwiki.scrape("http://www.nhs.uk/ServiceDirectories/Pages/AcuteTrustListing.aspx")     
root = lxml.html.fromstring(html)
for tr in root.cssselect(".trust-list li a"):
    href = tr.attrib['href'].decode()

    innerhtml = scraperwiki.scrape("http://www.nhs.uk/" + href)
    inneroot = lxml.html.fromstring(innerhtml)
    web = inneroot.cssselect(".panel-profile-site .panel-content .pad p a")
    try:
        website = web[0].attrib['href'].decode()
    except:
        website = "parser issue :("
    try:
        title = tr.attrib['title'].decode()
    except:
        title = 'parser issue :('
    if(href.startswith('/Services/')):
        data = {
            'url' : 'http://nhs.uk' + href,
            'name': title.replace('View details for ',''),
            'trust-url': website
            }
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)
import scraperwiki
import lxml.html 

html = scraperwiki.scrape("http://www.nhs.uk/ServiceDirectories/Pages/AcuteTrustListing.aspx")     
root = lxml.html.fromstring(html)
for tr in root.cssselect(".trust-list li a"):
    href = tr.attrib['href'].decode()

    innerhtml = scraperwiki.scrape("http://www.nhs.uk/" + href)
    inneroot = lxml.html.fromstring(innerhtml)
    web = inneroot.cssselect(".panel-profile-site .panel-content .pad p a")
    try:
        website = web[0].attrib['href'].decode()
    except:
        website = "parser issue :("
    try:
        title = tr.attrib['title'].decode()
    except:
        title = 'parser issue :('
    if(href.startswith('/Services/')):
        data = {
            'url' : 'http://nhs.uk' + href,
            'name': title.replace('View details for ',''),
            'trust-url': website
            }
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)
