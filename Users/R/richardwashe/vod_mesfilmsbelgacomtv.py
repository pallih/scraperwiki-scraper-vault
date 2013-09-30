import httplib2
from urllib2 import Request, urlopen, URLError, HTTPError
import re
import scraperwiki
from BeautifulSoup import BeautifulSoup, SoupStrainer
from BeautifulSoup import NavigableString

#start at this address - load it
#address = "http://www.videoload.de/c/65/82/97/6582974"
#soup = BeautifulSoup(urllib2.urlopen(address))

#get all of the anchors and loop through them

scraperwiki.sqlite.execute("drop table swdata")
scraperwiki.sqlite.execute("create table swdata ('page', 'domain', 'src', 'text', 'title', 'class', 'id', 'href', 'film', 'genre', 'price', 'priceSD', 'priceHD', 'releaseYear', 'origCountry', 'rating', 'actors', 'actresses')")

def loopLinks(siteURL):
    #were links loaded from this site? if not - load them

    siteURL.replace("\r","")
    siteURL.replace("\n","")
    siteURL.strip()
    
    rs = scraperwiki.sqlite.select("count(*) as freq from swdata where src=?", siteURL)

    for d in rs:

        if d["freq"]==0:
            req = Request(siteURL)
            try:
                soup = BeautifulSoup(urlopen(req))    
            except HTTPError, e:
                print 'The server could n0t fulfill the request.'
                print 'Error code: ', e.code
            except URLError, e:
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            else:
                aDomain = siteURL.replace("http://","")
                aDomain = aDomain.replace("https://","")
                aDomain = aDomain[:aDomain.find('/')]
    
                for tag in soup.findAll('a'):
    
                    linkURL = str(tag.get('href'))
                    addLink = "true"
    
                    #get absolute link
                    if linkURL.find('/')==0:
                       linkURL = 'http://' + aDomain + linkURL
                    else:
                        if linkURL.find('http://' + aDomain + '/')!= 0:
                            addLink = "false"
                    #ensure this is not the site url / home link
    
                    if linkURL == siteURL: addLink = "false"
    
                    if linkURL == 'http://' + origDomain + '/': addLink = "false"
                    linkURL.replace("\r","")
                    linkURL.replace("\n","")
                    linkURL.strip()
                    #ensure link has not already been loaded
                    rs = scraperwiki.sqlite.select("count(*) as freq from swdata where href=?", linkURL)
                    for d in rs:
                        if d["freq"]>0: addLink = "false"
    
                    if addLink!="false":
                        print linkURL
                        if str(linkURL).find("http://mesfilmsbelgacomtv.skynet.be/fr/films/")==0:
                            print "Film: " + linkURL
                            #get title, year, genre
                            filmReq = Request(linkURL)
                            try:
                                details = BeautifulSoup(urlopen(filmReq))    
                            except HTTPError, e:
                                print 'The server could n0t fulfill the request.'
                                print 'Error code: ', e.code
                            except URLError, e:
                                print 'We failed to reach a server.'
                                print 'Reason: ', e.reason
                            else:
        
                                fYear = str("unknown")
                                print fYear
                                
                                fGenre = str("unknown")
                                print fGenre
        
                                for yr in details.findAll(attrs={'class': 'year'}):
                                    if fYear == "unknown": 
                                        fYear = str(tag.get('class'))
            
                                print str(fYear)
        
                                for gNome in details.findAll(attrs={'id': 'wrapperGenome'}):
                                    for ul in gNome.findAll('ul'):
                                        fndGenre = str("false")
                                        for li in ul.findAll('li'):
                                            if tag.__class__ == NavigableString:            
                                                if fndGenre=="true":
                                                    fGenre = str(fGenre).replace("unknown","") + tag
                                                if tag == "Genres:": 
                                                    fndGenre = str("true")
        
                                print str(tag.get('title')).replace(" - Les films de Belgacom TV","")
                                                
                                data = { 
                                    'page' : details.html.head.title.contents,
                                    'domain' : aDomain,
                                    'src' : siteURL,
                                    'text' : details.NavigableString,
                                    'title' : details.get('title'),
                                    'class' : details.get('class'),
                                    'id' : details.get('id'),
                                    'href' : linkURL,
                                    'film' : str(details.get('title')).replace(" - Les films de Belgacom TV",""),
                                    'genre' : '', 
                                    'price' : '',
                                    'priceSD' : '',
                                    'priceHD' : '',
                                        'releaseYear' : str(fYear),
                                    'origCountry' : '',
                                    'rating' : '',
                                    'actors' : '',
                                    'actresses' : ''
                                }
                                scraperwiki.sqlite.save(unique_keys=['href'], data=data)
        
                        else:
                            print "Not a film: " + linkURL
                            data = {
                                'page' : soup.html.head.title.contents,
                                'domain' : aDomain,
                                'src' : siteURL,
                                'text' : tag.NavigableString,
                                'title' : tag.get('title'),
                                'class' : tag.get('class'),
                                'id' : tag.get('id'),
                                'href' : linkURL,
                                'film' : '',
                                'genre' : '',
                                'price' : '',
                                'priceSD' : '',
                                'priceHD' : '',
                                'releaseYear' : '',
                                'origCountry' : '',
                                'rating' : '',
                                'actors' : '',
                                'actresses' : ''
                            }
                            scraperwiki.sqlite.save(unique_keys=['href'], data=data)
                            if str(linkURL).find("http://mesfilmsbelgacomtv.skynet.be/fr/similar/")!=0:
                                if linkURL!="http://mesfilmsbelgacomtv.skynet.be/fr/":
                                    loopLinks(linkURL)
                
mainURL = "http://www.videoload.de/c/65/82/97/6582974"
mainURL = "http://mesfilmsbelgacomtv.skynet.be/fr/iDiscover/Genres.html"
mainURL = "http://mesfilmsbelgacomtv.skynet.be/fr/search/the%20tree%20of%20life.html"
origDomain = mainURL.replace("http://","")
origDomain = origDomain.replace("https://","")
origDomain = origDomain[:origDomain.find('/')]
loopLinks(mainURL)import httplib2
from urllib2 import Request, urlopen, URLError, HTTPError
import re
import scraperwiki
from BeautifulSoup import BeautifulSoup, SoupStrainer
from BeautifulSoup import NavigableString

#start at this address - load it
#address = "http://www.videoload.de/c/65/82/97/6582974"
#soup = BeautifulSoup(urllib2.urlopen(address))

#get all of the anchors and loop through them

scraperwiki.sqlite.execute("drop table swdata")
scraperwiki.sqlite.execute("create table swdata ('page', 'domain', 'src', 'text', 'title', 'class', 'id', 'href', 'film', 'genre', 'price', 'priceSD', 'priceHD', 'releaseYear', 'origCountry', 'rating', 'actors', 'actresses')")

def loopLinks(siteURL):
    #were links loaded from this site? if not - load them

    siteURL.replace("\r","")
    siteURL.replace("\n","")
    siteURL.strip()
    
    rs = scraperwiki.sqlite.select("count(*) as freq from swdata where src=?", siteURL)

    for d in rs:

        if d["freq"]==0:
            req = Request(siteURL)
            try:
                soup = BeautifulSoup(urlopen(req))    
            except HTTPError, e:
                print 'The server could n0t fulfill the request.'
                print 'Error code: ', e.code
            except URLError, e:
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            else:
                aDomain = siteURL.replace("http://","")
                aDomain = aDomain.replace("https://","")
                aDomain = aDomain[:aDomain.find('/')]
    
                for tag in soup.findAll('a'):
    
                    linkURL = str(tag.get('href'))
                    addLink = "true"
    
                    #get absolute link
                    if linkURL.find('/')==0:
                       linkURL = 'http://' + aDomain + linkURL
                    else:
                        if linkURL.find('http://' + aDomain + '/')!= 0:
                            addLink = "false"
                    #ensure this is not the site url / home link
    
                    if linkURL == siteURL: addLink = "false"
    
                    if linkURL == 'http://' + origDomain + '/': addLink = "false"
                    linkURL.replace("\r","")
                    linkURL.replace("\n","")
                    linkURL.strip()
                    #ensure link has not already been loaded
                    rs = scraperwiki.sqlite.select("count(*) as freq from swdata where href=?", linkURL)
                    for d in rs:
                        if d["freq"]>0: addLink = "false"
    
                    if addLink!="false":
                        print linkURL
                        if str(linkURL).find("http://mesfilmsbelgacomtv.skynet.be/fr/films/")==0:
                            print "Film: " + linkURL
                            #get title, year, genre
                            filmReq = Request(linkURL)
                            try:
                                details = BeautifulSoup(urlopen(filmReq))    
                            except HTTPError, e:
                                print 'The server could n0t fulfill the request.'
                                print 'Error code: ', e.code
                            except URLError, e:
                                print 'We failed to reach a server.'
                                print 'Reason: ', e.reason
                            else:
        
                                fYear = str("unknown")
                                print fYear
                                
                                fGenre = str("unknown")
                                print fGenre
        
                                for yr in details.findAll(attrs={'class': 'year'}):
                                    if fYear == "unknown": 
                                        fYear = str(tag.get('class'))
            
                                print str(fYear)
        
                                for gNome in details.findAll(attrs={'id': 'wrapperGenome'}):
                                    for ul in gNome.findAll('ul'):
                                        fndGenre = str("false")
                                        for li in ul.findAll('li'):
                                            if tag.__class__ == NavigableString:            
                                                if fndGenre=="true":
                                                    fGenre = str(fGenre).replace("unknown","") + tag
                                                if tag == "Genres:": 
                                                    fndGenre = str("true")
        
                                print str(tag.get('title')).replace(" - Les films de Belgacom TV","")
                                                
                                data = { 
                                    'page' : details.html.head.title.contents,
                                    'domain' : aDomain,
                                    'src' : siteURL,
                                    'text' : details.NavigableString,
                                    'title' : details.get('title'),
                                    'class' : details.get('class'),
                                    'id' : details.get('id'),
                                    'href' : linkURL,
                                    'film' : str(details.get('title')).replace(" - Les films de Belgacom TV",""),
                                    'genre' : '', 
                                    'price' : '',
                                    'priceSD' : '',
                                    'priceHD' : '',
                                        'releaseYear' : str(fYear),
                                    'origCountry' : '',
                                    'rating' : '',
                                    'actors' : '',
                                    'actresses' : ''
                                }
                                scraperwiki.sqlite.save(unique_keys=['href'], data=data)
        
                        else:
                            print "Not a film: " + linkURL
                            data = {
                                'page' : soup.html.head.title.contents,
                                'domain' : aDomain,
                                'src' : siteURL,
                                'text' : tag.NavigableString,
                                'title' : tag.get('title'),
                                'class' : tag.get('class'),
                                'id' : tag.get('id'),
                                'href' : linkURL,
                                'film' : '',
                                'genre' : '',
                                'price' : '',
                                'priceSD' : '',
                                'priceHD' : '',
                                'releaseYear' : '',
                                'origCountry' : '',
                                'rating' : '',
                                'actors' : '',
                                'actresses' : ''
                            }
                            scraperwiki.sqlite.save(unique_keys=['href'], data=data)
                            if str(linkURL).find("http://mesfilmsbelgacomtv.skynet.be/fr/similar/")!=0:
                                if linkURL!="http://mesfilmsbelgacomtv.skynet.be/fr/":
                                    loopLinks(linkURL)
                
mainURL = "http://www.videoload.de/c/65/82/97/6582974"
mainURL = "http://mesfilmsbelgacomtv.skynet.be/fr/iDiscover/Genres.html"
mainURL = "http://mesfilmsbelgacomtv.skynet.be/fr/search/the%20tree%20of%20life.html"
origDomain = mainURL.replace("http://","")
origDomain = origDomain.replace("https://","")
origDomain = origDomain[:origDomain.find('/')]
loopLinks(mainURL)