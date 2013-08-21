import scraperwiki
import re
import urllib
from BeautifulSoup import BeautifulSoup
from datetime import date
from datetime import timedelta

base = "http://standards.ieee.org";
def scrape_home_page():
    html = scraperwiki.scrape(base+'/about/sasb/patcom/patents.html')
    html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    div = html.find('div', { "id" : "text-content" })
    ul = div.find('ul')
    links = ul.findAll('a');
    for a in links:
        scrape_patent_page(base+a['href'])

def scrape_patent_page(url):
    html = scraperwiki.scrape(url)
    html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    div = html.find('div', { "id" : "text-content" })
    table = div.find('table')
    rows = table.findAll('tr')
    rows.pop(0)
    for r in rows:
        cols = r.findAll('td')
        item = {}
        for i in range(0,len(cols)):
            col = cols[i]
            if i == 0:
                item['reference'] = col.text
            elif i== 1:
                item['patent_owner'] = col.text
            elif i==2:
                item['contact_for_license'] = col.text
            elif i == 3:
                item['patent_no'] = col.text
            elif i == 4:
                item['letter_date'] = col.text
            elif i==5:
                item['assurance_received'] = col.text == 'yes'
            elif i == 6:
                item['date_record_entered'] = col.text
                scraperwiki.sqlite.save(unique_keys=['reference','patent_owner'], data = item)

scrape_home_page()