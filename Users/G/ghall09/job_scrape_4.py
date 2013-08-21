from urllib import urlopen
from BeautifulSoup import BeautifulSoup 
import re
import scraperwiki

#open and read webpage
webpage = urlopen("http://jobs.experian.com/sitemap.xml").read()

#locate article title
link = re.compile('<loc>(.*)</loc>')
mod = re.compile('<lastmod>(.*)</lastmod>')
priority = re.compile('<priority>(.*)</priority>')

#search for article title
findlink = re.findall(link, webpage)
findmod = re.findall(mod, webpage)
findpriority = re.findall(priority, webpage)

#determine what to titles / links to grab (2nd through 16th)
listiterator = []
listiterator[:] = range(0,3)

#print results
for i in listiterator:
    print findlink[i]
    print findmod[i]
#    print findpriority[i]

    reqpage = urlopen(findlink[i]).read()

    titleraw = re.compile("<span itemprop=\"title\">(.*)</span>")
    findtitleraw = re.findall(titleraw, reqpage)

    titleraw = re.compile("<span itemprop=\"title\">(.*)</span>")
    findtitleraw = re.findall(titleraw, reqpage)

print webpage
    
