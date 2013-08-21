import scraperwiki
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer

http = httplib2.Http()
status, response = http.request('http://www.linkedin.com/jsearch?keywords=marketing&searchLocationType=I&countryCode=us#facets=keywords%3Dmarketing%26jobTitle%3D%26company%3D%26postalCode%3D%26facetsOrder%3D%26pplSearchOrigin%3DFCTD%26search%3DSearch%26searchLocationType%3DI%26countryCode%3Dus%26keepFacets%3Dtrue%26facet_LOCATION%3Dus%253A0%2520us%253A84%26openFacets%3DNETWORK%252CCOMPANY%252CLOCATION%252CTIME_POSTED')

for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
    if link.has_key('href'):
        url = link['href'].strip()
        if not url.startswith('http://www.linkedin.com') and not url.startswith('http://www.linkedin.com'):
            data =  {
                'links' : link['href']
            }
            scraperwiki.sqlite.save(unique_keys=['links'], data=data)

import scraperwiki
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer

http = httplib2.Http()
status, response = http.request('http://www.linkedin.com/jsearch?keywords=marketing&searchLocationType=I&countryCode=us#facets=keywords%3Dmarketing%26searchLocationType%3DI%26countryCode%3Dus%26keepFacets%3DkeepFacets%26facet_LOCATION%3Dus%253A0+us%253A84%26pplSearchOrigin%3DFCTD%26sortCriteria%3DR%26page_num%3D2%26openFacets%3DNETWORK%252CCOMPANY%252CLOCATION%252CTIME_POSTED')

for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
    if link.has_key('href'):
        url = link['href'].strip()
        if not url.startswith('http://www.linkedin.com') and not url.startswith('http://www.linkedin.com'):
            data =  {
                'links' : link['href']
            }
            scraperwiki.sqlite.save(unique_keys=['links'], data=data)

http = httplib2.Http()
status, response = http.request('http://www.linkedin.com/jsearch?keywords=marketing&searchLocationType=I&countryCode=us#facets=keywords%3Dmarketing%26searchLocationType%3DI%26countryCode%3Dus%26keepFacets%3DkeepFacets%26facet_LOCATION%3Dus%253A0+us%253A84%26pplSearchOrigin%3DFCTD%26sortCriteria%3DR%26page_num%3D3%26openFacets%3DNETWORK%252CCOMPANY%252CLOCATION%252CTIME_POSTED')

for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
    if link.has_key('href'):
        url = link['href'].strip()
        if not url.startswith('http://www.linkedin.com') and not url.startswith('http://www.linkedin.com'):
            data =  {
                'links' : link['href']
            }
            scraperwiki.sqlite.save(unique_keys=['links'], data=data)