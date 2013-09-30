import scraperwiki
import lxml.html


for page in range(1, 100):
    html = scraperwiki.scrape('http://www.baseball-reference.com/leagues/' % page)
    root = lxml.html.fromstring(html)
    
    for el in root.cssselect("table.tracklist tr"):           
        links = el.cssselect("a")
        artist = links[1].text
        track = links[2].text
        url = links[2].get('href')
    
        print artist, track
    
        scraperwiki.sqlite.save(['url'], { 'artist': artist, 'track': track, 'url': url } )
import scraperwiki
import lxml.html


for page in range(1, 100):
    html = scraperwiki.scrape('http://www.baseball-reference.com/leagues/' % page)
    root = lxml.html.fromstring(html)
    
    for el in root.cssselect("table.tracklist tr"):           
        links = el.cssselect("a")
        artist = links[1].text
        track = links[2].text
        url = links[2].get('href')
    
        print artist, track
    
        scraperwiki.sqlite.save(['url'], { 'artist': artist, 'track': track, 'url': url } )
