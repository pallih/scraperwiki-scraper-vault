#############
#List of all street names in Iceland the postcode for the street and place (municipiality). Combines two datasets from the Iceland Post Authorities
##############

import scraperwiki,re
from BeautifulSoup import BeautifulSoup


#This is a list of postcodes and their place (i.e: 101 = Reykjavik)
html = scraperwiki.scrape('http://www.postur.is/gogn/Gotuskra/postnumer.txt')
soup = BeautifulSoup(html)
lines = soup.string.split('\r')
stadir = {}

for line in lines[1:-1]:
        #line = str(line)
        values = line.split(';')
        stadir [re.sub('\n','',values[0])] = values[1]
        
#List of all street names and their postcode
html = scraperwiki.scrape('http://www.postur.is/gogn/Gotuskra/gotuskra.txt')
soup = BeautifulSoup(html)
lines = soup.string.split('\r')

#Lets combine the two so we end up with a list that includes: postcode (pnr), street name(gata_nf & gata_thgf) and place name (stadur)
for line in lines[1:-1]:
        data = {}
        values = line.split(';')
        data['pnr'] = values[1]
        data['gata_nf'] = values[2]
        data['gata_thgf'] = values[3]
        data ['stadur'] = stadir[values[1]]
        print data
        #scraperwiki.datastore.save(["pnr","gata_nf"], data)

print '************ ALL DONE ***********'#############
#List of all street names in Iceland the postcode for the street and place (municipiality). Combines two datasets from the Iceland Post Authorities
##############

import scraperwiki,re
from BeautifulSoup import BeautifulSoup


#This is a list of postcodes and their place (i.e: 101 = Reykjavik)
html = scraperwiki.scrape('http://www.postur.is/gogn/Gotuskra/postnumer.txt')
soup = BeautifulSoup(html)
lines = soup.string.split('\r')
stadir = {}

for line in lines[1:-1]:
        #line = str(line)
        values = line.split(';')
        stadir [re.sub('\n','',values[0])] = values[1]
        
#List of all street names and their postcode
html = scraperwiki.scrape('http://www.postur.is/gogn/Gotuskra/gotuskra.txt')
soup = BeautifulSoup(html)
lines = soup.string.split('\r')

#Lets combine the two so we end up with a list that includes: postcode (pnr), street name(gata_nf & gata_thgf) and place name (stadur)
for line in lines[1:-1]:
        data = {}
        values = line.split(';')
        data['pnr'] = values[1]
        data['gata_nf'] = values[2]
        data['gata_thgf'] = values[3]
        data ['stadur'] = stadir[values[1]]
        print data
        #scraperwiki.datastore.save(["pnr","gata_nf"], data)

print '************ ALL DONE ***********'