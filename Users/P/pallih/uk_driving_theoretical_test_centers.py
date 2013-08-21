#Theoretical test centres // WORK IN PROGRESS

import scraperwiki,re
from BeautifulSoup import BeautifulSoup
#from string import ascii_uppercase

#print ascii_uppercase

urlbeginning = 'http://www.dft.gov.uk/dsa/dsa_theory_test_az.asp?letter='
urlend = '&CAT=-1&s=&TypeID=18&TestType='

alphabet = map(chr, range(65, 91))


def stripTags(s):
    ''' Strips HTML tags.
        Taken from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/440481
    '''
    intag = [False]
    
    def chk(c):
        if intag[0]:
            intag[0] = (c != '>')
            return False
        elif c == '<':
            intag[0] = True
            return False
        return True
    
    return ''.join(c for c in s if chk(c))


def scrape_letter(url):
    print url
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    soup.prettify()
    div = soup.find('div', 'formtext first')
    links = div.findAll('a')
    for a in links:
        url = 'http://www.dft.gov.uk/dsa/' + a['href']
        scrape_test_center(url)
    if soup.find('div', {'id' : 'pageresults'}):
        next_page_link = soup.find('div', {'id' : 'pageresults'}).a
        next_page_link = 'http://www.dft.gov.uk/dsa/' + next_page_link['href']
        scrape_test_center_next_page(next_page_link)

def scrape_test_center_next_page(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    soup.prettify()
    div = soup.find('div', 'formtext first')
    links = div.findAll('a')
    for a in links:
        url = 'http://www.dft.gov.uk/dsa/' + a['href']
        scrape_test_center(url)
        

def scrape_test_center(url):
    data = {}
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    soup.prettify()
    title = soup.find('h3')
    #print title.text
    address = title.findNext('p')
    address = stripTags(str(address).replace('<br />',', '))
    address = address.replace('\r\n\t \t','')
    data['source_url'] = url
    data['name'] = title.text
    data['address'] = address
    #extract postcode and geocode for maps
    postcode = scraperwiki.geo.extract_gb_postcode(address)
    latlng = scraperwiki.geo.gb_postcode_to_latlng(postcode)
    data['postcode'] = postcode
    data['latlng'] = latlng
    print data
    scraperwiki.datastore.save(["name"], data, latlng=(latlng))


#Theory test centres ID = 18
for letter in alphabet:
    url = urlbeginning + letter + urlend
    #print url
    scrape_letter(url)


#scrape_type('18')

#Practical test centres ID = 17

#scrape_type('17')  



