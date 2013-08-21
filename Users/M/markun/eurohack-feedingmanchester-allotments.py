import scraperwiki
from lxml.html import parse

# Blank Python

url = 'http://feedingmanchester.org.uk/civicrm/profile?force=1&gid=29&crmPID='

def getAllotments(url):
    html = parse(url).getroot()
    
    table = html.cssselect('.crm-search-results')[0].cssselect('tr')
    table.pop(0) #remove header
    
    for row in table:
        allotment = {}
        cells = row.cssselect('td')
        allotment['name'] = cells[1].text_content()
        allotment['address'] = cells[2].text_content()
        allotment['postcode'] = cells[3].text_content()
        allotment['community_plot'] = cells[4].text_content()
        allotment['link'] = cells[5].cssselect('a')[0].get('href')
        scraperwiki.sqlite.save(['name'], allotment)

def getDetails(url):
    pass

for page in range(1,6):
    getAllotments(url+str(page))