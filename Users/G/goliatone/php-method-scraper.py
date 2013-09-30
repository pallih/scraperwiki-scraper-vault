import scraperwiki
#import lxml.html
from bs4 import BeautifulSoup 
import urllib2

url = "http://us.php.net/quickref.php"
html = urllib2.urlopen(url).read()

pool = BeautifulSoup(html)
qref = pool.find(id="quickref_functions")

for link in qref.find_all('a'):
    print link

# Blank Python

#Create a list of the php methods.
"""
class ListPHPMethods:

    def update_list:
        url = "http://us.php.net/quickref.php"
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        data = list()
        for li in root.cssselect("ul[id='quickref_functions'] li a"):
            name = li.text
            url  = li.get("href")
            node = {
                   'url':url,
                   'name':name
            }
            data.append(node)
            scraperwiki.sqlite.save(unique_keys=['name', 'url'], data=node) 
"""
"""
import inspect

#class FetchMethodPage:
name = "zip_entry_name"
base = "http://us.php.net"
url  = "/manual/en/function.zip-entry-name.php" 
page = scraperwiki.scrape(base + url)
root = lxml.html.fromstring(page)
print lxml.html.tostring(root.body.cssselect("div[class='refentry']")[0])

"""
"""
url = "http://us.php.net/quickref.php"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
data = list()
out  = list()
for li in root.cssselect("ul[id='quickref_functions'] li a"):
    name = li.text
    url  = li.get("href")
    node = {
           'url':url,
           'name':name
    }
    out.append(name)
    data.append(node)
    scraperwiki.sqlite.save(unique_keys=['name', 'url'], data=node) 

print out
"""import scraperwiki
#import lxml.html
from bs4 import BeautifulSoup 
import urllib2

url = "http://us.php.net/quickref.php"
html = urllib2.urlopen(url).read()

pool = BeautifulSoup(html)
qref = pool.find(id="quickref_functions")

for link in qref.find_all('a'):
    print link

# Blank Python

#Create a list of the php methods.
"""
class ListPHPMethods:

    def update_list:
        url = "http://us.php.net/quickref.php"
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        data = list()
        for li in root.cssselect("ul[id='quickref_functions'] li a"):
            name = li.text
            url  = li.get("href")
            node = {
                   'url':url,
                   'name':name
            }
            data.append(node)
            scraperwiki.sqlite.save(unique_keys=['name', 'url'], data=node) 
"""
"""
import inspect

#class FetchMethodPage:
name = "zip_entry_name"
base = "http://us.php.net"
url  = "/manual/en/function.zip-entry-name.php" 
page = scraperwiki.scrape(base + url)
root = lxml.html.fromstring(page)
print lxml.html.tostring(root.body.cssselect("div[class='refentry']")[0])

"""
"""
url = "http://us.php.net/quickref.php"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
data = list()
out  = list()
for li in root.cssselect("ul[id='quickref_functions'] li a"):
    name = li.text
    url  = li.get("href")
    node = {
           'url':url,
           'name':name
    }
    out.append(name)
    data.append(node)
    scraperwiki.sqlite.save(unique_keys=['name', 'url'], data=node) 

print out
"""