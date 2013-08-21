#!/usr/bin/env python
from urllib2 import urlopen
#from urllib import UnicodeEncodeError
from json import loads
from scraperwiki.sqlite import save,select,show_tables
import re

#These are words and other strings without spaces that appear before the geographical location in the tweet
BEFORE_LOCATION=(
  'in'
, 'infront'
, 'around'
, 'at'
, 'by'
, 'from'
)

#These are words and other strings, possibly with spaces, that appear after the geographical location in the tweet
AFTER_LOCATION=(
  '?'
#, '#'
, ','
, '.'
)

from geopy import geocoders
G = geocoders.Google('http://www.google.com.eg/')

def get(count=10,page=1):
  """Get the most recent statuses and load the json"""
  url='https://api.twitter.com/1/statuses/user_timeline.json?include_entities=true&include_rts=true&screen_name=TahrirSupplies&count=%d&page=%d' % (count,page)
  return loads(urlopen(url).read())

class Tweet():
  def __init__(this,tweet_dict):
    this._tweet=tweet_dict

  def save(this):
    """Save a tweet to the datastore if it isn't there already"""
    save(['id'],this._tweet,'tweets')

  def is_new(this):
    """Check whether I've already saved it"""
    if 'tweets' not in show_tables():
      return True
    else:
      return 0==select('count(*) as c from tweets where id="%s"' % this._tweet['id'])[0]['c']

  def extract_location(this):
    #return re.sub(r'Sandra([^#]+)[#,.]',r'\\1',this._tweet['text'])
    #return re.sub(r' in ([^#]+)',r'\\1',this._tweet['text'])
    tokens=this._tweet['text'].split(' ')

    locstarts=[] #Where might the location start?
    for b in BEFORE_LOCATION:
      if b in tokens:
        locstarts.append(tokens.index(b)+1)

    #Location strings
    locations=[]
    for locstart in locstarts:
      #Go until the end of the tweet for now
      locend=len(tokens)
      loc_tokens=tokens[locstart:locend]
      location=' '.join(loc_tokens)
      locations.append(location)

    #Remove things after the AFTER_LOCATION
    for a in AFTER_LOCATION:
      locations=[loc.split(a)[0] for loc in locations]

    this.locations=locations

  def geocode(this):
    this.extract_location()
    for location in this.locations:
      try:
        locs_geo=G.geocode(location,exactly_one=False)
      except geocoders.google.GQueryError:
        pass
      except:
        #You didn't see anything
        pass
      else:
        exact=len(locs_geo)==1
        if not exact:
          indices=range(len(locs_geo))
          indices.reverse()
          for i in indices:
            #print 'Skipping %s' % locs_geo[i][0]
            if 'Egypt' not in locs_geo[i][0]:
              locs_geo.pop(i)
        for loc in locs_geo:
          location_geo,(latitude,longitude)=loc
          save([],{
            "tweet_id":this._tweet['id']
          , "place_raw":location
          , "place_geo":location_geo
          , "latitude":latitude
          , "longitude":longitude
          , "exact":exact
          },'geocode')


def backlog_grab():
  for p in range(1,35):
    tweet_dicts=get(count=50,page=p)
    save(['id'],tweet_dicts,'tweets')

def backlog_geocode():
  for t in [Tweet(d) for d in select('* from tweets where id not in (select tweet_id from `geocode`)')]:
    t.geocode()

def main():
  tweet_dicts=get(5)
  save(['id'],tweet_dicts,'tweets')
  tweets=[Tweet(tweet_dict) for tweet_dict in tweet_dicts]
  for t in tweets:
    t.geocode()

#main()
backlog_grab()
backlog_geocode()

#Drop the geocode table. (Use this if the geocoding totally changes and I need to get rid of old stuff.
#execute('drop table "geocode"')