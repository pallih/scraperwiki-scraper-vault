'''
import scraperwiki
import csv
import requests
import string
import time

from bs4 import BeautifulSoup
from types import *

URL = 'http://www.yellowpages.com/carlsbad-ca/commercial-real-estate?g=Carlsbad%2C+CA&q=commercial+real+estate'
response = requests.get(URL)
print response.status_code
'''
'''
import urllib
import urllib2

url = 'http://www.google.com'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
values = {'name' : 'Michael',
          'location' : 'Northampton',
          'language' : 'Python' }
headers = { 'User-Agent' : user_agent }

data = urllib.urlencode(values)
req = urllib2.Request(url, data, headers)
#req = urllib2.Request(url, headers)
response = urllib2.urlopen(req)
the_page = response.read()
'''

import scraperwiki
import urllib
import urllib2

URL = 'http://www.yellowpages.com/carlsbad-ca/commercial-real-estate?g=Carlsbad%2C+CA&q=commercial+real+estate'

headers = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
req = urllib2.Request("http://www.yellowpages.com/carlsbad-ca/commercial-real-estate?g=Carlsbad%2C+CA&q=commercial+real+estate", headers=headers)
urllib2.urlopen(req)
'''
import scraperwiki
import csv
import requests
import string
import time

from bs4 import BeautifulSoup
from types import *

URL = 'http://www.yellowpages.com/carlsbad-ca/commercial-real-estate?g=Carlsbad%2C+CA&q=commercial+real+estate'
response = requests.get(URL)
print response.status_code
'''
'''
import urllib
import urllib2

url = 'http://www.google.com'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
values = {'name' : 'Michael',
          'location' : 'Northampton',
          'language' : 'Python' }
headers = { 'User-Agent' : user_agent }

data = urllib.urlencode(values)
req = urllib2.Request(url, data, headers)
#req = urllib2.Request(url, headers)
response = urllib2.urlopen(req)
the_page = response.read()
'''

import scraperwiki
import urllib
import urllib2

URL = 'http://www.yellowpages.com/carlsbad-ca/commercial-real-estate?g=Carlsbad%2C+CA&q=commercial+real+estate'

headers = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
req = urllib2.Request("http://www.yellowpages.com/carlsbad-ca/commercial-real-estate?g=Carlsbad%2C+CA&q=commercial+real+estate", headers=headers)
urllib2.urlopen(req)
