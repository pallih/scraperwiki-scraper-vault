###########################################################################################
# scraper for http://www.statistik-berlin-brandenburg.de/Statistiken/inhalt-statistiken.asp
###########################################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from sets import Set

def run(url):
        visited = Set()
        queue = [{'url':url, 'id':None, 'name': None, 'level':0}]
        while len(queue)>0:
            parent = queue.pop()
            html = scraperwiki.scrape(parent['url'])
            soup = BeautifulSoup(html)
            topics_div = soup.find('div',id='mid-col-1')
            topics_table = topics_div.find('table')
            topics_a = topics_table.findAll('a')
            parent_id = parent['id']
            level = parent['level']+1
            for topic in topics_a:
                name = topic.text
                description = topic.text
                href = topic['href']
                if topic.text == "Pressemitteilungen":
                    continue
                if topic.text == "Basisdaten":
                    name = parent['name']
                    description = parent['name']
                t = re.match(r".*Ptyp=(100|300).*", href)
                if t!=None:
                    id = re.match(r".*&Sageb=(?P<id>\w+)&.*", href).group('id')
                    if id not in visited:
                        visited.add(id)
                        record = {'id': id, 'name': name, 'description': description, 'level': level, 'parent': parent_id}
                        scraperwiki.datastore.save(['id'], record)
                        queue.insert(0,{'url': 'http://www.statistik-berlin-brandenburg.de/statistiken/'+href, 'id': id, 'name': name , 'level': level})

run('http://www.statistik-berlin-brandenburg.de/statistiken/inhalt-statistiken.asp')
