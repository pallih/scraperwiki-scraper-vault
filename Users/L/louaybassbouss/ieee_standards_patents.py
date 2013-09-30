#############################################################
# scraper for http://standards.ieee.org/db/patents/index.html
#############################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

def scrape_page(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    table = soup.find("table",border=1)
    rows = table.findAll("tr")
    rows.pop(0)
    for row in rows:
        record = {}
        cols = row.findAll("td")
        record['standard_no'] = cols[0].font.text.strip()
        record['patent_owner'] = cols[1].font.text.strip()
        record['contact_for_license'] = cols[2].font.text.strip()
        record['patent_no'] = cols[3].font.text.strip()
        record['letter_date'] = cols[4].font.text.strip()
        record['assurance_received'] = cols[5].font.text.strip()
        record['revision_date'] = cols[6].font.text.strip()
        scraperwiki.datastore.save(['standard_no','patent_owner','patent_no'], record)
    
    '''
    i = 0
    record = None
    count = 0
    for row in rows:
        strong = row.find("strong", text = "Company")
        if strong:
            i = 1
            record = {}
            continue
        strong = row.find("strong", text = "Patent title")
        if strong:
            i = 2
        else:
            strong = row.find("strong", text = "Country of registration")
            if strong:
                i = 3

        if i == 1:
            cols = row.findAll("td",recursive=False)
            record['company'] = cols[1].text.strip()
            record['publication_no'] = cols[2].text.strip()
            record['application_no'] = cols[3].text.strip()
            record['deliverable_no'] = cols[4].text.strip()
            record['section'] = cols[5].text.strip()
            record['version'] = cols[6].text.strip()
            record['projects'] = cols[7].text.strip()
            record['declaration_date'] = cols[8].text.strip()
            i=0
        if i == 2:
            record['patent_title'] = strong.findNext(text=True).strip()
            i=0
        if i == 3:
            cols = row.findAll("tr")[1].findAll("td")
            record['country_of_registration'] = cols[1].text.strip()
            record['applicable_countries'] = cols[2].text.strip().split("&nbsp;-&nbsp;")
            scraperwiki.datastore.save(['company','publication_no','application_no','projects','declaration_date'], record)
            count = count+1
            i=0
    return count
'''    
        
def run():
    url = "http://standards.ieee.org/db/patents/index.html"
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    links = soup.findAll("a",href=re.compile('http://standards\\.ieee\\.org/db/patents/'))
    
    for a in links:
        try:
            #print a
            scrape_page(a['href'])
        except:
            pass

print "begin"
#scrape_page("http://standards.ieee.org/db/patents/pat31.html")
run()

    #############################################################
# scraper for http://standards.ieee.org/db/patents/index.html
#############################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

def scrape_page(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    table = soup.find("table",border=1)
    rows = table.findAll("tr")
    rows.pop(0)
    for row in rows:
        record = {}
        cols = row.findAll("td")
        record['standard_no'] = cols[0].font.text.strip()
        record['patent_owner'] = cols[1].font.text.strip()
        record['contact_for_license'] = cols[2].font.text.strip()
        record['patent_no'] = cols[3].font.text.strip()
        record['letter_date'] = cols[4].font.text.strip()
        record['assurance_received'] = cols[5].font.text.strip()
        record['revision_date'] = cols[6].font.text.strip()
        scraperwiki.datastore.save(['standard_no','patent_owner','patent_no'], record)
    
    '''
    i = 0
    record = None
    count = 0
    for row in rows:
        strong = row.find("strong", text = "Company")
        if strong:
            i = 1
            record = {}
            continue
        strong = row.find("strong", text = "Patent title")
        if strong:
            i = 2
        else:
            strong = row.find("strong", text = "Country of registration")
            if strong:
                i = 3

        if i == 1:
            cols = row.findAll("td",recursive=False)
            record['company'] = cols[1].text.strip()
            record['publication_no'] = cols[2].text.strip()
            record['application_no'] = cols[3].text.strip()
            record['deliverable_no'] = cols[4].text.strip()
            record['section'] = cols[5].text.strip()
            record['version'] = cols[6].text.strip()
            record['projects'] = cols[7].text.strip()
            record['declaration_date'] = cols[8].text.strip()
            i=0
        if i == 2:
            record['patent_title'] = strong.findNext(text=True).strip()
            i=0
        if i == 3:
            cols = row.findAll("tr")[1].findAll("td")
            record['country_of_registration'] = cols[1].text.strip()
            record['applicable_countries'] = cols[2].text.strip().split("&nbsp;-&nbsp;")
            scraperwiki.datastore.save(['company','publication_no','application_no','projects','declaration_date'], record)
            count = count+1
            i=0
    return count
'''    
        
def run():
    url = "http://standards.ieee.org/db/patents/index.html"
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    links = soup.findAll("a",href=re.compile('http://standards\\.ieee\\.org/db/patents/'))
    
    for a in links:
        try:
            #print a
            scrape_page(a['href'])
        except:
            pass

print "begin"
#scrape_page("http://standards.ieee.org/db/patents/pat31.html")
run()

    