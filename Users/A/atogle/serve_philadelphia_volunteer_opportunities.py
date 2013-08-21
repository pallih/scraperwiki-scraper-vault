###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import simplejson
import re
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://volunteer.phila.gov/search/search.php'
resp = scraperwiki.scrape(starting_url, {'category_id':'false', 'keyword':'false', 'isPriority':'false', 'pagenum':2, 'sort_by':'false', 'sort_type':'false', 'audiencetype':'false', 'interests':'false', 'skills':'false', 'date':'false', 'cmd':'gethomepagesearch'})

html = simplejson.loads(resp)['html']
soup = BeautifulSoup(html)
divs = soup.findAll('div', {'id' : re.compile('^band')})
records = []
for div in divs:
    record = {}
    cells = div.findAll('td')
    record['opportunity'] = cells[0].text
    record['organization'] = cells[1].text
    record['location'] = cells[2].text
    record['category'] = cells[3].text
    records.append(record)

print records   
#print soup.prettify()