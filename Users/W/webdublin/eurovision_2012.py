import scraperwiki
import lxml.html
import urllib   
import simplejson
import urllib2
import datetime
import operator
from operator import itemgetter, attrgetter



# Getting Eurovision 2012 Participants for other scraper
scraperwiki.sqlite.attach("eurovision_2013_-_participants")
participants = scraperwiki.sqlite.select("country, song, singer, 0 'mentions' from [eurovision_2013_-_participants].swdata")

#scraperwiki.sqlite.execute("delete from swdata")  
#print participants 

QUERY = '#eurovision'
#singer
GEOINFO = '53.26521293124656,-9.063720703125,257km'
RESULTS_PER_PAGE = '100'
PAGES = 20
TYPE = 'recent'
LANGUAGE = 'en'
results = 0
pos_singer = 0
pos_song = 0
pos_country = 0
rec_count = 0
total = 0
run_number = 1
runs = scraperwiki.sqlite.execute("select max(run_number)from swdata")
oldtime = scraperwiki.sqlite.execute("select timestamp from swdata order by run_number desc limit '1'")
print oldtime

x = runs['data'].pop()
run_number = x[0] + 1

run_time =  datetime.datetime.now()


for page in range(1, PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY.encode('utf_8')), RESULTS_PER_PAGE, LANGUAGE, page)

#for page in range(1, NUM_PAGES+1):
#base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s' \
#    % (urllib2.quote(QUERY.encode('utf_8')), RESULTS_PER_PAGE, LANGUAGE)
#base_url = 'http://search.twitter.com/search.json?q=%s&geocode=%s&rpp=%s&lang=%s' \
#         % (urllib2.quote(QUERY.encode('utf_8')), urllib2.quote(GEOINFO), RESULTS_PER_PAGE, LANGUAGE)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))            
        for result in results_json['results']:
            data = {}
            strText = ''.join(result['text'])
            total += 1
            for part in participants:
                country = part['country'] 
                song = part['song']
                singer = part['singer']
                pos_singer = strText.find(singer, 0, 140)
                pos_song = strText.find(song, 0, 140)
                pos_country = strText.find(country, 0, 140)
                #print pos_country
                if pos_song > 0:
                    part['mentions'] = part['mentions']+ 1
                    pos_song = 0  
                    pos_singer = 0          
                    pos_country = 0
                elif pos_singer > 0:
                    part['mentions'] = part['mentions']+ 1
                    pos_song = 0  
                    pos_singer = 0          
                    pos_country = 0
                elif pos_country > 0:
                    if country != 'Azerbaijan':
                        part['mentions'] = part['mentions']+ 1
                        pos_song = 0  
                        pos_singer = 0          
                        pos_country = 0
            #print singer + " - " + country + " - " + str(results)     
            
            #data['from_user'] = result['from_user']
            #print data['from_user'], data['text']
            #scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url

part_sorted = sorted(participants, key=itemgetter('mentions'), reverse=True)

#stack = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12]

for part in part_sorted:
    singer = part['singer']
    song = part['song']
    country = part['country']
    results = part['mentions']
#    if results > 0: 
#        if len(stack) > 0:
#            points = stack.pop()
    scraperwiki.sqlite.save(unique_keys=["country", "run_number"], data={"country":country, "singer":singer, "points":results, "run_number":run_number, "results":results, "timestamp":run_time})
    print country.encode('utf_8') + " - " + singer.encode('utf_8') + " - " + song.encode('utf_8')+ " - " + str(results)
            #scraperwiki.sqlite.save(unique_keys=["country"], data={"country":country, "points":points))
        #str(results)
#print rec_count
    
print total



import scraperwiki
import lxml.html
import urllib   
import simplejson
import urllib2
import datetime
import operator
from operator import itemgetter, attrgetter



# Getting Eurovision 2012 Participants for other scraper
scraperwiki.sqlite.attach("eurovision_2013_-_participants")
participants = scraperwiki.sqlite.select("country, song, singer, 0 'mentions' from [eurovision_2013_-_participants].swdata")

#scraperwiki.sqlite.execute("delete from swdata")  
#print participants 

QUERY = '#eurovision'
#singer
GEOINFO = '53.26521293124656,-9.063720703125,257km'
RESULTS_PER_PAGE = '100'
PAGES = 20
TYPE = 'recent'
LANGUAGE = 'en'
results = 0
pos_singer = 0
pos_song = 0
pos_country = 0
rec_count = 0
total = 0
run_number = 1
runs = scraperwiki.sqlite.execute("select max(run_number)from swdata")
oldtime = scraperwiki.sqlite.execute("select timestamp from swdata order by run_number desc limit '1'")
print oldtime

x = runs['data'].pop()
run_number = x[0] + 1

run_time =  datetime.datetime.now()


for page in range(1, PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY.encode('utf_8')), RESULTS_PER_PAGE, LANGUAGE, page)

#for page in range(1, NUM_PAGES+1):
#base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s' \
#    % (urllib2.quote(QUERY.encode('utf_8')), RESULTS_PER_PAGE, LANGUAGE)
#base_url = 'http://search.twitter.com/search.json?q=%s&geocode=%s&rpp=%s&lang=%s' \
#         % (urllib2.quote(QUERY.encode('utf_8')), urllib2.quote(GEOINFO), RESULTS_PER_PAGE, LANGUAGE)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))            
        for result in results_json['results']:
            data = {}
            strText = ''.join(result['text'])
            total += 1
            for part in participants:
                country = part['country'] 
                song = part['song']
                singer = part['singer']
                pos_singer = strText.find(singer, 0, 140)
                pos_song = strText.find(song, 0, 140)
                pos_country = strText.find(country, 0, 140)
                #print pos_country
                if pos_song > 0:
                    part['mentions'] = part['mentions']+ 1
                    pos_song = 0  
                    pos_singer = 0          
                    pos_country = 0
                elif pos_singer > 0:
                    part['mentions'] = part['mentions']+ 1
                    pos_song = 0  
                    pos_singer = 0          
                    pos_country = 0
                elif pos_country > 0:
                    if country != 'Azerbaijan':
                        part['mentions'] = part['mentions']+ 1
                        pos_song = 0  
                        pos_singer = 0          
                        pos_country = 0
            #print singer + " - " + country + " - " + str(results)     
            
            #data['from_user'] = result['from_user']
            #print data['from_user'], data['text']
            #scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url

part_sorted = sorted(participants, key=itemgetter('mentions'), reverse=True)

#stack = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12]

for part in part_sorted:
    singer = part['singer']
    song = part['song']
    country = part['country']
    results = part['mentions']
#    if results > 0: 
#        if len(stack) > 0:
#            points = stack.pop()
    scraperwiki.sqlite.save(unique_keys=["country", "run_number"], data={"country":country, "singer":singer, "points":results, "run_number":run_number, "results":results, "timestamp":run_time})
    print country.encode('utf_8') + " - " + singer.encode('utf_8') + " - " + song.encode('utf_8')+ " - " + str(results)
            #scraperwiki.sqlite.save(unique_keys=["country"], data={"country":country, "points":points))
        #str(results)
#print rec_count
    
print total



