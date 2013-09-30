# pseudo code for http://www.allmusic.com/
import sys
import scraperwiki
import lxml.html

""" Testing code
try:
    #html = scraperwiki.scrape('http://www.allmusic.com/artist/pnk-p365124')
    html = scraperwiki.scrape('http://www.allmusic.com/album/mssundaztood-r558494')
    print html
    rows = root.cssselect("table.data tr")
except:
    print 'no'
"""



#exit because this will not run yet
sys.exit()

def scrape_artist(root):
    print 'TODO'
    #do something
    #record = { "td" : td.text } # column name and value
    #scraperwiki.datastore.save(["td"], record) # save the records one by one

def scrape_album(root):
    print 'TODO'
     #do something

#grab all the artists until we get 10 sequential 404s
sequential404s=0
MAXsequential=10
artist_URL='http://www.allmusic.com/artist/p'
for i in range(sys.maxint):
    try:
        html = scraperwiki.scrape(artist_URL+str(i))
        sequential404s=0
        root = lxml.html.fromstring(html)
        scrape_artist(root)
    except:
        sequential404s+=1
    if sequential404s>MAXsequential:
        break

#grab all the albums until we get 10 sequential 404s
sequential404s=0
album_URL='http://www.allmusic.com/artist/r'
for i in range(sys.maxint):
    try:
        html = scraperwiki.scrape(album_URL+str(i))
        sequential404s=0
        root = lxml.html.fromstring(html)
        scrape_album(root)
    except:
        sequential404s+=1
    if sequential404s>MAXsequential:
        break





#EOF
# pseudo code for http://www.allmusic.com/
import sys
import scraperwiki
import lxml.html

""" Testing code
try:
    #html = scraperwiki.scrape('http://www.allmusic.com/artist/pnk-p365124')
    html = scraperwiki.scrape('http://www.allmusic.com/album/mssundaztood-r558494')
    print html
    rows = root.cssselect("table.data tr")
except:
    print 'no'
"""



#exit because this will not run yet
sys.exit()

def scrape_artist(root):
    print 'TODO'
    #do something
    #record = { "td" : td.text } # column name and value
    #scraperwiki.datastore.save(["td"], record) # save the records one by one

def scrape_album(root):
    print 'TODO'
     #do something

#grab all the artists until we get 10 sequential 404s
sequential404s=0
MAXsequential=10
artist_URL='http://www.allmusic.com/artist/p'
for i in range(sys.maxint):
    try:
        html = scraperwiki.scrape(artist_URL+str(i))
        sequential404s=0
        root = lxml.html.fromstring(html)
        scrape_artist(root)
    except:
        sequential404s+=1
    if sequential404s>MAXsequential:
        break

#grab all the albums until we get 10 sequential 404s
sequential404s=0
album_URL='http://www.allmusic.com/artist/r'
for i in range(sys.maxint):
    try:
        html = scraperwiki.scrape(album_URL+str(i))
        sequential404s=0
        root = lxml.html.fromstring(html)
        scrape_album(root)
    except:
        sequential404s+=1
    if sequential404s>MAXsequential:
        break





#EOF
