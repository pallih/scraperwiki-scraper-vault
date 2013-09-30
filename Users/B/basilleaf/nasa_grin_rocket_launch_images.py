import scraperwiki
import os.path, urllib  
import exceptions, urllib2, re
from BeautifulSoup import BeautifulStoneSoup
import sys
import re
import datetime
import time
import collections

base_url = 'http://grin.hq.nasa.gov' # base url of the website
index_url = 'http://grin.hq.nasa.gov/BROWSE/rocket_launch.html' # index page with all the things
# url = 'http://grin.hq.nasa.gov/BROWSE/rocket_launch_7.html' # just one page of index

# fields and patterns to search for in the detail pages (GRIN has it's own special tags around data)
all_patterns = {
    'GRIN_id' : '<!-- GRINNUMBER-BEGIN -->(.*?)<!-- GRINNUMBER-END -->',
    'title' : '<!-- ONE-LINE-DESCRIPTION-BEGIN -->(.*?)<!-- ONE-LINE-DESCRIPTION-END -->',
    'description' : '<!-- DESCRIPTION-BEGIN -->(.*?)<!-- DESCRIPTION-END -->',
    'keywords' : '<!-- KEYWORD-BEGIN -->(.*?)<!-- KEYWORD-END -->',
    'date' : '<!-- DATE-BEGIN --(.*?)-- DATE-END -->',
}

try:
    index_page = urllib2.urlopen(index_url).read()   
except urllib2.HTTPError:
    raise Exception("Http 404 - invalid start url: " + index_url)

index_soup = BeautifulStoneSoup(index_page) 
all_links = index_soup.findAll('a')   


# get all the detail pages:
all_pages = []
for link in all_links:
    if str(link.contents[0]) == 'More information':
        all_pages.append(base_url + link['href'])

# scrape data from each detail page
for page_url in all_pages:
    try:
        page = urllib2.urlopen(page_url).read()   
    except urllib2.HTTPError:
        raise Exception("Http 404 " + page_url)
    
    try: 
        data = {} # collections.OrderedDict() # but ScraperWiki not liking..
        soup = BeautifulStoneSoup(page) 
        data['credit'] = ''.join(str(soup.findAll('ul')[1]).splitlines())
        for field, pattern in all_patterns.items():
            data[field] = ('').join(re.findall(pattern,page,re.DOTALL|re.MULTILINE)[0].splitlines())

        data['Thumbnail'] = soup.find('a',text='Thumbnail').parent['href']
        data['Small'] = soup.find('a',text='Small').parent['href']
        data['Medium'] = soup.find('a',text='Medium').parent['href']
        data['Large'] = soup.find('a',text='Large').parent['href']
        data['page_url'] = page_url
        
        # handle the date field
        if data['date']:
            t = time.strptime(data['date'], "%Y%m%d") 
            data['date'] = time.strftime('%B %d, %Y', t)

        print data
        # update scraperwiki
        scraperwiki.sqlite.save(unique_keys=['GRIN_id'], data=data)

    except: # it's sunday night and I'm lazy!
        pass


import scraperwiki
import os.path, urllib  
import exceptions, urllib2, re
from BeautifulSoup import BeautifulStoneSoup
import sys
import re
import datetime
import time
import collections

base_url = 'http://grin.hq.nasa.gov' # base url of the website
index_url = 'http://grin.hq.nasa.gov/BROWSE/rocket_launch.html' # index page with all the things
# url = 'http://grin.hq.nasa.gov/BROWSE/rocket_launch_7.html' # just one page of index

# fields and patterns to search for in the detail pages (GRIN has it's own special tags around data)
all_patterns = {
    'GRIN_id' : '<!-- GRINNUMBER-BEGIN -->(.*?)<!-- GRINNUMBER-END -->',
    'title' : '<!-- ONE-LINE-DESCRIPTION-BEGIN -->(.*?)<!-- ONE-LINE-DESCRIPTION-END -->',
    'description' : '<!-- DESCRIPTION-BEGIN -->(.*?)<!-- DESCRIPTION-END -->',
    'keywords' : '<!-- KEYWORD-BEGIN -->(.*?)<!-- KEYWORD-END -->',
    'date' : '<!-- DATE-BEGIN --(.*?)-- DATE-END -->',
}

try:
    index_page = urllib2.urlopen(index_url).read()   
except urllib2.HTTPError:
    raise Exception("Http 404 - invalid start url: " + index_url)

index_soup = BeautifulStoneSoup(index_page) 
all_links = index_soup.findAll('a')   


# get all the detail pages:
all_pages = []
for link in all_links:
    if str(link.contents[0]) == 'More information':
        all_pages.append(base_url + link['href'])

# scrape data from each detail page
for page_url in all_pages:
    try:
        page = urllib2.urlopen(page_url).read()   
    except urllib2.HTTPError:
        raise Exception("Http 404 " + page_url)
    
    try: 
        data = {} # collections.OrderedDict() # but ScraperWiki not liking..
        soup = BeautifulStoneSoup(page) 
        data['credit'] = ''.join(str(soup.findAll('ul')[1]).splitlines())
        for field, pattern in all_patterns.items():
            data[field] = ('').join(re.findall(pattern,page,re.DOTALL|re.MULTILINE)[0].splitlines())

        data['Thumbnail'] = soup.find('a',text='Thumbnail').parent['href']
        data['Small'] = soup.find('a',text='Small').parent['href']
        data['Medium'] = soup.find('a',text='Medium').parent['href']
        data['Large'] = soup.find('a',text='Large').parent['href']
        data['page_url'] = page_url
        
        # handle the date field
        if data['date']:
            t = time.strptime(data['date'], "%Y%m%d") 
            data['date'] = time.strftime('%B %d, %Y', t)

        print data
        # update scraperwiki
        scraperwiki.sqlite.save(unique_keys=['GRIN_id'], data=data)

    except: # it's sunday night and I'm lazy!
        pass


import scraperwiki
import os.path, urllib  
import exceptions, urllib2, re
from BeautifulSoup import BeautifulStoneSoup
import sys
import re
import datetime
import time
import collections

base_url = 'http://grin.hq.nasa.gov' # base url of the website
index_url = 'http://grin.hq.nasa.gov/BROWSE/rocket_launch.html' # index page with all the things
# url = 'http://grin.hq.nasa.gov/BROWSE/rocket_launch_7.html' # just one page of index

# fields and patterns to search for in the detail pages (GRIN has it's own special tags around data)
all_patterns = {
    'GRIN_id' : '<!-- GRINNUMBER-BEGIN -->(.*?)<!-- GRINNUMBER-END -->',
    'title' : '<!-- ONE-LINE-DESCRIPTION-BEGIN -->(.*?)<!-- ONE-LINE-DESCRIPTION-END -->',
    'description' : '<!-- DESCRIPTION-BEGIN -->(.*?)<!-- DESCRIPTION-END -->',
    'keywords' : '<!-- KEYWORD-BEGIN -->(.*?)<!-- KEYWORD-END -->',
    'date' : '<!-- DATE-BEGIN --(.*?)-- DATE-END -->',
}

try:
    index_page = urllib2.urlopen(index_url).read()   
except urllib2.HTTPError:
    raise Exception("Http 404 - invalid start url: " + index_url)

index_soup = BeautifulStoneSoup(index_page) 
all_links = index_soup.findAll('a')   


# get all the detail pages:
all_pages = []
for link in all_links:
    if str(link.contents[0]) == 'More information':
        all_pages.append(base_url + link['href'])

# scrape data from each detail page
for page_url in all_pages:
    try:
        page = urllib2.urlopen(page_url).read()   
    except urllib2.HTTPError:
        raise Exception("Http 404 " + page_url)
    
    try: 
        data = {} # collections.OrderedDict() # but ScraperWiki not liking..
        soup = BeautifulStoneSoup(page) 
        data['credit'] = ''.join(str(soup.findAll('ul')[1]).splitlines())
        for field, pattern in all_patterns.items():
            data[field] = ('').join(re.findall(pattern,page,re.DOTALL|re.MULTILINE)[0].splitlines())

        data['Thumbnail'] = soup.find('a',text='Thumbnail').parent['href']
        data['Small'] = soup.find('a',text='Small').parent['href']
        data['Medium'] = soup.find('a',text='Medium').parent['href']
        data['Large'] = soup.find('a',text='Large').parent['href']
        data['page_url'] = page_url
        
        # handle the date field
        if data['date']:
            t = time.strptime(data['date'], "%Y%m%d") 
            data['date'] = time.strftime('%B %d, %Y', t)

        print data
        # update scraperwiki
        scraperwiki.sqlite.save(unique_keys=['GRIN_id'], data=data)

    except: # it's sunday night and I'm lazy!
        pass


import scraperwiki
import os.path, urllib  
import exceptions, urllib2, re
from BeautifulSoup import BeautifulStoneSoup
import sys
import re
import datetime
import time
import collections

base_url = 'http://grin.hq.nasa.gov' # base url of the website
index_url = 'http://grin.hq.nasa.gov/BROWSE/rocket_launch.html' # index page with all the things
# url = 'http://grin.hq.nasa.gov/BROWSE/rocket_launch_7.html' # just one page of index

# fields and patterns to search for in the detail pages (GRIN has it's own special tags around data)
all_patterns = {
    'GRIN_id' : '<!-- GRINNUMBER-BEGIN -->(.*?)<!-- GRINNUMBER-END -->',
    'title' : '<!-- ONE-LINE-DESCRIPTION-BEGIN -->(.*?)<!-- ONE-LINE-DESCRIPTION-END -->',
    'description' : '<!-- DESCRIPTION-BEGIN -->(.*?)<!-- DESCRIPTION-END -->',
    'keywords' : '<!-- KEYWORD-BEGIN -->(.*?)<!-- KEYWORD-END -->',
    'date' : '<!-- DATE-BEGIN --(.*?)-- DATE-END -->',
}

try:
    index_page = urllib2.urlopen(index_url).read()   
except urllib2.HTTPError:
    raise Exception("Http 404 - invalid start url: " + index_url)

index_soup = BeautifulStoneSoup(index_page) 
all_links = index_soup.findAll('a')   


# get all the detail pages:
all_pages = []
for link in all_links:
    if str(link.contents[0]) == 'More information':
        all_pages.append(base_url + link['href'])

# scrape data from each detail page
for page_url in all_pages:
    try:
        page = urllib2.urlopen(page_url).read()   
    except urllib2.HTTPError:
        raise Exception("Http 404 " + page_url)
    
    try: 
        data = {} # collections.OrderedDict() # but ScraperWiki not liking..
        soup = BeautifulStoneSoup(page) 
        data['credit'] = ''.join(str(soup.findAll('ul')[1]).splitlines())
        for field, pattern in all_patterns.items():
            data[field] = ('').join(re.findall(pattern,page,re.DOTALL|re.MULTILINE)[0].splitlines())

        data['Thumbnail'] = soup.find('a',text='Thumbnail').parent['href']
        data['Small'] = soup.find('a',text='Small').parent['href']
        data['Medium'] = soup.find('a',text='Medium').parent['href']
        data['Large'] = soup.find('a',text='Large').parent['href']
        data['page_url'] = page_url
        
        # handle the date field
        if data['date']:
            t = time.strptime(data['date'], "%Y%m%d") 
            data['date'] = time.strftime('%B %d, %Y', t)

        print data
        # update scraperwiki
        scraperwiki.sqlite.save(unique_keys=['GRIN_id'], data=data)

    except: # it's sunday night and I'm lazy!
        pass


