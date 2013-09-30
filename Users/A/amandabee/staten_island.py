import scraperwiki
from bs4 import BeautifulSoup

import urlparse


# url = 'http://www.nyc.gov/html/cau/html/cb/si.shtml'

url = 'http://fawcetthospital.com/patient-financial/index.dot?page_name=pricing'


html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)

print soup




for community_board in soup.find_all('table', {'class':'cb_table'}):
    try:
        print community_board['class']
    except:
        continue
    
    cb_name = community_board.td.get_text()
    nested_table = community_board.table

    rows = (nested_table.find_all('tr'))

    cb_neighborhoods = rows[0].find('td', {"class":"cb_text"}).get_text()
    cb_precinct = rows[2].find('td', {"class":"cb_text"}).get_text()
    cb_precinct_phone = rows[3].find('td', {"class":"cb_text"}).get_text()

    
    for anchor in rows[1].find('td', {"class":"cb_text"}).find_all('a'):
        print anchor.contents, anchor.get('href')
        cb_website = anchor.get('href')


    for chunk in rows[1].find('td', {"class":"cb_text"}).find_all("b"):
        print chunk

        for s,sibling in enumerate(chunk.next_siblings):
            if s < 3:
                print s, sibling
                try:
                    print sibling.tag
                except:
                    continue



    leadership = rows[1].find('td', {"class":"cb_text"}).p
    print leadership
    print type(leadership)



    
import scraperwiki
from bs4 import BeautifulSoup

import urlparse


# url = 'http://www.nyc.gov/html/cau/html/cb/si.shtml'

url = 'http://fawcetthospital.com/patient-financial/index.dot?page_name=pricing'


html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)

print soup




for community_board in soup.find_all('table', {'class':'cb_table'}):
    try:
        print community_board['class']
    except:
        continue
    
    cb_name = community_board.td.get_text()
    nested_table = community_board.table

    rows = (nested_table.find_all('tr'))

    cb_neighborhoods = rows[0].find('td', {"class":"cb_text"}).get_text()
    cb_precinct = rows[2].find('td', {"class":"cb_text"}).get_text()
    cb_precinct_phone = rows[3].find('td', {"class":"cb_text"}).get_text()

    
    for anchor in rows[1].find('td', {"class":"cb_text"}).find_all('a'):
        print anchor.contents, anchor.get('href')
        cb_website = anchor.get('href')


    for chunk in rows[1].find('td', {"class":"cb_text"}).find_all("b"):
        print chunk

        for s,sibling in enumerate(chunk.next_siblings):
            if s < 3:
                print s, sibling
                try:
                    print sibling.tag
                except:
                    continue



    leadership = rows[1].find('td', {"class":"cb_text"}).p
    print leadership
    print type(leadership)



    
