import scraperwiki
import requests
import BeautifulSoup
import time
import re


def clean(data):     
    p = re.compile('//')     
    return p.sub('', data)

def cleanKoord(data):     
    p = re.compile('(Koordinaten fehlen! Hilf mit.)')     
    return p.sub('', data)

def cleanStandort(data):     
    p = re.compile('(Standort)')     
    return p.sub('', data)

def cleanBr(data):     
    p = re.compile('()')     
    return p.sub('', data)


url = "http://de.wikipedia.org/wiki/Liste_der_Baudenkm%C3%A4ler_in_W%C3%BCrzburg-Altstadt"
response = requests.get(url, verify = False).text
soup = BeautifulSoup.BeautifulSoup(response)

infoSoup = BeautifulSoup.BeautifulSoup(response)
  
infoTags = infoSoup.findAll('table')
for i in range(1,len(infoTags)):
    letter = infoTags[i].findAll('td')
    
    for j in range(len(letter)/5):
        lage = letter[0::5][j]
        lat = None
        lng = None
        imageUrl = None
        linkSoup = BeautifulSoup.BeautifulSoup(str(lage))
        lage = lage.text
        lage = cleanKoord(lage)
        lage = cleanStandort(lage)
        lage = cleanBr(lage)
        
        if len(linkSoup.findAll('small')) > 0:
            if  linkSoup.findAll('small')[0].text == "(Standort)":
       
                coordUrl = 'http:' + linkSoup.findAll('a')[0]['href']
                resp = requests.get(coordUrl, verify = False).text
                coordSoup = BeautifulSoup.BeautifulSoup(resp)
                lat = coordSoup.findAll('span', {'class':'latitude'})[0].text
                lng = coordSoup.findAll('span', {'class':'longitude'})[0].text
            
        objekt = letter[1::5][j].text
       
        description = letter[2::5][j].text
        
        id =letter[3::5][j].text
        
        image = letter[4::5][j]

        imageSoup = BeautifulSoup.BeautifulSoup(str(letter[4::5][j].findAll('a')))
        
        if imageSoup.text == '[BW]':
            imageUrl = None
           
        elif imageSoup.text == '[,weitere Bilder]':
            imageUrl = None

        elif len(imageSoup)== 1: 
             imageUrl = None
        
        else:
             imageUrl = imageSoup.findAll('img')[0]['src']
             

        data = {'lage' : lage,
                'lat' : lat,
                'lng' : lng,
                'object' : objekt,
                'id' : id,
                'imageUrl' : imageUrl}
        scraperwiki.sqlite.save(unique_keys=['id'], data=data) 
import scraperwiki
import requests
import BeautifulSoup
import time
import re


def clean(data):     
    p = re.compile('//')     
    return p.sub('', data)

def cleanKoord(data):     
    p = re.compile('(Koordinaten fehlen! Hilf mit.)')     
    return p.sub('', data)

def cleanStandort(data):     
    p = re.compile('(Standort)')     
    return p.sub('', data)

def cleanBr(data):     
    p = re.compile('()')     
    return p.sub('', data)


url = "http://de.wikipedia.org/wiki/Liste_der_Baudenkm%C3%A4ler_in_W%C3%BCrzburg-Altstadt"
response = requests.get(url, verify = False).text
soup = BeautifulSoup.BeautifulSoup(response)

infoSoup = BeautifulSoup.BeautifulSoup(response)
  
infoTags = infoSoup.findAll('table')
for i in range(1,len(infoTags)):
    letter = infoTags[i].findAll('td')
    
    for j in range(len(letter)/5):
        lage = letter[0::5][j]
        lat = None
        lng = None
        imageUrl = None
        linkSoup = BeautifulSoup.BeautifulSoup(str(lage))
        lage = lage.text
        lage = cleanKoord(lage)
        lage = cleanStandort(lage)
        lage = cleanBr(lage)
        
        if len(linkSoup.findAll('small')) > 0:
            if  linkSoup.findAll('small')[0].text == "(Standort)":
       
                coordUrl = 'http:' + linkSoup.findAll('a')[0]['href']
                resp = requests.get(coordUrl, verify = False).text
                coordSoup = BeautifulSoup.BeautifulSoup(resp)
                lat = coordSoup.findAll('span', {'class':'latitude'})[0].text
                lng = coordSoup.findAll('span', {'class':'longitude'})[0].text
            
        objekt = letter[1::5][j].text
       
        description = letter[2::5][j].text
        
        id =letter[3::5][j].text
        
        image = letter[4::5][j]

        imageSoup = BeautifulSoup.BeautifulSoup(str(letter[4::5][j].findAll('a')))
        
        if imageSoup.text == '[BW]':
            imageUrl = None
           
        elif imageSoup.text == '[,weitere Bilder]':
            imageUrl = None

        elif len(imageSoup)== 1: 
             imageUrl = None
        
        else:
             imageUrl = imageSoup.findAll('img')[0]['src']
             

        data = {'lage' : lage,
                'lat' : lat,
                'lng' : lng,
                'object' : objekt,
                'id' : id,
                'imageUrl' : imageUrl}
        scraperwiki.sqlite.save(unique_keys=['id'], data=data) 
