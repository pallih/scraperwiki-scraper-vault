#Work in progress

import scraperwiki,re
from BeautifulSoup import BeautifulSoup

url = 'http://www.vedur.is/skjalftar-og-eldgos/jardskjalftar'

def extract(text, sub1, sub2):
    """extract a substring between two substrings sub1 and sub2 in text"""
    return text.split(sub1)[-1].split(sub2)[0]

html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)
soup.prettify()

quakes = extract(html, "VI.quakeInfo = [","]")

#print quakes.split('}')

test = re.findall('{(.*?)}', quakes)

for t in test:
    print t
    time = re.findall('Date\((\d.+)\)',t)
    print time[0]
    lat = re.findall('lat\':\'(\d.*?)\'',t)
    print lat[0]
    lon = re.findall('lon\':\'(-\d.*?)\'',t)
    print lon[0]
    size = re.findall('s\':\'(.*?)\'',t)
    print size[0]
    depth = re.findall('dep\':\'(.*?)\'',t)
    print depth[0]
    quality = re.findall('q\':\'(\d.*?)\'',t)
    print quality[0]
    distanceL = re.findall('dL\':\'(\d.*?)\'',t)
    print distanceL[0]
    distanceD = re.findall('dD\':\'(.*?)\'',t)
    print distanceD[0]
    distanceR = re.findall('dR\':\'(.*?)\'',t)
    print distanceR[0]

#print quakes


#Work in progress

import scraperwiki,re
from BeautifulSoup import BeautifulSoup

url = 'http://www.vedur.is/skjalftar-og-eldgos/jardskjalftar'

def extract(text, sub1, sub2):
    """extract a substring between two substrings sub1 and sub2 in text"""
    return text.split(sub1)[-1].split(sub2)[0]

html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)
soup.prettify()

quakes = extract(html, "VI.quakeInfo = [","]")

#print quakes.split('}')

test = re.findall('{(.*?)}', quakes)

for t in test:
    print t
    time = re.findall('Date\((\d.+)\)',t)
    print time[0]
    lat = re.findall('lat\':\'(\d.*?)\'',t)
    print lat[0]
    lon = re.findall('lon\':\'(-\d.*?)\'',t)
    print lon[0]
    size = re.findall('s\':\'(.*?)\'',t)
    print size[0]
    depth = re.findall('dep\':\'(.*?)\'',t)
    print depth[0]
    quality = re.findall('q\':\'(\d.*?)\'',t)
    print quality[0]
    distanceL = re.findall('dL\':\'(\d.*?)\'',t)
    print distanceL[0]
    distanceD = re.findall('dD\':\'(.*?)\'',t)
    print distanceD[0]
    distanceR = re.findall('dR\':\'(.*?)\'',t)
    print distanceR[0]

#print quakes


