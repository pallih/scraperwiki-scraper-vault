import scraperwiki
import urllib
import re
from bs4 import BeautifulSoup as Soup
import urlparse

base_urllist = "http://evenementen.uitslagen.nl/2013/marathonrotterdam/uitslag0"
end_url = "nl.html"
base_urldata = "http://evenementen.uitslagen.nl/2013/marathonrotterdam/"

for num in range(1023, 1024):
    html = base_urllist+str(num)
    url = html+end_url #dit koppelt de drie elementen van de url aan elkaar
    #page = Soup(urllib.urlopen(url)) #open de pagina

    page = scraperwiki.scrape(url)
    if page is not None:
        endofurl = re.findall("details.php?(.*?)>", page)

#marathon o=1, andere o's staan voor andere afstanden; o=2 is 10km, etc, ontleed de url
#amp; weghalen die in de html van de paginas staat, want die schopt de urls in de war, zie bijv http://evenementen.uitslagen.nl/2013/marathonrotterdam/details.php?s=504&amp;o=1
        
        endofurl = [conv.replace('amp;','') for conv in endofurl]

#tweede basis-url

        base_url = 'http://evenementen.uitslagen.nl/2013/marathonrotterdam/details.php' #de base_url van de loper-url

#loper-url samenstellen uit de base en de resultaten van de scrape
        urlparse.urljoin(base_url, 'details.php?(.*)')

        full_urls = [urlparse.urljoin(base_url, url) for url in endofurl]

#per pagina worden alle urls nu nog in 1 lijst verzameld en dus in 1 cell opgeslagen.
#de volgende regel plaatst elk element in de lijst op een aparte regel

        for elem in full_urls:

            singleurl = elem

            #print singleurl
       
            data = {'url':singleurl}
    
            print data

            scraperwiki.sqlite.save(['url'], data) 

            #de data uit de loper-url halen
        
       import scraperwiki
import urllib
import re
from bs4 import BeautifulSoup as Soup
import urlparse

base_urllist = "http://evenementen.uitslagen.nl/2013/marathonrotterdam/uitslag0"
end_url = "nl.html"
base_urldata = "http://evenementen.uitslagen.nl/2013/marathonrotterdam/"

for num in range(1023, 1024):
    html = base_urllist+str(num)
    url = html+end_url #dit koppelt de drie elementen van de url aan elkaar
    #page = Soup(urllib.urlopen(url)) #open de pagina

    page = scraperwiki.scrape(url)
    if page is not None:
        endofurl = re.findall("details.php?(.*?)>", page)

#marathon o=1, andere o's staan voor andere afstanden; o=2 is 10km, etc, ontleed de url
#amp; weghalen die in de html van de paginas staat, want die schopt de urls in de war, zie bijv http://evenementen.uitslagen.nl/2013/marathonrotterdam/details.php?s=504&amp;o=1
        
        endofurl = [conv.replace('amp;','') for conv in endofurl]

#tweede basis-url

        base_url = 'http://evenementen.uitslagen.nl/2013/marathonrotterdam/details.php' #de base_url van de loper-url

#loper-url samenstellen uit de base en de resultaten van de scrape
        urlparse.urljoin(base_url, 'details.php?(.*)')

        full_urls = [urlparse.urljoin(base_url, url) for url in endofurl]

#per pagina worden alle urls nu nog in 1 lijst verzameld en dus in 1 cell opgeslagen.
#de volgende regel plaatst elk element in de lijst op een aparte regel

        for elem in full_urls:

            singleurl = elem

            #print singleurl
       
            data = {'url':singleurl}
    
            print data

            scraperwiki.sqlite.save(['url'], data) 

            #de data uit de loper-url halen
        
       