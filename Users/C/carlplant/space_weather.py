#simple scraper to measure NOAA space weather forecasts

import scraperwiki #import libraries to work with
from BeautifulSoup import BeautifulSoup #more details can be found here http://www.crummy.com/software/BeautifulSoup/bs3/documentation.html#Parsing a Document
import re
import datetime

try:
    scraperwiki.sqlite.execute("""
        create table geostorm
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)
except:
    print "Table probably already exists."

html = scraperwiki.scrape("http://www.spaceweather.com/") #the webpage we will be scraping
soup = BeautifulSoup(html)

#print soup.prettify() #print the results of soup


flare = soup.findAll(attrs={"class" : "solarFlaresTableDatumText"})
fTextM = flare[0].text
#print fTextM
splitM = re.split('\%',fTextM)
record = {}
record['flareClassM'] = splitM[0]
fTextX = flare[2].text
#print fTextX
splitX = re.split('\%',fTextX)
record['flareClassX'] = splitX[0]
geoactive = flare[4].text
splitgeoA = re.split('\%',geoactive)
record['MLgeoStormActive'] = splitgeoA[0]
geominor = flare[6].text
#print geominor
splitgeoM = re.split('\%',geominor)
record['MLgeoStormMinor'] = splitgeoM[0]
geosevere = flare[8].text
print geosevere
splitgeoS = re.split('\%',geosevere)
record['MLgeoStormSevere'] = splitgeoS[0]


record['timeOfScrape'] = datetime.date.today()

scraperwiki.sqlite.save(unique_keys=[],data=record, table_name='geostorm')