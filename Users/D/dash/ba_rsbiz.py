#
import scraperwiki
import lxml.html
from bs4 import BeautifulSoup

def scrape_first_page():
    url_to_scrape = 'http://www.business-rs.ba/PrivredniSubjekti.aspx'
    html = scraperwiki.scrape(url_to_scrape)
    soup = BeautifulSoup(html)
    maintable = soup.find('table', id = 'ctl00_cphPKRSWeb_GridView1')
    for row in maintable.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) != 6:
            continue
        data = {}
        data['jib'] = cells[0].string
        data['name'] = cells[1].string
        data['municipalities'] =  cells[2].string
        data['code_activities'] =  cells[3].string
        data['prevailing_activity'] = cells[4].string

        scraperwiki.sqlite.save(unique_keys = ['jib'], data = data)       

scrape_first_page()

#
import scraperwiki
import lxml.html
from bs4 import BeautifulSoup

def scrape_first_page():
    url_to_scrape = 'http://www.business-rs.ba/PrivredniSubjekti.aspx'
    html = scraperwiki.scrape(url_to_scrape)
    soup = BeautifulSoup(html)
    maintable = soup.find('table', id = 'ctl00_cphPKRSWeb_GridView1')
    for row in maintable.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) != 6:
            continue
        data = {}
        data['jib'] = cells[0].string
        data['name'] = cells[1].string
        data['municipalities'] =  cells[2].string
        data['code_activities'] =  cells[3].string
        data['prevailing_activity'] = cells[4].string

        scraperwiki.sqlite.save(unique_keys = ['jib'], data = data)       

scrape_first_page()

