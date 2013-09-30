#####################################################################
# scraper for http://maerker.brandenburg.de/lis/list.php?page=maerker
#####################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

def run(url):
    html = scraperwiki.scrape(url)
    #soup = BeautifulStoneSoup(html,convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    soup = BeautifulSoup(html)
    municipalities_a = soup.findAll('a',href = re.compile(r".*?/lis/list\.php\?page=maerker&sv\[kommune\]=(\d+).*"))
    for municipality in municipalities_a:
        href = municipality['href']
        id = re.match(r".*?/lis/list\.php\?page=maerker&sv\[kommune\]=(?P<id>\d+).*", href).group('id')
        name = municipality.text
        record = {'id': id, 'name': name}
        scraperwiki.datastore.save(['id'], record)
        
run('http://maerker.brandenburg.de/lis/list.php?page=maerker')
    #####################################################################
# scraper for http://maerker.brandenburg.de/lis/list.php?page=maerker
#####################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

def run(url):
    html = scraperwiki.scrape(url)
    #soup = BeautifulStoneSoup(html,convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    soup = BeautifulSoup(html)
    municipalities_a = soup.findAll('a',href = re.compile(r".*?/lis/list\.php\?page=maerker&sv\[kommune\]=(\d+).*"))
    for municipality in municipalities_a:
        href = municipality['href']
        id = re.match(r".*?/lis/list\.php\?page=maerker&sv\[kommune\]=(?P<id>\d+).*", href).group('id')
        name = municipality.text
        record = {'id': id, 'name': name}
        scraperwiki.datastore.save(['id'], record)
        
run('http://maerker.brandenburg.de/lis/list.php?page=maerker')
    