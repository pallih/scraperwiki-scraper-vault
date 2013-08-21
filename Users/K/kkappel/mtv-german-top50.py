###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

starting_url = 'http://www.mtv.de/win'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)
charts = soup.findAll('tr')
                    
for chart in charts:
#    if chart['class'].find('ch_artist') == -1:
#           continue
    record = {
        'ch_track': None,
        'ch_artist': None,
        'ch_place': None,
        'ch_last': None,
    }              
    tds = chart.findAll('td')

    for artist in tds.findAll('ch_artist'):
        try:
            if artist['class'].find('ch_artist') != -1:
                record['artist'] = span.findAll('artist',{'class':'ch_artist'})[0].text[:-6]
        except:
            pass


    #    scraperwiki.datastore.save(["td"], record) 
    