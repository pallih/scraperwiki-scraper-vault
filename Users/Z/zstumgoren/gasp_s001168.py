from pyquery import PyQuery as pq
import scraperwiki

BASE_URL = 'http://sarbanes.house.gov'
BIOGUIDE_ID = 'S001168'

gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper("100cb49eec17480db65becac765a495d", BIOGUIDE_ID)

def scrape_bio():
    
    url = BASE_URL + '/free_details.asp?id=44#bio'
    html = scraperwiki.scrape(url)
    graphs = [pq(graph).text().replace(u'\xa0', u'').strip() 
              for graph in pq(html)('div.bodyblock span')]
                  
    bio = "\n\n".join(graphs)
    gasp.add_biography(bio, url=url)

scrape_bio()

gasp.finish()