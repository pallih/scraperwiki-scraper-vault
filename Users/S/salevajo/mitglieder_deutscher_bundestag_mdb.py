import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

baseurl = 'http://www.bundestag.de/bundestag/abgeordnete17'
html = scraperwiki.scrape(baseurl+'/alphabet/index.html')
#print html

soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
rows = soup.findAll(attrs={'class': 'linkIntern'})
#print rows

def normalise_party(s):
    """delete trailing punctuation from party string"""
    s = re.sub('[\.\*\)\+]+$', '', s)
    return s

for row in rows:
    person = {}
    details = row.text

    spl = details.split(",")
    
    lastpart = spl[2]

    person['LastName'] = spl[0].strip()
    person['FirstName'] = spl[1].strip()
    person['Party'] = normalise_party(spl[2].strip())

    url = row.a['href'].replace("..", "")

    person['URL'] = baseurl + url

    person['Comment'] = ''
    if re.search('\+', lastpart) is not None:
        person['Comment'] = 'DECEASED'
    elif re.search('\*', lastpart) is not None:
        person['Comment'] = 'RESIGNED'

    bio = scraperwiki.scrape(person['URL'])
    biosoup = BeautifulSoup(bio)

    imagedivs = biosoup.findAll(attrs={'class': 'bildDivPortrait'})
    if (len(imagedivs) > 0):
        image = imagedivs[0].findAll('img')
        if (len(image) > 0):
            person['Portrait'] = baseurl + image[0]['src'].replace("../..", "")
    
    scraperwiki.sqlite.save(['URL'], person)

