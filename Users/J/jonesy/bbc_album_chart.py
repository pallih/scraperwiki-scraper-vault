import scraperwiki
from lxml import html

url = "http://www.bbc.co.uk/radio1/chart/albums"
doc_text = scraperwiki.scrape(url)
doc = html.fromstring(doc_text)

counter = 0

for row in doc.cssselect(".chart ol li"):
    artist = row.cssselect(".artist").pop()
    album = row.cssselect(".track").pop()
    position = row.cssselect(".position").pop()
    print "array('artist'=>'" + artist.text + "', 'album'=>'" + album.text + "', position=>'" + position.text + "'),"
    data = {
        'artist': artist.text,
        'album': album.text,
        'position': position.text,
    }

    scraperwiki.sqlite.save(unique_keys=["position"], data=data)
    
counter += 1

print counterimport scraperwiki
from lxml import html

url = "http://www.bbc.co.uk/radio1/chart/albums"
doc_text = scraperwiki.scrape(url)
doc = html.fromstring(doc_text)

counter = 0

for row in doc.cssselect(".cht-entry-wrapper"):
    artist = row.cssselect(".cht-entry-artist").pop()
    album = row.cssselect(".cht-entry-title").pop()
    position = counter+1
    print "array('artist'=>'" + artist.text + "', 'album'=>'" + album.text + "', 'position'=>" + str(position)+ "),"
    data = {
        'artist': artist.text,
        'album': album.text,
        'position': position,
    }

    scraperwiki.sqlite.save(unique_keys=["position"], data=data)
    counter += 1

print counter