import scraperwiki
import simplejson as json
from urllib import quote

#DAVE_CHANNEL_ID = "cbRF" # production
DAVE_CHANNEL_ID = "cdPd"
STATION_URI = "http://ref.atlasapi.org/channels/pressassociation.com/stations/609"

scraperwiki.sqlite.attach("dave_schedule_scraper")
scraperwiki.utils.httpresponseheader("Content-Type", "text/json")
output = {}
brands = []
brandContent = {}
brandRewrite = {}

publisher = {
    'key': 'scraperwiki.com',
    'name': 'ScraperWiki',
    'country': 'ALL'
}

# Not sure what to map entertainment to
daveGenreMap = {
   "http://video.uktv.co.uk/dave/programmes/by-genre/comedy": "http://ref.atlasapi.org/genres/atlas/comedy",
   "http://video.uktv.co.uk/dave/programmes/by-genre/entertainment": "http://ref.atlasapi.org/genres/atlas/comedy"
}

def toBoolean(value):
    return value == "1"

def extractBasicData(row):
    content = {}
    content["title"] = row["title"]
    content["description"] = row["description"]
    content["media_type"] = "video"
    if row["image"] != None:
        content["image"] = row["image"]
    content["uri"] = row["uri"]
    content["type"] = row["type"]
    content["publisher"] = publisher
    if row.has_key("genre"):
        content["genres"] = [daveGenreMap[row["genre"]]]
        content["genres"].append(row["genre"])
    if row["type"] == 'episode': 
        content["container"] = {"uri": row["container"]}  
    if row["type"] == "broadcast":
        if row["container"] in brandRewrite:
            content["container"] = {"uri": brandRewrite[row["container"]]} 
        else:
            content["container"] = {"uri": row["container"]} 
    return content

def generateBrandUri(uri, slug):
    newUri = "http://video.uktv.co.uk/dave/" + slug
    brandRewrite[uri] = newUri
    return newUri

def appendBrands(contents):
    data = scraperwiki.sqlite.select(           
        '''* from swdata
        where type='brand'
        order by type'''
    )
    for row in data:
        brand = extractBasicData(row)
        # Override brnad uri if brand slug present
        if row["brand-slug"] is not None:
            brand["uri"] = generateBrandUri(row["uri"], row["brand-slug"])
        contents.append(brand) 
    return contents 
    

def appendEpisodes(contents):
    data = scraperwiki.sqlite.select(           
        '''* from swdata 
        where type = 'episode'
        order by type'''
    )
    for row in data:
        content = extractBasicData(row)
        content["series_number"] = row["series_number"]
        content["episode_number"] = row["episode_number"]
        location = {
             "transport_type": "link",
             "uri" : row["uri"],
             "available": True
        }
        content["locations"] = [location]
        content["specialization"] = "tv"
        contents.append(content)
    return contents

def appendBroadcasts(contents):
    data = scraperwiki.sqlite.select(           
        '''* from swdata 
        where type = 'broadcast'
        order by type'''
    )
    for row in data:
        # image` text, `description` text, `type` text, `uri` text, `title` text, `audioDescribed` text, `container` text, `subtitled` text, `start` text, `duration` integer, `end` text, `channel` text
        content = extractBasicData(row)
        broadcast = {}
        broadcast["transmission_time"] = row["start"]
        broadcast["transmission_end_time"] = row["end"]
        broadcast["broadcast_duration"] = row["duration"]
        broadcast["broadcast_on"] = STATION_URI
        broadcast["id"] = row["uri"] #: "bbc:p016lg6f"
        #broadcast["repeat"] = # : false
        #broadcast["signed"] = # : false
        broadcast["subtitled"] = toBoolean(row["subtitled"])
        broadcast["audio_described"] = toBoolean(row["audioDescribed"])
        channel = {}
        #channel: {
        #aliases: [ ],
        #id: "cbbn"
        #},
        channel["id"] = DAVE_CHANNEL_ID
        broadcast["channel"] = channel
        #channel["aliases"] =  [ ]
        broadcast["duration"] = row["duration"]
        broadcast["published_duration"] = row["duration"]
        restriction = {}
        broadcast["restriction"] = restriction
        content["broadcasts"] = [broadcast]
        content["type"] = "episode"
        contents.append(content)
    return contents
 
contents = []
contents = appendBrands(contents)
contents = appendEpisodes(contents) 
contents = appendBroadcasts(contents)  
output["contents"] = contents
print json.dumps(output)


