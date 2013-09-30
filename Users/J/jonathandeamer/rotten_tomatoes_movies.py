import scraperwiki
import urllib2
import simplejson


API_key = "7c7a6pa7tgcttzz67k3jyej5"

movie_IDs = []

def get_IDs(API_key):
    movie_IDs = []
    all_scraped_dict = (scraperwiki.sqlite.select(           
    '''id from swdata'''
    ))
    all_scraped = []
    for each in all_scraped_dict:
        all_scraped.append(each['id'])

    print all_scraped
    URL = "http://api.rottentomatoes.com/api/public/v1.0/lists/movies/opening.json?page_limit=999&apikey=" + API_key
    req = urllib2.Request(URL)
    opener = urllib2.build_opener()
    f = opener.open(req)
    a = simplejson.load(f)['movies']
    for each in a:
        if each['id'] not in all_scraped:
            movie_IDs.append(each['id'])

    """URL = "http://api.rottentomatoes.com/api/public/v1.0/lists/movies/in_theaters.json?page_limit=999&apikey=" + API_key
    req = urllib2.Request(URL)
    opener = urllib2.build_opener()
    f = opener.open(req)
    a = simplejson.load(f)['movies']
    for each in a:
        movie_IDs.append(each['id'])"""

    URL = "http://api.rottentomatoes.com/api/public/v1.0/lists/movies/box_office.json?page_limit=999&apikey=" + API_key
    req = urllib2.Request(URL)
    opener = urllib2.build_opener()
    f = opener.open(req)
    a = simplejson.load(f)['movies']
    for each in a:
        if each['id'] not in all_scraped:
            movie_IDs.append(each['id'])

    
   
    
    highest_scraped = 770672122 #max(all_scraped)

    while len(movie_IDs) < 500:
        highest_scraped = highest_scraped - 1
        print len(movie_IDs)
        if highest_scraped not in all_scraped:
            movie_IDs.append(highest_scraped)
    
    '''
lowest_movie_ID = scraperwiki.sqlite.select(           
        id from swdata order by id asc limit 1
    ) 
Nothing below ID 8937?
    for each in range(1,8000):
        if (int(lowest_movie_ID[0]['id'])-each) > 0:
            movie_IDs.append(int(lowest_movie_ID[0]['id'])-each)'''

    return movie_IDs

def get_movie(movie_ID, API_key):
    movie_data = {'id':'','title':'','year':'','mpaa_rating':'','genres':'','ratings':''}
    for each in movie_data:
        try:
            URL = "http://api.rottentomatoes.com/api/public/v1.0/movies/" + str(movie_ID) + ".json?apikey=" + API_key
            #URL = "http://api.rottentomatoes.com/api/public/v1.0/movie_alias.json?id=" + str(movie_ID) + "&type=imdb&apikey=" + API_key
            req = urllib2.Request(URL)
            opener = urllib2.build_opener()
            f = opener.open(req)
            movie_data[each] = simplejson.load(f)[each]
        except KeyError:
            print "ID not found: " + str(movie_ID)
        except urllib2.HTTPError:
            print "HTTPError"
    try:
        scraperwiki.sqlite.save(unique_keys=["id"], data={
        "id":movie_data['id'],
        "title":movie_data['title'],
        "year":movie_data['year'],
        "mpaa_rating":movie_data['mpaa_rating'],
        "genres":movie_data['genres'],
        "critics_score":dict(movie_data['ratings'])['critics_score'],
        "audience_score":dict(movie_data['ratings'])['audience_score']})   
    except KeyError:
        print "ID not found: " + str(movie_ID)

for each in get_IDs(API_key):
    if each not in movie_IDs:
        movie_IDs.append(each)

for each in movie_IDs:
    get_movie(each, API_key)import scraperwiki
import urllib2
import simplejson


API_key = "7c7a6pa7tgcttzz67k3jyej5"

movie_IDs = []

def get_IDs(API_key):
    movie_IDs = []
    all_scraped_dict = (scraperwiki.sqlite.select(           
    '''id from swdata'''
    ))
    all_scraped = []
    for each in all_scraped_dict:
        all_scraped.append(each['id'])

    print all_scraped
    URL = "http://api.rottentomatoes.com/api/public/v1.0/lists/movies/opening.json?page_limit=999&apikey=" + API_key
    req = urllib2.Request(URL)
    opener = urllib2.build_opener()
    f = opener.open(req)
    a = simplejson.load(f)['movies']
    for each in a:
        if each['id'] not in all_scraped:
            movie_IDs.append(each['id'])

    """URL = "http://api.rottentomatoes.com/api/public/v1.0/lists/movies/in_theaters.json?page_limit=999&apikey=" + API_key
    req = urllib2.Request(URL)
    opener = urllib2.build_opener()
    f = opener.open(req)
    a = simplejson.load(f)['movies']
    for each in a:
        movie_IDs.append(each['id'])"""

    URL = "http://api.rottentomatoes.com/api/public/v1.0/lists/movies/box_office.json?page_limit=999&apikey=" + API_key
    req = urllib2.Request(URL)
    opener = urllib2.build_opener()
    f = opener.open(req)
    a = simplejson.load(f)['movies']
    for each in a:
        if each['id'] not in all_scraped:
            movie_IDs.append(each['id'])

    
   
    
    highest_scraped = 770672122 #max(all_scraped)

    while len(movie_IDs) < 500:
        highest_scraped = highest_scraped - 1
        print len(movie_IDs)
        if highest_scraped not in all_scraped:
            movie_IDs.append(highest_scraped)
    
    '''
lowest_movie_ID = scraperwiki.sqlite.select(           
        id from swdata order by id asc limit 1
    ) 
Nothing below ID 8937?
    for each in range(1,8000):
        if (int(lowest_movie_ID[0]['id'])-each) > 0:
            movie_IDs.append(int(lowest_movie_ID[0]['id'])-each)'''

    return movie_IDs

def get_movie(movie_ID, API_key):
    movie_data = {'id':'','title':'','year':'','mpaa_rating':'','genres':'','ratings':''}
    for each in movie_data:
        try:
            URL = "http://api.rottentomatoes.com/api/public/v1.0/movies/" + str(movie_ID) + ".json?apikey=" + API_key
            #URL = "http://api.rottentomatoes.com/api/public/v1.0/movie_alias.json?id=" + str(movie_ID) + "&type=imdb&apikey=" + API_key
            req = urllib2.Request(URL)
            opener = urllib2.build_opener()
            f = opener.open(req)
            movie_data[each] = simplejson.load(f)[each]
        except KeyError:
            print "ID not found: " + str(movie_ID)
        except urllib2.HTTPError:
            print "HTTPError"
    try:
        scraperwiki.sqlite.save(unique_keys=["id"], data={
        "id":movie_data['id'],
        "title":movie_data['title'],
        "year":movie_data['year'],
        "mpaa_rating":movie_data['mpaa_rating'],
        "genres":movie_data['genres'],
        "critics_score":dict(movie_data['ratings'])['critics_score'],
        "audience_score":dict(movie_data['ratings'])['audience_score']})   
    except KeyError:
        print "ID not found: " + str(movie_ID)

for each in get_IDs(API_key):
    if each not in movie_IDs:
        movie_IDs.append(each)

for each in movie_IDs:
    get_movie(each, API_key)