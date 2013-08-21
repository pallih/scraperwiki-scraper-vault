# scrape vancouver city council

import scraperwiki
import re

from BeautifulSoup import BeautifulSoup


def scrape_member(url_base, url):

    soup = BeautifulSoup(scraperwiki.scrape(url_base + url))
    c = soup.find('div', id='content')
    b = soup.find('div', id='rightRail').findAll('div', 'basicBox')[1]

    record = {}
    record['url'] = url_base + url
    record['source_url'] = url_base + url
    record['photo_url'] = url_base + c.find('img', id='feature')['src']
    record['email'] = b.findAll('a')[0]['href'].split('?')[0].replace('mailto:', '')
    record['boundary_url'] = '/boundaries/census-subdivisions/5915022/'

    name = c.find('h1').text.split(' ')
    record['name'] = ' '.join(name[1:]).strip()
    record['elected_office'] = name[0]

    return record
        

url_base = 'http://vancouver.ca'
soup = BeautifulSoup(scraperwiki.scrape(url_base + '/your-government/city-councillors.aspx'))

m = soup.find('ul', 'cov-profile')
members = m.findAll('a')
members.append({ 'href': '/your-government/mayor-gregor-robertson.aspx' })

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')

for a in members:
    r = scrape_member(url_base, a['href'])
    scraperwiki.sqlite.save(['name'], r)