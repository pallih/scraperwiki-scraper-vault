import scraperwiki
import lxml.html
import re

base_url = "http://www.lyricsmania.com/robbie_williams_lyrics.html"

html = scraperwiki.scrape(base_url)
print html
root = lxml.html.fromstring(html)

album_block = root.xpath('//*[@id="albums"]/table[2]')
index = 0
albums = album_block[0].cssselect("td")
for album in albums: 
    year = re.search(r"\(\d\d\d\d\)", lxml.html.tostring(album))
    if year.group(0):
        year1 = year.group(0)
        year1 = year1.replace("(", "")
        year1 = year1.replace(")", "")
        print year1
    else:
        year1 = ""
    
    print lxml.html.tostring(album)
    titles = album.cssselect("h2")
    print titles[0].text_content()
    songs = album.cssselect("li")
    for song in songs:
        record = {}
        index += 1
        record['index'] = index
        record['year'] = year1
        record['album'] = titles[0].text_content()
        record['song'] = song.text_content()
        song_url = song.cssselect("a")
        record['url'] = "http://www.lyricsmania.com"+song[0].attrib['href']
        scraperwiki.sqlite.save(['index'], record) 

import scraperwiki
import lxml.html
import re

base_url = "http://www.lyricsmania.com/robbie_williams_lyrics.html"

html = scraperwiki.scrape(base_url)
print html
root = lxml.html.fromstring(html)

album_block = root.xpath('//*[@id="albums"]/table[2]')
index = 0
albums = album_block[0].cssselect("td")
for album in albums: 
    year = re.search(r"\(\d\d\d\d\)", lxml.html.tostring(album))
    if year.group(0):
        year1 = year.group(0)
        year1 = year1.replace("(", "")
        year1 = year1.replace(")", "")
        print year1
    else:
        year1 = ""
    
    print lxml.html.tostring(album)
    titles = album.cssselect("h2")
    print titles[0].text_content()
    songs = album.cssselect("li")
    for song in songs:
        record = {}
        index += 1
        record['index'] = index
        record['year'] = year1
        record['album'] = titles[0].text_content()
        record['song'] = song.text_content()
        song_url = song.cssselect("a")
        record['url'] = "http://www.lyricsmania.com"+song[0].attrib['href']
        scraperwiki.sqlite.save(['index'], record) 

