from urlparse import urljoin
import scraperwiki
from bs4 import BeautifulSoup
import re

scraperwiki.sqlite.execute('DROP TABLE `swdata`')

url = "http://www.markham.ca/wps/portal/Markham/MunicipalGovernment/MayorAndCouncil/RegionalAndWardCouncillors/!ut/p/c5/04_SB8K8xLLM9MSSzPy8xBz9CP0os3gTf3dnZ58wi0CjIBMDA09PlzBTP5dAw9BAQ_2CbEdFANQHEzg!/"
soup = BeautifulSoup(scraperwiki.scrape(url))

def getCleanTxt(field):
    return field.get_text().strip()

fields = soup.findAll(width="25%")
for td in fields:
    text = getCleanTxt(td)
    if not text:
        # Empty record, so we ignore it
        continue
    
    position=td.find('strong')
    positionCheck=getCleanTxt(td.find('strong'))
    # find email for each councillors
    link=urljoin(url , position.parent.get('href'))
    email_soup = BeautifulSoup(scraperwiki.scrape(link))
    email_find= email_soup.find(text=re.compile('E-mail:'))
    email=email_find.next_sibling.next_sibling
    if not email:
        #skip if email website structure differs
        email=""
    else:
        email=email.get_text()
    print email

    if (positionCheck =="Deputy Mayor") or (positionCheck =="Regional Councillor"):
        record = {
            'position': getCleanTxt(td.find('strong')),
            'name': getCleanTxt(td.findAll('strong')[1]),
            'img_link': urljoin(url, td.find('img')['src']),
            'district_name': 'Markham, ON',
            'email': email,
        }
        print record
        scraperwiki.sqlite.save([], record)
        print '----'
    else:
    # Entries for district specific councillors
        record = {
            'position': 'Councillor',
            'district_id': getCleanTxt(td.find('strong')).split("Councillor")[0],
            'name': getCleanTxt(td.findAll('strong')[1]),
            'img_link': urljoin(url, td.find('img')['src']),
            'district_name': 'Markham, ON',
            'email': email,
        }
        print record
        scraperwiki.sqlite.save([], record)
        print '----'
