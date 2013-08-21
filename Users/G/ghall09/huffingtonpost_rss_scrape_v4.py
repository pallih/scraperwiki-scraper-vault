from urllib import urlopen
from BeautifulSoup import BeautifulSoup 
import re
import scraperwiki


#open and read webpage
webpage = urlopen("http://feeds.huffingtonpost.com/huffingtonpost/raw_feed").read()

#determine what to titles / links to grab (2nd through 16th)
listiterator = []
listiterator[:] = range(2,16)

soup = BeautifulSoup(webpage)

titlesoup = soup.findAll("title")

linksoup = soup.findAll("link")

#print results
for i in listiterator:
    data = {}
    data["Title"] = titlesoup[i]
    data["Link"] = linksoup[i]
    
    scraperwiki.sqlite.save(["Title"], data) 


