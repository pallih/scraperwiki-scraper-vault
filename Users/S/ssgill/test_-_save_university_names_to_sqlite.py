import scraperwiki
from BeautifulSoup import BeautifulSoup
import urllib2

# 

url="http://www.utexas.edu/world/univ/alpha/"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())

universities=soup.findAll('a',{'class':'institution'})

p =1
if p < 10:
    for eachuniversity in universities:
#        record = {"university" : eachuniversity.text}
        scraperwiki.sqlite.save(unique_keys = ["university"], data={"university": eachuniversity.text})
        p = p+1

        
#scraperwiki.sqlite.save(unique_keys = ["university"], data={"university": eachuniversity.text,"url":eachuniversity.attrib['href']})
#example of multi field sqlsave
#scraperwiki.sqlite.save(unique_keys=['url'], data={'title': el.text, 'url': el.attrib['href'], 'num_python_scrapers': matching_python_scrapers})
#    print eachuniversity['href']+","+eachuniversity.string

import scraperwiki
from BeautifulSoup import BeautifulSoup
import urllib2

# 

url="http://www.utexas.edu/world/univ/alpha/"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())

universities=soup.findAll('a',{'class':'institution'})

p =1
if p < 10:
    for eachuniversity in universities:
#        record = {"university" : eachuniversity.text}
        scraperwiki.sqlite.save(unique_keys = ["university"], data={"university": eachuniversity.text})
        p = p+1

        
#scraperwiki.sqlite.save(unique_keys = ["university"], data={"university": eachuniversity.text,"url":eachuniversity.attrib['href']})
#example of multi field sqlsave
#scraperwiki.sqlite.save(unique_keys=['url'], data={'title': el.text, 'url': el.attrib['href'], 'num_python_scrapers': matching_python_scrapers})
#    print eachuniversity['href']+","+eachuniversity.string

