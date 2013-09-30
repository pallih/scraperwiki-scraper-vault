import scraperwiki
import urllib
import demjson
import re
import pickle
import requests


def parse_artists(artist_list):
    # Format is a; or a & b; or a, b & c
    artist_list = re.split(",? & |, | and ", artist_list)
    return artist_list

def parse_artists_from_title(title):
    # Format is foo (feat. [artist_list])
    regexp = 'feat\.[^)\]]+'
    result = re.search(regexp, title, re.I)
    if result:
        result = result.group(0) # Should only be one
        result = result[6:] # get rid of feat.
        return parse_artists(result)
    return []

def get_collaborators_from_json(search_json, artistName):
    collaborators = set ()
    for result in search_json['results']:
        #print result['trackName']
        artists = set(parse_artists(result['artistName']))
        
        artists.update(parse_artists_from_title(result['trackName']))
        
        #print title_artists
        #print artistName, artists, result['trackName']
        if artistName in artists:
            collaborators.update(artists)
    return collaborators
        
def get_json(params):
    r = requests.get('http://itunes.apple.com/search', params=params)
    return r.text
def get_collaborators(artistName):
   
    collaborators = set ()
    #artistNameQuoted = artistName.replace(" ","+")
    #artistNameQuoted = urllib.quote_plus(artistName)
   
    # Search in the artist field
    #scrape_url = "http://itunes.apple.com/search?term=%s&limit=5000&entity=song&attribute=artistTerm" % artistNameQuoted
    params = {'term' : artistName, 'limit' : 5000, 'entity' : 'song', 'attribute' : 'artistTerm' }
    search_json = demjson.decode(get_json(params))
    
    collaborators.update(get_collaborators_from_json(search_json, artistName))

    # Search in the title field (will fail for artists whose names also appear as unrelated song titles...) 
    #scrape_url = "http://itunes.apple.com/search?term=%s&limit=5000&entity=song&attribute=songTerm" % artistNameQuoted
    params = {'term' : artistName, 'limit' : 5000, 'entity' : 'song', 'attribute' : 'songTerm' }
    search_json = demjson.decode(get_json(params))
    #print search_json
    
    collaborators.update(get_collaborators_from_json(search_json, artistName))
    
    for collaborator in collaborators:
        
        data = {'artist' : artistName, 'collaborator' : collaborator }
        scraperwiki.sqlite.save(unique_keys=['artist', 'collaborator'], data=data)
    return collaborators  
# Blank Python

for collaborator in get_collaborators(u'David Byrne'):
    print collaborator 
    
    if scraperwiki.sqlite.select("* from swdata where artist=? limit 1", [collaborator]):
        continue
    get_collaborators(collaborator)



import scraperwiki
import urllib
import demjson
import re
import pickle
import requests


def parse_artists(artist_list):
    # Format is a; or a & b; or a, b & c
    artist_list = re.split(",? & |, | and ", artist_list)
    return artist_list

def parse_artists_from_title(title):
    # Format is foo (feat. [artist_list])
    regexp = 'feat\.[^)\]]+'
    result = re.search(regexp, title, re.I)
    if result:
        result = result.group(0) # Should only be one
        result = result[6:] # get rid of feat.
        return parse_artists(result)
    return []

def get_collaborators_from_json(search_json, artistName):
    collaborators = set ()
    for result in search_json['results']:
        #print result['trackName']
        artists = set(parse_artists(result['artistName']))
        
        artists.update(parse_artists_from_title(result['trackName']))
        
        #print title_artists
        #print artistName, artists, result['trackName']
        if artistName in artists:
            collaborators.update(artists)
    return collaborators
        
def get_json(params):
    r = requests.get('http://itunes.apple.com/search', params=params)
    return r.text
def get_collaborators(artistName):
   
    collaborators = set ()
    #artistNameQuoted = artistName.replace(" ","+")
    #artistNameQuoted = urllib.quote_plus(artistName)
   
    # Search in the artist field
    #scrape_url = "http://itunes.apple.com/search?term=%s&limit=5000&entity=song&attribute=artistTerm" % artistNameQuoted
    params = {'term' : artistName, 'limit' : 5000, 'entity' : 'song', 'attribute' : 'artistTerm' }
    search_json = demjson.decode(get_json(params))
    
    collaborators.update(get_collaborators_from_json(search_json, artistName))

    # Search in the title field (will fail for artists whose names also appear as unrelated song titles...) 
    #scrape_url = "http://itunes.apple.com/search?term=%s&limit=5000&entity=song&attribute=songTerm" % artistNameQuoted
    params = {'term' : artistName, 'limit' : 5000, 'entity' : 'song', 'attribute' : 'songTerm' }
    search_json = demjson.decode(get_json(params))
    #print search_json
    
    collaborators.update(get_collaborators_from_json(search_json, artistName))
    
    for collaborator in collaborators:
        
        data = {'artist' : artistName, 'collaborator' : collaborator }
        scraperwiki.sqlite.save(unique_keys=['artist', 'collaborator'], data=data)
    return collaborators  
# Blank Python

for collaborator in get_collaborators(u'David Byrne'):
    print collaborator 
    
    if scraperwiki.sqlite.select("* from swdata where artist=? limit 1", [collaborator]):
        continue
    get_collaborators(collaborator)



