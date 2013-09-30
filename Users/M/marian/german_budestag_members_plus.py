import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

html = scraperwiki.scrape('http://www.bundestag.de/bundestag/abgeordnete17/alphabet/index.html')
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

    person['URL'] = "http://www.bundestag.de/bundestag/abgeordnete17" + url

    person['Comment'] = ''
    if re.search('\+', lastpart) is not None:
        person['Comment'] = 'DECEASED'
    elif re.search('\*', lastpart) is not None:
        person['Comment'] = 'RESIGNED'

    
    scraperwiki.datastore.save(['URL'], person)


import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

html = scraperwiki.scrape('http://www.bundestag.de/bundestag/abgeordnete17/alphabet/index.html')
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

    person['URL'] = "http://www.bundestag.de/bundestag/abgeordnete17" + url

    person['Comment'] = ''
    if re.search('\+', lastpart) is not None:
        person['Comment'] = 'DECEASED'
    elif re.search('\*', lastpart) is not None:
        person['Comment'] = 'RESIGNED'

    
    scraperwiki.datastore.save(['URL'], person)


import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

html = scraperwiki.scrape('http://www.bundestag.de/bundestag/abgeordnete17/alphabet/index.html')
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

    person['URL'] = "http://www.bundestag.de/bundestag/abgeordnete17" + url

    person['Comment'] = ''
    if re.search('\+', lastpart) is not None:
        person['Comment'] = 'DECEASED'
    elif re.search('\*', lastpart) is not None:
        person['Comment'] = 'RESIGNED'

    
    scraperwiki.datastore.save(['URL'], person)


import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

html = scraperwiki.scrape('http://www.bundestag.de/bundestag/abgeordnete17/alphabet/index.html')
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

    person['URL'] = "http://www.bundestag.de/bundestag/abgeordnete17" + url

    person['Comment'] = ''
    if re.search('\+', lastpart) is not None:
        person['Comment'] = 'DECEASED'
    elif re.search('\*', lastpart) is not None:
        person['Comment'] = 'RESIGNED'

    
    scraperwiki.datastore.save(['URL'], person)


