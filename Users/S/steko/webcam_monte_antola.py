###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from time import time
from BeautifulSoup import BeautifulSoup


# webcams
cams = ['antola', 'nava', 'beigua', 'aiona']

for c in cams:
    
    # retrieve a page 
    starting_url = 'http://www.altaviadeimontiliguri.it/portale/it/meteocam_data.wp?postazione=%s&imgdim=standard' % c
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)

    # use BeautifulSoup to get all <td> tags
    text = soup.findAll(attrs={'class':'centerText'}) 
    img = soup.findAll(attrs={'id':'AltaVia_Text'})[1:]
    for i in img:
        data = {'imgurl':i['src'], 'time':time()}
        scraperwiki.sqlite.save(unique_keys=['imgurl'], data=data)
