# code pool example show by scraperwiki

import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://last.fm/user/apple/tracks")
root = lxml.html.fromstring(html)
for el in root.cssselect("table.tracklist tr"):
    links=el.cssselect("a")
    artist=links[1].text
    track=links[1].text
    url=links[2].get('href')
    scraperwiki.sqlite.save(['url'],{'artist':artist, 'track':track, 'url':url})

# code pool example show by scraperwiki

import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://last.fm/user/apple/tracks")
root = lxml.html.fromstring(html)
for el in root.cssselect("table.tracklist tr"):
    links=el.cssselect("a")
    artist=links[1].text
    track=links[1].text
    url=links[2].get('href')
    scraperwiki.sqlite.save(['url'],{'artist':artist, 'track':track, 'url':url})

