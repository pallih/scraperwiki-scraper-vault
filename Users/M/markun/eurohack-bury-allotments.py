import scraperwiki
from lxml.html import parse

# Blank Python

url = "http://www.bury.gov.uk/index.aspx?articleid=3222"

def getAllotments(url):
    html = parse(url).getroot()
    
    table = html.cssselect('#bodytext')[0].cssselect('tr')
    table.pop(0) #remove header
    
    for row in table:
        allotment = {}
        cells = row.cssselect('td')
        allotment['sitename'] = cells[0].text_content().strip()
        allotment['contact'] = cells[1].text_content().strip()
        allotment['total_plots'] = cells[2].text_content().strip()
        allotment['s_or_ns'] = cells[3].text_content().strip()
        allotment['id'] = allotment['sitename']
        scraperwiki.sqlite.save(['id'], allotment)
        #print allotment

def getDetails(url):
    pass


getAllotments(url)
