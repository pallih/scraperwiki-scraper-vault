# scrape winnipeg city council

import scraperwiki
import re
import json

from urlparse import urlparse
from urlparse import parse_qs
from BeautifulSoup import BeautifulSoup, Tag


def scrape_member(url_base, url):
    record = {}
    council = re.match(r'(.*)\.stm', url)

    if council:
        s = '/council/' + url
        record['url'] = url_base + s
    else:
        s = url + 'contact.stm'
        record['url'] = url_base + url

    record['source_url'] = url_base + s
    soup = BeautifulSoup(scraperwiki.scrape(url_base + s))
    c = soup.find('div', id='content')
    td = c.findAll('table')[0].findAll('td')
    email = False
    offices = []

    if council:
        record['elected_office'] = 'Councillor'
        photo_url = c.find('img', 'bio_pic')['src']
        # Meta description also has representative and district names, but in once case it is incorrect.
        record['name'] = soup.find('span', {'class': 'bg90B'}).text.replace('Councillor', '').strip()
        record['district_name'] = soup.find('span', {'class': 'bg100B'}).text.replace(' Ward', '').strip()
        qs = urlparse(td[7].find('a')['href']).query
        qs = parse_qs(qs)
        rec = qs.get('Recipient', None)
        if len(rec):
            email = rec[0] + '@winnipeg.ca'
        postal = td[1]
        tel = td[3].text
        fax = td[5].text
    else:
        record['elected_office'] = 'Mayor'
        record['boundary_url'] = '/boundaries/census-subdivisions/4611040/'
        lm = soup.find('div', id='left-menu')
        l = lm.findAll('div', 'section')[1]
        photo_url = l.find('img')['src']
        record['name'] = l.find('a').text.replace('Mayor ', '').strip()
        email = 'mayor@winnipeg.ca'
        postal = td[5]
        tel = ''
        fax = td[1].text
        mayor_page = BeautifulSoup(scraperwiki.scrape(url_base + '/interhom/mayor/'))
        record['name'] = mayor_page.find('img',src="/interhom/Mayor/images/signature.jpg")['alt']


    postal =  '\n'.join([x.strip() for x in postal.findAll(text=True)])
    offices = []
    offices.append({
        'type': 'constituency',
        'tel': tel,
        'fax': fax,
        'postal': postal
    })
    record['offices'] = json.dumps(offices)
    record['photo_url'] = url_base + photo_url
    if email:
        record['email'] = email
    return record
           
if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')
scraperwiki.sqlite.commit();
url_base = 'http://winnipeg.ca'
soup = BeautifulSoup(scraperwiki.scrape(url_base + '/council/'))

m = soup.find('div', id='content')
t = m.findAll('table')[1]
members = t.findAll('a')

for a in members:
    r = scrape_member(url_base, a['href'])
    scraperwiki.sqlite.save(['name'], r)