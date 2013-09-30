import scraperwiki
import lxml.html
import re

foreclosure_pages = []
base_url = "http://www4.co.hennepin.mn.us/webforeclosure/"
list_url = base_url + "/resultbyaddress.asp"

html = scraperwiki.scrape(list_url)
root = lxml.html.fromstring(html)
for a in root.cssselect("table a"):
    link = a.attrib['href']
    if 'propertydetail' in link:
        foreclosure_pages.append(base_url + link)

for page in foreclosure_pages:
    foreclosure = {}
    print "Parsing page " + page
    html = scraperwiki.scrape(page)
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("table tr"):
        children = tr.getchildren()
        if len(children) is 2:
            heading = children[0].text_content().replace(":","").replace("\r","").replace("\n","").replace("(s)","s").replace("/"," or ").strip()
            heading = re.sub(' +', ' ', heading)
            value = children[1].text_content().strip()
            foreclosure[heading] = value
    print foreclosure
    scraperwiki.sqlite.save(unique_keys=['Sale Record Number'], data=foreclosure)import scraperwiki
import lxml.html
import re

foreclosure_pages = []
base_url = "http://www4.co.hennepin.mn.us/webforeclosure/"
list_url = base_url + "/resultbyaddress.asp"

html = scraperwiki.scrape(list_url)
root = lxml.html.fromstring(html)
for a in root.cssselect("table a"):
    link = a.attrib['href']
    if 'propertydetail' in link:
        foreclosure_pages.append(base_url + link)

for page in foreclosure_pages:
    foreclosure = {}
    print "Parsing page " + page
    html = scraperwiki.scrape(page)
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("table tr"):
        children = tr.getchildren()
        if len(children) is 2:
            heading = children[0].text_content().replace(":","").replace("\r","").replace("\n","").replace("(s)","s").replace("/"," or ").strip()
            heading = re.sub(' +', ' ', heading)
            value = children[1].text_content().strip()
            foreclosure[heading] = value
    print foreclosure
    scraperwiki.sqlite.save(unique_keys=['Sale Record Number'], data=foreclosure)