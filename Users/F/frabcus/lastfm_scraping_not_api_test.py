import scraperwiki
import lxml.html

for n in range(1,100):
    html = scraperwiki.scrape("http://www.last.fm/user/frabcus/tracks?page=%d" % n)
    print html
    root = lxml.html.fromstring(html)
    
    for el in root.cssselect(".tracklist tr"):           
        print el
        links = el.cssselect(".subjectCell a")
        artist = links[0].text
        track = links[1].text
        link = links[1].attrib['href']
        
        scraperwiki.sqlite.save(['link'], { 'artist': artist, 'track': track, 'link': link })
    
