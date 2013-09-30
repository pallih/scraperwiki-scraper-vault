# -*- coding: utf-8 -*-
import scraperwiki
import requests
import urllib2
import BeautifulSoup 
import re


url = 'http://www.liegenschaftsfonds-berlin.de/site/index.php?id=98&no_cache=1'


response = requests.get(url, verify = False).text

soup = BeautifulSoup.BeautifulSoup(response)
descAll = soup.findAll('td', attrs = {'class':'normal_text'})

t =descAll[1]
f =t.findAll(text = True)

beb = f[35::32]
bez = f[30::32]
nutz = f[33::32]
adr = f[28::32]

bss = BeautifulSoup.BeautifulStoneSoup



linkList = []
addressList = []
aTags = soup.findAll('a')[1::2]

for i in range(len(aTags)):
    if aTags[i].has_key('href'):
        url =  aTags[i]['href']
        
        if re.search('id=50',url):
            
            link = url
            
            linkList.append(link)
            
            
for i in range(1,len(nutz)):

    nSoup = bss(nutz[i], convertEntities = bss.HTML_ENTITIES)
    nutzung = nSoup.contents[0]
        
    bSoup = bss(bez[i], convertEntities = bss.HTML_ENTITIES)
    bezirk = bSoup.contents[0]
        
    beSoup = bss(beb[i], convertEntities = bss.HTML_ENTITIES)
    bebaung = beSoup.contents[0]

    aSoup = bss(adr[i], convertEntities = bss.HTML_ENTITIES)
    adresse = aSoup.contents[0]
    
    data = {'id': i,
            'nutzung':nutzung,
            'bebauung':bebaung,
            'link':"http://www.liegenschaftsfonds-berlin.de" + linkList[i-1],
            'addresse':adresse,
            'bezirk': bezirk
            }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data) 

# -*- coding: utf-8 -*-
import scraperwiki
import requests
import urllib2
import BeautifulSoup 
import re


url = 'http://www.liegenschaftsfonds-berlin.de/site/index.php?id=98&no_cache=1'


response = requests.get(url, verify = False).text

soup = BeautifulSoup.BeautifulSoup(response)
descAll = soup.findAll('td', attrs = {'class':'normal_text'})

t =descAll[1]
f =t.findAll(text = True)

beb = f[35::32]
bez = f[30::32]
nutz = f[33::32]
adr = f[28::32]

bss = BeautifulSoup.BeautifulStoneSoup



linkList = []
addressList = []
aTags = soup.findAll('a')[1::2]

for i in range(len(aTags)):
    if aTags[i].has_key('href'):
        url =  aTags[i]['href']
        
        if re.search('id=50',url):
            
            link = url
            
            linkList.append(link)
            
            
for i in range(1,len(nutz)):

    nSoup = bss(nutz[i], convertEntities = bss.HTML_ENTITIES)
    nutzung = nSoup.contents[0]
        
    bSoup = bss(bez[i], convertEntities = bss.HTML_ENTITIES)
    bezirk = bSoup.contents[0]
        
    beSoup = bss(beb[i], convertEntities = bss.HTML_ENTITIES)
    bebaung = beSoup.contents[0]

    aSoup = bss(adr[i], convertEntities = bss.HTML_ENTITIES)
    adresse = aSoup.contents[0]
    
    data = {'id': i,
            'nutzung':nutzung,
            'bebauung':bebaung,
            'link':"http://www.liegenschaftsfonds-berlin.de" + linkList[i-1],
            'addresse':adresse,
            'bezirk': bezirk
            }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data) 

