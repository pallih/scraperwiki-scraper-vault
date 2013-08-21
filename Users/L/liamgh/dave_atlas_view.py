import scraperwiki
import simplejson as json
from urllib import quote

scraperwiki.sqlite.attach("dave_on_demand_scraper")
scraperwiki.utils.httpresponseheader("Content-Type", "text/json")
output = {}
brands = []
brandContent = {}
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

def extractBasicData(row):
    content = {}
    content["title"] = row["title"]
    content["description"] = row["description"]
    content["media_type"] = "video"
    content["image"] = row["image"]
    content["uri"] = row["uri"]
    content["type"] = row["type"]
    content["publisher"] = publisher
    if row["genre"]:
        content["genres"] = [daveGenreMap[row["genre"]]]
        content["genres"].append(row["genre"])
    if row["type"] == 'episode':
        content["container"] = {"uri": row["container"]}  
    return content

def appendBrands(contents):
    data = scraperwiki.sqlite.select(           
        '''* from swdata
        where type='brand'
        order by type'''
    )
    for row in data:
        brand = extractBasicData(row)
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

 
contents = []
contents = appendBrands(contents)
contents = appendEpisodes(contents)    
output["contents"] = contents
print json.dumps(output)

