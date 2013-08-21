# Blank Python
from BeautifulSoup import BeautifulSoup as bs
import urllib2, re
from string import ascii_uppercase
from time import sleep
import scraperwiki
# "De heer et Madame Van Hullebusch"

def parseName(namestr):
    
    p = re.compile('De heer|Professor|Professor Dr.|Mevrouw|Baron|S.E.M.|Graaf|Burggraaf|Dokter|Jonkheer|Dr.|Mister|Jufrouw|Burggravin|SAS|Ridder|Gravin|Prince|SAS Prince|Ridder|Minister van Staat|Marquies|Stafhouder')
    m = p.match(namestr)
    if m: 
        return namestr[m.end():]
    else:
        return namestr

def parse(letter):
    url = '/'.join(['http://www.cercledelorraine.be/nl/lijst-van-de-leden', letter])
    html = urllib2.urlopen(url).read()
    soup = bs(html)
    datatable = soup.find('table', width='300')
    results = []
    for record in datatable.findAll('tr'):
        person = {}
        lines = record.td.findNextSibling('td').findAll('div')

        person['member_of'] = 'Cercle de Lorraine'
        person['namestr'] = lines[0].text.replace('&nbsp;', ' ')
        person['position'] = lines[1].text.replace('&nbsp;', ' ')
        person['organisation'] = lines[2].text.replace('&nbsp;', ' ')
        person['name'] = parseName(person['namestr'])

        results.append(person)

    return(results)

for letter in ascii_uppercase:
    for record in parse(letter):
         scraperwiki.sqlite.save(['namestr'], record)
    sleep(0.5)

