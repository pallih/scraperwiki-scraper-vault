import httplib2
import urllib2,sys
import re
import scraperwiki
from BeautifulSoup import BeautifulSoup, SoupStrainer
from BeautifulSoup import NavigableString

#start at this address - load it
#address = "http://www.videoload.de/c/65/82/97/6582974"
#soup = BeautifulSoup(urllib2.urlopen(address))

#get all of the anchors and loop through them

#scraperwiki.sqlite.execute("create table swdata ('page', 'domain', 'src', 'text', 'title', 'class', 'id', 'href', 'film', 'genre', 'price', 'priceSD', 'priceHD', 'releaseYear', 'origCountry', 'rating', 'actors', 'actresses')")

def loopLinks(siteURL):
    #were links loaded from this site? if not - load them
    print siteURL
    rs = scraperwiki.sqlite.select("count(*) as freq from swdata where src=?", siteURL)
    print " - " + "check freq"
    for d in rs:
        print " - " + str(d["freq"])
        if d["freq"]==0:
            soup = BeautifulSoup(urllib2.urlopen(siteURL))    
            aDomain = siteURL.replace("http://","")
            aDomain = aDomain.replace("https://","")
            aDomain = aDomain[:aDomain.find('/')]
            print " - find all anchors"
            for tag in soup.findAll('a'):
                print "ANCHOR: " + tag.get('href')
                linkURL = str(tag.get('href'))
                addLink = "true"
                print " - " + addLink + ' (starting out)'                
                #get absolute link
                if linkURL.find('/')==0: 
                   linkURL = 'http://' + aDomain + linkURL 
                else:
                    if linkURL.find('http://' + aDomain + '/')!= 0:
                        addLink = "false"
                print " - final link: " + linkURL
                print " - Orig Domain: " + origDomain
                print " - " + addLink + ' (same domain)'                
                #ensure this is not the site url / home link

                if linkURL == siteURL: addLink = "false"
                print " - " + addLink + ' (link to src page)'
                if linkURL == 'http://' + origDomain + '/': addLink = "false"
                print " - " + addLink + ' (home link)'                
                #ensure link has not already been loaded
                rs = scraperwiki.sqlite.select("count(*) as freq from swdata where href=?", linkURL)
                for d in rs:
                    if d["freq"]>0: addLink = "false"
                print " - " + addLink + ' (already loaded)'
                #load or not?
                print " - Final result for " + linkURL + ' = ' + addLink
                if addLink!="false":
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
                    print 'Loop to ' + linkURL
                    loopLinks(linkURL)
            
mainURL = "http://www.videoload.de/c/65/82/97/6582974"
mainURL = "http://mesfilmsbelgacomtv.skynet.be/fr/iDiscover/Genres.html"
origDomain = mainURL.replace("http://","")
origDomain = origDomain.replace("https://","")
origDomain = origDomain[:origDomain.find('/')]
loopLinks(mainURL)
