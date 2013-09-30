import scraperwiki
import urllib
import re
from bs4 import BeautifulSoup as Soup
import urlparse

base_urllist = "http://evenementen.uitslagen.nl/2013/marathonrotterdam/uitslag0"
end_url = "nl.html"


for num in range(1023, 1024):
    html = base_urllist+str(num)
    url = html+end_url #dit koppelt de drie elementen van de url aan elkaar

    page = scraperwiki.scrape(url)
    if page is not None:
        endofurl = re.findall("details.php?(.*?)>", page)

        endofurl = [conv.replace('amp;','') for conv in endofurl]

        base_url = 'http://evenementen.uitslagen.nl/2013/marathonrotterdam/details.php' #de base_url van de loper-url

        urlparse.urljoin(base_url, 'details.php?(.*)')

        full_urls = [urlparse.urljoin(base_url, url) for url in endofurl]
        
        for elem in full_urls:

            singleurl = elem

            data = {'url':singleurl}
    
            scraperwiki.sqlite.save(['url'], data)

       
            
        

import scraperwiki
import urllib
import re
from bs4 import BeautifulSoup as Soup
import urlparse

base_urllist = "http://evenementen.uitslagen.nl/2013/marathonrotterdam/uitslag0"
end_url = "nl.html"


for num in range(1023, 1024):
    html = base_urllist+str(num)
    url = html+end_url #dit koppelt de drie elementen van de url aan elkaar

    page = scraperwiki.scrape(url)
    if page is not None:
        endofurl = re.findall("details.php?(.*?)>", page)

        endofurl = [conv.replace('amp;','') for conv in endofurl]

        base_url = 'http://evenementen.uitslagen.nl/2013/marathonrotterdam/details.php' #de base_url van de loper-url

        urlparse.urljoin(base_url, 'details.php?(.*)')

        full_urls = [urlparse.urljoin(base_url, url) for url in endofurl]
        
        for elem in full_urls:

            singleurl = elem

            data = {'url':singleurl}
    
            scraperwiki.sqlite.save(['url'], data)

       
            
        

