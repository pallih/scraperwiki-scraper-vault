###############################################
#   Scrapper to get Trailer  information
##############################################

import scraperwiki
import lxml.html



#html = scraperwiki.scrape("http://en.600024.com/movie/latest-tamil-movies")
#root = lxml.html.fromstring(html)
#for table in root.cssselect("div."):
#    for row in root.cssselect("tr"):
#        td = root.cssselect("td")
#        print lxml.html.tostring(td[0])

links=["http://www.behindwoods.com/features/Trailers/trailers1/index.html"]


html = scraperwiki.scrape(links[0])
root = lxml.html.fromstring(html)
movieName=[]
movieLink=[]
movie=[]

def moreLink(root):
    for tr in root.cssselect("div[align='right']"):
        more = lxml.html.fromstring(lxml.html.tostring(tr))
        for el in more.cssselect("a font"):
            if "MORE" in el.text:
                links.append(more.cssselect("a")[1].attrib['href'])
moreLink(root)
moreLink(lxml.html.fromstring(scraperwiki.scrape(links[1])))
moreLink(lxml.html.fromstring(scraperwiki.scrape(links[2])))
def getTrailerLink(root):
    film = []
    movie=root.cssselect("a.gallery-head-new")
    for el in movie:
        if "TRAILER" in el.text:
            movieName.append(el.text)
            movieLink.append(el.attrib['href'])

getTrailerLink(root)
getTrailerLink(lxml.html.fromstring(scraperwiki.scrape(links[1])))
getTrailerLink(lxml.html.fromstring(scraperwiki.scrape(links[2])))
getTrailerLink(lxml.html.fromstring(scraperwiki.scrape(links[3])))

for i in movieName:
    print i

for i in movieLink:
    
###############################################
#   Scrapper to get Trailer  information
##############################################

import scraperwiki
import lxml.html



#html = scraperwiki.scrape("http://en.600024.com/movie/latest-tamil-movies")
#root = lxml.html.fromstring(html)
#for table in root.cssselect("div."):
#    for row in root.cssselect("tr"):
#        td = root.cssselect("td")
#        print lxml.html.tostring(td[0])

links=["http://www.behindwoods.com/features/Trailers/trailers1/index.html"]


html = scraperwiki.scrape(links[0])
root = lxml.html.fromstring(html)
movieName=[]
movieLink=[]
movie=[]

def moreLink(root):
    for tr in root.cssselect("div[align='right']"):
        more = lxml.html.fromstring(lxml.html.tostring(tr))
        for el in more.cssselect("a font"):
            if "MORE" in el.text:
                links.append(more.cssselect("a")[1].attrib['href'])
moreLink(root)
moreLink(lxml.html.fromstring(scraperwiki.scrape(links[1])))
moreLink(lxml.html.fromstring(scraperwiki.scrape(links[2])))
def getTrailerLink(root):
    film = []
    movie=root.cssselect("a.gallery-head-new")
    for el in movie:
        if "TRAILER" in el.text:
            movieName.append(el.text)
            movieLink.append(el.attrib['href'])

getTrailerLink(root)
getTrailerLink(lxml.html.fromstring(scraperwiki.scrape(links[1])))
getTrailerLink(lxml.html.fromstring(scraperwiki.scrape(links[2])))
getTrailerLink(lxml.html.fromstring(scraperwiki.scrape(links[3])))

for i in movieName:
    print i

for i in movieLink:
    
