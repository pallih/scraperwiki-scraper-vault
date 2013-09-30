import scraperwiki
import requests 
import BeautifulSoup
import time
import re



def info(url):
    response = requests.get(url, verify = False).text
    linkSoup  = BeautifulSoup.BeautifulSoup(response)
    detailLinks = linkSoup.findAll('a', {'class' : 'DetailLink'})

    for i in range(len(detailLinks)):
        detailLink = detailLinks[i]['href']
        url=url = "http://www.bbfc.de" + detailLink
        response = requests.get(url, verify = False).text
        detailSoup  = BeautifulSoup.BeautifulSoup(response)
        
        internet = None
        phone = None
        email = None
        address = None
        location = None
        ort = None

        #addressM = detailSoup.findAll('div', {'class' : 'AddressMain'})[0]
        
        #if re.search('div class="Address"',str(addressM)):
        #    address = detailSoup.findAll('div', {'class' : 'Address'})[0].string
        
        #if re.search('Location',str(addressM)):
        #    l = detailSoup.findAll('div', {'class' : 'Location'})[0].string 
        #    if l != None:
        #        locSoup = bss(l, convertEntities = bss.HTML_ENTITIES)
        #        location = locSoup.contents[0]

        info = detailSoup.findAll('div', {'class' : 'Info'})[0]
        
        #infoSoup  = BeautifulSoup.BeautifulSoup(infoText)
        infoText= info.findAll(text = True)[1]
                
        addressInfo = detailSoup.findAll('div', {'class' : 'Entry'})
        #print len(addressInfo[0])
        contactDict = {}
        labels = addressInfo[0].findAll('div', {'class' : 'Label'})[0:len(addressInfo[0])]
        values = addressInfo[0].findAll('div', {'class' : 'Value'})#[j].findAll(text = True)[0]
        #print labels
        #print contactDict
        
        for j in range(len(labels)):
            contactDict[labels[j].findAll(text = True)[0]] = values[j].findAll(text = True)[0]
        #print contactDict
        
        if contactDict.has_key('Internet:'):
            internet = contactDict['Internet:']

        if contactDict.has_key('Telefon:'):
            phone = contactDict['Telefon:']

        #if contactDict.has_key('Ort:'):
        #    o = contactDict['Ort:']
        #    bss = BeautifulSoup.BeautifulStoneSoup
        #    nameSoup = bss(o, convertEntities = bss.HTML_ENTITIES)
        #    ort = nameSoup.contents[0]
           

        if contactDict.has_key(u'Stra\xdfe *:'):
            a = contactDict[u'Stra\xdfe *:']
            
            bss = BeautifulSoup.BeautifulStoneSoup
            nameSoup = bss(a, convertEntities = bss.HTML_ENTITIES)
            address = nameSoup.contents[0]
            
        
        data = {'address': address,
            
            'infoText':infoText,
            'categoryName':categoryName,
            'internet' : internet,
            'phone' : phone,
            'bbfcUrl' : url
            }
        scraperwiki.sqlite.save(unique_keys=['bbfcUrl'], data=data)
        
        
    return  



url = "http://www.bbfc.de/WebObjects/Medienboard.woa/wa/MBdba/1011320,bbfcloc,overview,de,cat=,term=,epoch=,cstyle="
response = requests.get(url, verify = False).text
soup = BeautifulSoup.BeautifulSoup(response)

categories = str(soup.findAll('div', attrs = {'class':'Entry'}))

categorySoup = BeautifulSoup.BeautifulSoup(categories)

aTags = categorySoup.findAll('a')#, attrs = {'href':url})
iter = len(aTags)

for j in range(iter):
    category = aTags[j]
    categoryLink = category['href']
    categoryName = category.string
    url = "http://www.bbfc.de" + categoryLink
    response = requests.get(url, verify = False).text
    linkSoup  = BeautifulSoup.BeautifulSoup(response)
    hitcountString = linkSoup.findAll('div', {'class' : 'Hitcount'})[0].string
    hitcount = hitcountString.partition(" ")[0]
    
    
    if int(hitcount) > 10:
        batch = linkSoup.findAll('div', {'class' : 'Batch'})
        for k in range(len(batch)):
            batchUrl = "http://www.bbfc.de" + categoryLink + ",_batch=" + str(k)
            info(batchUrl)
            
    else:
        url = "http://www.bbfc.de" + categoryLink
        info(url)
        
    time.sleep(5)

import scraperwiki
import requests 
import BeautifulSoup
import time
import re



def info(url):
    response = requests.get(url, verify = False).text
    linkSoup  = BeautifulSoup.BeautifulSoup(response)
    detailLinks = linkSoup.findAll('a', {'class' : 'DetailLink'})

    for i in range(len(detailLinks)):
        detailLink = detailLinks[i]['href']
        url=url = "http://www.bbfc.de" + detailLink
        response = requests.get(url, verify = False).text
        detailSoup  = BeautifulSoup.BeautifulSoup(response)
        
        internet = None
        phone = None
        email = None
        address = None
        location = None
        ort = None

        #addressM = detailSoup.findAll('div', {'class' : 'AddressMain'})[0]
        
        #if re.search('div class="Address"',str(addressM)):
        #    address = detailSoup.findAll('div', {'class' : 'Address'})[0].string
        
        #if re.search('Location',str(addressM)):
        #    l = detailSoup.findAll('div', {'class' : 'Location'})[0].string 
        #    if l != None:
        #        locSoup = bss(l, convertEntities = bss.HTML_ENTITIES)
        #        location = locSoup.contents[0]

        info = detailSoup.findAll('div', {'class' : 'Info'})[0]
        
        #infoSoup  = BeautifulSoup.BeautifulSoup(infoText)
        infoText= info.findAll(text = True)[1]
                
        addressInfo = detailSoup.findAll('div', {'class' : 'Entry'})
        #print len(addressInfo[0])
        contactDict = {}
        labels = addressInfo[0].findAll('div', {'class' : 'Label'})[0:len(addressInfo[0])]
        values = addressInfo[0].findAll('div', {'class' : 'Value'})#[j].findAll(text = True)[0]
        #print labels
        #print contactDict
        
        for j in range(len(labels)):
            contactDict[labels[j].findAll(text = True)[0]] = values[j].findAll(text = True)[0]
        #print contactDict
        
        if contactDict.has_key('Internet:'):
            internet = contactDict['Internet:']

        if contactDict.has_key('Telefon:'):
            phone = contactDict['Telefon:']

        #if contactDict.has_key('Ort:'):
        #    o = contactDict['Ort:']
        #    bss = BeautifulSoup.BeautifulStoneSoup
        #    nameSoup = bss(o, convertEntities = bss.HTML_ENTITIES)
        #    ort = nameSoup.contents[0]
           

        if contactDict.has_key(u'Stra\xdfe *:'):
            a = contactDict[u'Stra\xdfe *:']
            
            bss = BeautifulSoup.BeautifulStoneSoup
            nameSoup = bss(a, convertEntities = bss.HTML_ENTITIES)
            address = nameSoup.contents[0]
            
        
        data = {'address': address,
            
            'infoText':infoText,
            'categoryName':categoryName,
            'internet' : internet,
            'phone' : phone,
            'bbfcUrl' : url
            }
        scraperwiki.sqlite.save(unique_keys=['bbfcUrl'], data=data)
        
        
    return  



url = "http://www.bbfc.de/WebObjects/Medienboard.woa/wa/MBdba/1011320,bbfcloc,overview,de,cat=,term=,epoch=,cstyle="
response = requests.get(url, verify = False).text
soup = BeautifulSoup.BeautifulSoup(response)

categories = str(soup.findAll('div', attrs = {'class':'Entry'}))

categorySoup = BeautifulSoup.BeautifulSoup(categories)

aTags = categorySoup.findAll('a')#, attrs = {'href':url})
iter = len(aTags)

for j in range(iter):
    category = aTags[j]
    categoryLink = category['href']
    categoryName = category.string
    url = "http://www.bbfc.de" + categoryLink
    response = requests.get(url, verify = False).text
    linkSoup  = BeautifulSoup.BeautifulSoup(response)
    hitcountString = linkSoup.findAll('div', {'class' : 'Hitcount'})[0].string
    hitcount = hitcountString.partition(" ")[0]
    
    
    if int(hitcount) > 10:
        batch = linkSoup.findAll('div', {'class' : 'Batch'})
        for k in range(len(batch)):
            batchUrl = "http://www.bbfc.de" + categoryLink + ",_batch=" + str(k)
            info(batchUrl)
            
    else:
        url = "http://www.bbfc.de" + categoryLink
        info(url)
        
    time.sleep(5)

