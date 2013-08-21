import scraperwiki
from BeautifulSoup import BeautifulStoneSoup

starting_url = 'http://static.reallysimple.org/users/dave/linkblog.xml'
xml = scraperwiki.scrape(starting_url)
soup = BeautifulStoneSoup(xml)

items = soup.findAll('item') 
for item in items:

    description = item.find('description').string if item.find('description') else ""
    link = item.find('link').string if item.find('link') else ""
    pubdate = item.find('pubdate').string if item.find('pubdate') else ""
    guid = item.find('guid').string if item.find('guid') else ""
    linkfull = item.find('microblog:linkfull').string if item.find('microblog:linkfull') else ""
    readcount = item.find('microblog:readcount').string if item.find('microblog:readcount') else ""


    record = { "guid" : guid, "description" : description, "link" : link, "pubdate" : pubdate, "linkfull" : linkfull, "readcount" : readcount }
    scraperwiki.sqlite.save(["guid"], record) 
    