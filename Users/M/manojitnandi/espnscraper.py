import scraperwiki
import simplejson
import time

api_call='http://api.espn.com/v1/sports/news/headlines/top?apikey=w2kydft87jbyjxt6dtwvxade'
#api_call = 'http://api.espn.com/v1/sports/basketball/nba/athletes?apikey=w2kydft87jbyjxt6dtwvxade'
#api_call = 'http://api.espn.com/v1/sports/football/nfl/teams/34/news?apikey=w2kydft87jbyjxt6dtwvxade'


response = simplejson.loads(scraperwiki.scrape(api_call))
response = response['headlines']
for story in response:
    print story
    stor = story['story']
    desc = story['description']
    if story.has_key('title'):
        title = story['title']
    else:
        title = " "
    headline = story['headline']
    published = story['published']
    keywords = story['keywords']
    typ = story['type']
    id = story['id']
    data = {'story':stor, 'description':desc, 'title':title, 'headline':headline, 'published':published, 'keywords':keywords, 'type':typ, 'id':id}
    scraperwiki.sqlite.save(unique_keys=['id'], data = data)
time.sleep(2) 


import scraperwiki
import simplejson
import time

api_call='http://api.espn.com/v1/sports/news/headlines/top?apikey=w2kydft87jbyjxt6dtwvxade'
#api_call = 'http://api.espn.com/v1/sports/basketball/nba/athletes?apikey=w2kydft87jbyjxt6dtwvxade'
#api_call = 'http://api.espn.com/v1/sports/football/nfl/teams/34/news?apikey=w2kydft87jbyjxt6dtwvxade'


response = simplejson.loads(scraperwiki.scrape(api_call))
response = response['headlines']
for story in response:
    print story
    stor = story['story']
    desc = story['description']
    if story.has_key('title'):
        title = story['title']
    else:
        title = " "
    headline = story['headline']
    published = story['published']
    keywords = story['keywords']
    typ = story['type']
    id = story['id']
    data = {'story':stor, 'description':desc, 'title':title, 'headline':headline, 'published':published, 'keywords':keywords, 'type':typ, 'id':id}
    scraperwiki.sqlite.save(unique_keys=['id'], data = data)
time.sleep(2) 


