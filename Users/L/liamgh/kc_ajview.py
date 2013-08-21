import scraperwiki
import simplejson as json
from urllib import quote

scraperwiki.sqlite.attach("koldcast_scraper")
scraperwiki.utils.httpresponseheader("Content-Type", "text/json")
output = {}
brands = []
brandContent = {}
publisher = {
    'key': 'scraperwiki.com',
    'name': 'ScraperWiki',
    'country': 'ALL'
}

kcGenreMap = {
   "Action": "http://ref.atlasapi.org/genres/atlas/drama",
   "Animation": "http://ref.atlasapi.org/genres/atlas/animation",
   "Comedy": "http://ref.atlasapi.org/genres/atlas/comedy",
   "Drama": "http://ref.atlasapi.org/genres/atlas/drama",
   "Fantasy": "http://ref.atlasapi.org/genres/atlas/drama",
   "Food & Cooking": "http://ref.atlasapi.org/genres/atlas/lifestyle",
   "Horror": "http://ref.atlasapi.org/genres/atlas/drama",
   "Kids": "http://ref.atlasapi.org/genres/atlas/childrens",
   "Lifestyle": "http://ref.atlasapi.org/genres/atlas/lifestyle",
   "Musical": "http://ref.atlasapi.org/genres/atlas/music",
   "Mystery" : "http://ref.atlasapi.org/genres/atlas/drama",
   "News & Politics": "http://ref.atlasapi.org/genres/atlas/factual",
   "Sci-Fi": "http://ref.atlasapi.org/genres/atlas/drama",
   "Science & Technology": "http://ref.atlasapi.org/genres/atlas/factual",
   "Soaps": "http://ref.atlasapi.org/genres/atlas/drama",
   "Teen": "http://ref.atlasapi.org/genres/atlas/drama"
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
        content["genres"] = [kcGenreMap[row["genre"]]]
        content["genres"].append("http://www.koldcast.tv/browse/" + quote(row["genre"]))
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
