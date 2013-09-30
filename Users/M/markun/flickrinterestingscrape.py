import scraperwiki
import BeautifulSoup
import datetime

scraperwiki.sqlite.save_var('data_columns', ['id', 'title', 'owner', 'latlng_lat', 'latlng_lng', 'accuracy', 'date'])
#scraperwiki.metadata.save

url = 'http://api.flickr.com/services/rest/?method=flickr.tags.getRelated&api_key=11bf05952b3f3fc783ae7f8da608d8e8&tag=Eiffel'

#url = 'http://api.flickr.com/services/rest/?method=flickr.interestingness.getList&api_key=11bf05952b3f3fc783ae7f8da608d8e8&extras=geo&per_page=500&date='

h = datetime.date.today()
first_date = datetime.date(2000,1,7)

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
        if (float(photo['latitude']) != 0.0):
            data['id'] = photo['id']
            data['title'] = photo['title']
            data['owner'] = photo['owner']
            data['accuracy'] = photo['accuracy']
            lat_lng = [float(photo['latitude']), float(photo['longitude'])]
            scraperwiki.datastore.save(['id'], data,date=p, latlng=lat_lng)
    p = p + datetime.timedelta(days=1)
    scraperwiki.sqlite.save_var('last_scraped_date', p.isoformat())import scraperwiki
import BeautifulSoup
import datetime

scraperwiki.sqlite.save_var('data_columns', ['id', 'title', 'owner', 'latlng_lat', 'latlng_lng', 'accuracy', 'date'])
#scraperwiki.metadata.save

url = 'http://api.flickr.com/services/rest/?method=flickr.tags.getRelated&api_key=11bf05952b3f3fc783ae7f8da608d8e8&tag=Eiffel'

#url = 'http://api.flickr.com/services/rest/?method=flickr.interestingness.getList&api_key=11bf05952b3f3fc783ae7f8da608d8e8&extras=geo&per_page=500&date='

h = datetime.date.today()
first_date = datetime.date(2000,1,7)

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
        if (float(photo['latitude']) != 0.0):
            data['id'] = photo['id']
            data['title'] = photo['title']
            data['owner'] = photo['owner']
            data['accuracy'] = photo['accuracy']
            lat_lng = [float(photo['latitude']), float(photo['longitude'])]
            scraperwiki.datastore.save(['id'], data,date=p, latlng=lat_lng)
    p = p + datetime.timedelta(days=1)
    scraperwiki.sqlite.save_var('last_scraped_date', p.isoformat())