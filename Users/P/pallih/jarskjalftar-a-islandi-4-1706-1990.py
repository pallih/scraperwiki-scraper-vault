import scraperwiki,re
from BeautifulSoup import BeautifulSoup

quake = {}

def scrape_skjalfta(url):
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        soup.prettify()
        table = soup.find ('table', { 'width' : '80%' })
        tr = table.findAll('tr')
        for tr in tr:
            date = tr.findNext('td')
            date_store = re.sub(" \d+:\d+","",date.text)
            date_time = date.text
            time = re.sub("\d+-\d+-\d+ ","",date.text)
            location=date.findNext('td')
            lat = location.text[:4]
            lng = location.text[5:]
            latlng = [lat,lng]
            latlng_float= map(float, latlng)
            size=location.findNext('td')
            distance=size.findNext('td')
            landmark=distance.findNext('td')
            quake['date'] = date_store
            quake['time'] = time
            quake['date_time'] = date_time
            quake['lat'] = lat
            quake['lng'] = lng
            quake['size'] = size.text
            quake['distance'] = distance.text
            quake['landmark'] = landmark.text
            print quake
            scraperwiki.datastore.save(["date_time"], quake, latlng=(latlng_float))

url = 'http://hraun.vedur.is/ja/ymislegt/storskjalf.html'

scrape_skjalfta(url)

