import scraperwiki
from lxml.html import parse

# Blank Python

url = "http://www.birmingham.gov.uk/cs/Satellite/allotmentsacocksgreen?packedargs=website%3D4&rendermode=live"

def getAllotments(url):
    html = parse(url).getroot()
    
    table = html.cssselect('.main')[0].cssselect('tr')
    table.pop(0) #remove header
    
    for row in table:
        allotment = {}
        cells = row.cssselect('td')
        allotment['ward'] = cells[0].text_content().strip()
        allotment['sitename'] = cells[1].text_content().strip()
        allotment['total_plots'] = cells[2].text_content().strip()
        allotment['facilities'] = cells[3].text_content().strip()
        allotment['id'] = allotment['ward'] + '-' + allotment['sitename']
        scraperwiki.sqlite.save(['id'], allotment)
        #print allotment

def getDetails(url):
    pass


url = "http://www.birmingham.gov.uk/cs/Satellite?c=Page&childpagename=Parks%2FPageLayout&cid=1223092603781&pagename=BCC%2FCommon%2FWrapper%2FWrapper"

html = parse(url).getroot()
links = html.cssselect('.main')[0].cssselect('a')
links.pop(0) # remove email
for link in links:
    getAllotments('http://www.birmingham.gov.uk' + link.get('href'))
import scraperwiki
from lxml.html import parse

# Blank Python

url = "http://www.birmingham.gov.uk/cs/Satellite/allotmentsacocksgreen?packedargs=website%3D4&rendermode=live"

def getAllotments(url):
    html = parse(url).getroot()
    
    table = html.cssselect('.main')[0].cssselect('tr')
    table.pop(0) #remove header
    
    for row in table:
        allotment = {}
        cells = row.cssselect('td')
        allotment['ward'] = cells[0].text_content().strip()
        allotment['sitename'] = cells[1].text_content().strip()
        allotment['total_plots'] = cells[2].text_content().strip()
        allotment['facilities'] = cells[3].text_content().strip()
        allotment['id'] = allotment['ward'] + '-' + allotment['sitename']
        scraperwiki.sqlite.save(['id'], allotment)
        #print allotment

def getDetails(url):
    pass


url = "http://www.birmingham.gov.uk/cs/Satellite?c=Page&childpagename=Parks%2FPageLayout&cid=1223092603781&pagename=BCC%2FCommon%2FWrapper%2FWrapper"

html = parse(url).getroot()
links = html.cssselect('.main')[0].cssselect('a')
links.pop(0) # remove email
for link in links:
    getAllotments('http://www.birmingham.gov.uk' + link.get('href'))
