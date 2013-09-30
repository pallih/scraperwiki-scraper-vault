import scraperwiki
import urllib2
from bs4 import BeautifulSoup
import re

url ="https://projecteuler.net/problem="

def get_page(url,num):
    content = None
    try:
        content = urllib2.urlopen(url+str(num)).read()
        return content
    except urllib2.URLError:
        return content

def extract_main (page):
    soup = BeautifulSoup(page)
    content = soup.find('div', attrs={'id' : 'content'})
    return content

contentAll = []
for i in range (1,420):
    contentAll.append(extract_main(get_page(url,i)))
    scraperwiki.sqlite.save(unique_keys=["id"], data={"id":i,"content":get_page(url,i)})


data = scraperwiki.sqlite.select(
    '''* FROM swdata ORDER BY id '''
)
print data 

print contentAll
    import scraperwiki
import urllib2
from bs4 import BeautifulSoup
import re

url ="https://projecteuler.net/problem="

def get_page(url,num):
    content = None
    try:
        content = urllib2.urlopen(url+str(num)).read()
        return content
    except urllib2.URLError:
        return content

def extract_main (page):
    soup = BeautifulSoup(page)
    content = soup.find('div', attrs={'id' : 'content'})
    return content

contentAll = []
for i in range (1,420):
    contentAll.append(extract_main(get_page(url,i)))
    scraperwiki.sqlite.save(unique_keys=["id"], data={"id":i,"content":get_page(url,i)})


data = scraperwiki.sqlite.select(
    '''* FROM swdata ORDER BY id '''
)
print data 

print contentAll
    