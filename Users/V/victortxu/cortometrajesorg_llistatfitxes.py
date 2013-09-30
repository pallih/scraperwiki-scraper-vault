import scraperwiki
import lxml.html
#from bs4 import BeautifulSoup

html = scraperwiki.scrape("http://cortometrajes.org/cortometrajes/")
root = lxml.html.fromstring(html)
#raw = BeautifulSoup(html)


for el in root.cssselect("div.post-text a"):           
    print el.attrib['href']
    #print el.text
    #print el.tail
    #print (tag.href)

#for el in raw.findAll(class="post-text"):           
    #print el.attrib['href']
    #print el.text
    #print el.tail
    #print (tag.href)import scraperwiki
import lxml.html
#from bs4 import BeautifulSoup

html = scraperwiki.scrape("http://cortometrajes.org/cortometrajes/")
root = lxml.html.fromstring(html)
#raw = BeautifulSoup(html)


for el in root.cssselect("div.post-text a"):           
    print el.attrib['href']
    #print el.text
    #print el.tail
    #print (tag.href)

#for el in raw.findAll(class="post-text"):           
    #print el.attrib['href']
    #print el.text
    #print el.tail
    #print (tag.href)