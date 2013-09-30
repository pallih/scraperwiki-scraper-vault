import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

# Blank Python

az = 'Abcdefghijklmnopqrstuvwxyz'
for letter in az:

    url = 'http://www.dft.gov.uk/dsa/AtoZservices_Bannered.asp?Cat=-1&TestType=&TypeID=17&Letter=%s' % letter

    list_html = scraperwiki.scrape(url)
    list_page = BeautifulSoup.BeautifulSoup(list_html)
    
    links = list_page.find('div', {'class': 'formtext first'}).findAll('a')
    for link in links:
        if link['href'].find('AddressDetails_Bannered.asp?id'):
            print 'http://www.dft.gov.uk/dsa/' + link['href']
            centre_html = scraperwiki.scrape('http://www.dft.gov.uk/dsa/' + link['href'])    
            centre_page = BeautifulSoup.BeautifulSoup(centre_html)
            content = centre_page.find('div', {'class': 'formtext first'})
            print content
            
            headings = content.findAll('h3')
            print headingsimport scraperwiki
import BeautifulSoup

from scraperwiki import datastore

# Blank Python

az = 'Abcdefghijklmnopqrstuvwxyz'
for letter in az:

    url = 'http://www.dft.gov.uk/dsa/AtoZservices_Bannered.asp?Cat=-1&TestType=&TypeID=17&Letter=%s' % letter

    list_html = scraperwiki.scrape(url)
    list_page = BeautifulSoup.BeautifulSoup(list_html)
    
    links = list_page.find('div', {'class': 'formtext first'}).findAll('a')
    for link in links:
        if link['href'].find('AddressDetails_Bannered.asp?id'):
            print 'http://www.dft.gov.uk/dsa/' + link['href']
            centre_html = scraperwiki.scrape('http://www.dft.gov.uk/dsa/' + link['href'])    
            centre_page = BeautifulSoup.BeautifulSoup(centre_html)
            content = centre_page.find('div', {'class': 'formtext first'})
            print content
            
            headings = content.findAll('h3')
            print headings