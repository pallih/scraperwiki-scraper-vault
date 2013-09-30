#####################################################################
# scraper for http://maerker.brandenburg.de/lis/list.php?page=maerker
#####################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

def scrape_complaints(m_url,m_id):
    html = scraperwiki.scrape(m_url)
    soup = BeautifulSoup(html)
    table = soup.find('table',{"summary" : "Aktuellste Meldungen"})
    next = soup.find(lambda tag: tag.name == 'a' and tag.text == 'weiter')
    if table:
        rows = table.findAll('tr')
        for r in rows:
            cols = r.findAll('td')
            if len(cols) == 4:
                col = cols[1]
                match = re.match(r"(?P<title>.*)\(ID (?P<id>.*?)\)", col.find('h4').text)
                id = match.group('id').strip()
                title = match.group('title').strip()
                category = col.find('strong').text.strip()
                description = col.p.nextSibling.strip()
                col = cols[2]
                p = col.findAll('p')
                i=0
                street = None
                m_name = None
                if len(p) == 2:                    
                    street = p[i].contents[2].strip()
                    m_name = p[i].contents[0].strip()
                    i = i +1
                strong = p[i].findAll('strong')
                date = strong[0].text
                time = strong[1].text.replace(' Uhr','')
                col = cols[3]
                a = col.find('a')
                image = None
                if a:
                    image = "http://maerker.brandenburg.de" + a['href']
                    
            if len(cols) == 1:
                col = cols[0]
                strong = col.find('strong')
                if strong:
                    status = re.match(r"Status: (?P<status>.*?) \(.*", col.find('strong').text).group('status')
                    record = {'id': id, 'title': title, 'description': description, 'category': category, 'municipality_id': m_id, 'municipality_name': m_name, 'street': street, 'date': date, 'time': time, 'image': image, 'status': status}
                    scraperwiki.datastore.save(['id'], record)

    if next:
        try:
            scrape_complaints("http://maerker.brandenburg.de"+next["href"],m_id)
        except: 
            pass
        
        
    

def run(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    municipalities_a = soup.findAll('a',href = re.compile(r".*?/lis/list\.php\?page=maerker&sv\[kommune\]=(\d+).*"))
    for municipality in municipalities_a:
        m_href = municipality['href']
        m_url = "http://maerker.brandenburg.de"+m_href
        m_id = re.match(r".*?/lis/list\.php\?page=maerker&sv\[kommune\]=(?P<id>\d+).*", m_href).group('id')
        try:
            scrape_complaints(m_url,m_id)
            m_url = m_url.replace("page=maerker","page=maerker_archiv")
            scrape_complaints(m_url,m_id)
        except: 
            pass

run('http://maerker.brandenburg.de/lis/list.php?page=maerker')
#scrape_complaints("http://maerker.brandenburg.de/lis/list.php?page=maerker&sv[kommune]=214946","226429")
#####################################################################
# scraper for http://maerker.brandenburg.de/lis/list.php?page=maerker
#####################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

def scrape_complaints(m_url,m_id):
    html = scraperwiki.scrape(m_url)
    soup = BeautifulSoup(html)
    table = soup.find('table',{"summary" : "Aktuellste Meldungen"})
    next = soup.find(lambda tag: tag.name == 'a' and tag.text == 'weiter')
    if table:
        rows = table.findAll('tr')
        for r in rows:
            cols = r.findAll('td')
            if len(cols) == 4:
                col = cols[1]
                match = re.match(r"(?P<title>.*)\(ID (?P<id>.*?)\)", col.find('h4').text)
                id = match.group('id').strip()
                title = match.group('title').strip()
                category = col.find('strong').text.strip()
                description = col.p.nextSibling.strip()
                col = cols[2]
                p = col.findAll('p')
                i=0
                street = None
                m_name = None
                if len(p) == 2:                    
                    street = p[i].contents[2].strip()
                    m_name = p[i].contents[0].strip()
                    i = i +1
                strong = p[i].findAll('strong')
                date = strong[0].text
                time = strong[1].text.replace(' Uhr','')
                col = cols[3]
                a = col.find('a')
                image = None
                if a:
                    image = "http://maerker.brandenburg.de" + a['href']
                    
            if len(cols) == 1:
                col = cols[0]
                strong = col.find('strong')
                if strong:
                    status = re.match(r"Status: (?P<status>.*?) \(.*", col.find('strong').text).group('status')
                    record = {'id': id, 'title': title, 'description': description, 'category': category, 'municipality_id': m_id, 'municipality_name': m_name, 'street': street, 'date': date, 'time': time, 'image': image, 'status': status}
                    scraperwiki.datastore.save(['id'], record)

    if next:
        try:
            scrape_complaints("http://maerker.brandenburg.de"+next["href"],m_id)
        except: 
            pass
        
        
    

def run(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    municipalities_a = soup.findAll('a',href = re.compile(r".*?/lis/list\.php\?page=maerker&sv\[kommune\]=(\d+).*"))
    for municipality in municipalities_a:
        m_href = municipality['href']
        m_url = "http://maerker.brandenburg.de"+m_href
        m_id = re.match(r".*?/lis/list\.php\?page=maerker&sv\[kommune\]=(?P<id>\d+).*", m_href).group('id')
        try:
            scrape_complaints(m_url,m_id)
            m_url = m_url.replace("page=maerker","page=maerker_archiv")
            scrape_complaints(m_url,m_id)
        except: 
            pass

run('http://maerker.brandenburg.de/lis/list.php?page=maerker')
#scrape_complaints("http://maerker.brandenburg.de/lis/list.php?page=maerker&sv[kommune]=214946","226429")
