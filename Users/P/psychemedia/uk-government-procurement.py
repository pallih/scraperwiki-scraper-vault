###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.businesslink.gov.uk/bdotg/action/detail?type=CAMPAIGN&itemId=1085790117&r.s=e&r.lc=en&r.i=1085790107&r.t=CAMPAIGN'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)
start=soup.find(text='Browse published tender documents')
rows=start.findAllNext('tr')

for row in rows:
    cells=row.findAll('td')
    if len(cells)>0:
        cells=row.findAll('td')
        reference=cells[0].text
        organisation=cells[1].text
        url=cells[2].a['href']
        title=cells[2].a.text
        value=cells[3].text
        date=cells[4].text
        value=value.replace('&pound;','')
        value=value.replace(',','')
        if value=='Unknown':
            value=0
        record = {'Reference':reference,'Organisation':organisation,'URL':url,'Title':title,'Value':value,'Date':date}
        scraperwiki.datastore.save(["Reference"], record)
'''
# use BeautifulSoup to get all <td> tags
tds = soup.findAll('td') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.datastore.save(["td"], record) 
''' 