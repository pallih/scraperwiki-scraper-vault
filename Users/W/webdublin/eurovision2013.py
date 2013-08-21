import scraperwiki
import lxml.html
import urllib   
import simplejson
import urllib2
import datetime
import time
import operator
from operator import itemgetter, attrgetter



# Getting Eurovision 2012 Participants for other scraper
scraperwiki.sqlite.attach("eurovision_2013_-_participants")
participants = scraperwiki.sqlite.select("country, song, singer, 0 'mentions', semi from [eurovision_2013_-_participants].swdata")
#runs = 45
#i = 1
#for part in participants:
#    for i in range(45):
#        scraperwiki.sqlite.save(unique_keys=["country", "run_number"], data={"country":part["country"], "run_number" : i,"song":part["song"], "semi":part["semi"]})

#print "Updated Semis"

#scraperwiki.sqlite.execute("delete from swdata")  
#print participants 

QUERY = '#eurovision'
#singer
GEOINFO = '53.26521293124656,-9.063720703125,257km'
RESULTS_PER_PAGE = '100'
PAGES = 14
TYPE = 'recent'
LANGUAGE = 'en'
results = 0
pos_singer = 0
pos_song = 0
pos_country = 0
rec_count = 0
total = 0
semi = 0
fails = 0

run_number = 1
runs = scraperwiki.sqlite.execute("select max(run_number)from swdata")
#print runs

x = runs['data'].pop()
run_number = x[0] + 1


run_time =  datetime.datetime.now()

#base_url = "https://api.twitter.com/1.1/search/tweets.json?q=%23freebandnames&since_id=24012619984051000&max_id=250126199840518145&result_type=mixed&count=4"

for page in range(1, PAGES+1):
    #base_url = ''
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY.encode('utf_8')), RESULTS_PER_PAGE, LANGUAGE, page)
    
    time.sleep(5)

    #print base_url 
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))     
        for result in results_json['results']:
            data = {}
            strText = ''.join(result['text'])
            total += 1
            for part in participants:
                country = part['country'] 
                song = part['song']
                song = song.lstrip()
                singer = part['singer']
                semi = part['semi']
                #print semi
                pos_singer = strText.find(singer, 0, 140)
                pos_song = strText.find(song, 0, 140)
                pos_country = strText.find(country, 0, 140)
                
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
                    if country != 'Sweden':
                        part['mentions'] = part['mentions']+ 1
                        pos_song = 0  
                        pos_singer = 0          
                        pos_country = 0
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        fails = fails + 1

part_sorted = sorted(participants, key=itemgetter('mentions'), reverse=True)

#stack = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12]
if fails < 10:
    for part in part_sorted:
        singer = part['singer']
        song = part['song']
        country = part['country']
        results = part['mentions']
        scraperwiki.sqlite.save(unique_keys=["country", "run_number"], data={"country":country, "singer":singer, "points":results, "run_number":run_number, "results":results, "song":song, "timestamp":run_time, "semi":semi})
        print country.encode('utf_8') + " - " + singer.encode('utf_8') + " - " + song.encode('utf_8')+ " - " + str(results)
    



