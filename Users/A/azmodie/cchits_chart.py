''' ### CChits.net Chart Scraper ###

This script scrapes cchits.net chart listings for cchits android app

This script should only run 1 per day.

'''
import scraperwiki
from BeautifulSoup import BeautifulSoup
from collections import OrderedDict

DEBUG = False
no_pages = 2
url = 'http://www.cchits.net/'
chart = 'chart?page='
useragent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0)" \
            " Gecko/20100101 Firefox/17.0"
pages = []
for i in range(no_pages):
    pages.append(url + chart + str(i))

for page in pages:
    pagesrc = scraperwiki.scrape(page, None, useragent)
    soup = BeautifulSoup(pagesrc)
    tdata = [{}]
    for j in range(1, 26):
        table = soup.find('table')
        rows = table.findAll('tr')[j]
        cols = rows.findAll('td')
        links = rows.findAll('a')
        license = rows.findAll('abbr')
        position = cols[0].string
        trackid = links[0]['name']
        track_movement = cols[1].string
        sparkline_date = str(cols[2].find(text=True))
        sparkline = soup.find('span').get('values')
        artist = links[2].text
        artist_link = links[2]['href']
        track = links[1].string
        track_link = links[1]['href']
        status = license[0].string
        entry = OrderedDict({'Position': int(position),
                            'Track_movement': track_movement.encode("utf-8"),
                            'Sparkline': sparkline.encode("utf-8"),
                            'Sparkline Dates': sparkline_date.encode("utf-8"),
                            'Artist': artist.encode("utf-8"),
                            'Artist_Link': artist_link.encode("utf-8"),
                            'Trackid': int(trackid),
                            'Track': track.encode("utf-8"),
                            'Track_Link': track_link.encode("utf-8"),
                            'Status': status.encode("utf-8")})
        if j == 1:
            tdata[0] = entry
        else:
            tdata.append(entry)
    scraperwiki.sqlite.save(unique_keys=["Position"], data=tdata)
    del tdata

### debug ###
if DEBUG is True:
    selected = scraperwiki.sqlite.select("* from swdata")
    for select in selected:
        print select
