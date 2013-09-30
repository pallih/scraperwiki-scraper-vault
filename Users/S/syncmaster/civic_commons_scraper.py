import scraperwiki

# Blank Python
#changed from BeautifulSoup to bs4 as soup.find_all('a') did not work
from bs4 import BeautifulSoup
import re
import urllib2

base_url = "http://civiccommons.org"
url = "http://civiccommons.org/apps"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())

###*************************************************************************###
##### 2. Takes only the contents of a-href and not the whole tag           ####
##### link_tag.get('href') gives just the relative link. So appending base url to every link ####
###*************************************************************************###

list_of_links = [] #creating empty list

for link_tag in soup.findAll('a', href=re.compile('^/software-licenses.*')):
   string_temp_link = base_url+link_tag.get('href')
   list_of_links.append(string_temp_link)

for link_item in list_of_links:
    print link_item
import scraperwiki

# Blank Python
#changed from BeautifulSoup to bs4 as soup.find_all('a') did not work
from bs4 import BeautifulSoup
import re
import urllib2

base_url = "http://civiccommons.org"
url = "http://civiccommons.org/apps"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())

###*************************************************************************###
##### 2. Takes only the contents of a-href and not the whole tag           ####
##### link_tag.get('href') gives just the relative link. So appending base url to every link ####
###*************************************************************************###

list_of_links = [] #creating empty list

for link_tag in soup.findAll('a', href=re.compile('^/software-licenses.*')):
   string_temp_link = base_url+link_tag.get('href')
   list_of_links.append(string_temp_link)

for link_item in list_of_links:
    print link_item
