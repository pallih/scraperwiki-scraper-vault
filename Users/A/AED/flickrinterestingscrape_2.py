import scraperwiki
import BeautifulSoup
import datetime

html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
      'years_in_school' : int(tds[4].text_content())
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['country'], data=data)





scraperwiki.sqlite.save_var('data_columns', ['id', 'title', 'owner', 'latlng_lat', 'latlng_lng', 'accuracy', 'date'])
#scraperwiki.metadata.save

#url = 'http://api.flickr.com/services/rest/?method=flickr.tags.getRelated&api_key=33fd8c6cd5aecf7be10b1c078d821db1&tag=uct'

#url = 'http://api.flickr.com/services/rest/?method=flickr.interestingness.getList&api_key=33fd8c6cd5aecf7be10b1c078d821db1&extras=geo&per_page=500&date='

#url = 'http://api.flickr.com/services/rest/?method=flickr.galleries.getList&api_key=3a5137e25b65dcd4e9e0e11809de438d&user_id=44590630%40N06'



h = datetime.date.today()
first_date = datetime.date(2011,9,1)

p = scraperwiki.sqlite.get_var('last_scraped_date', default=first_date.isoformat())
#scraperwiki.metadata.get 
#p = first_date.isoformat() #descomente para resestar o scraper
p = datetime.datetime.strptime(p, '%Y-%m-%d').date()
print "Restarting at " + p.isoformat()

while p < h:
    data = p.isoformat()
    print 'Scrape... ' + data
    xml = scraperwiki.scrape(url + data)
    soup = BeautifulSoup.BeautifulSoup(xml)
    for photo in soup.findAll('photo'):
        data = {}
        # Choose unique keyname, add optional date/latlng fields
        if (float(photo['title']) != ''):
            data['id'] = photo['id']
            data['title'] = photo['title']
            data['owner'] = photo['owner']
            data['accuracy'] = photo['accuracy']
            lat_lng = [float(photo['latitude']), float(photo['longitude'])]
            scraperwiki.datastore.save(['id'], data,date=p, latlng=lat_lng)
    p = p + datetime.timedelta(days=1)
    scraperwiki.sqlite.save_var('last_scraped_date', p.isoformat())