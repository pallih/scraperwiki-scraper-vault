import feedparser
import scrapemark
import scraperwiki

def get_feed(feed_url):
    print(feed_url)
    #feed = feedparser.parse("http://www.rigzone.com/news/rss/rigzone_latest.aspx")
    #feed = feedparser.parse("http://api.geonames.org/rssToGeoRSS?feedUrl=http://www.rigzone.com/news/rss/rigzone_latest.aspx&username=ngtait")
    feed = feedparser.parse("http://api.geonames.org/rssToGeoRSS?feedUrl=" + feed_url + "&username=ngtait")
    print(feed)
    entries = []
    entries.extend(feed["items"])
    idfld = 0    
    for entry in entries:
        idfld += 1
        # remove spaces from links
        entry["link"] = entry["link"].replace(" ", "")
        try:
            data = (
                {
                    "idfld" : idfld,
                    "title" : entry["title"],
                    "identifier" : entry["link"],
                    "modified" : entry["updated"],
                    "abstract" : entry["description"],
                    "latitude" : entry["geo_lat"],
                    "longitude" : entry["geo_long"],
                    "source" : ""    
                }
            )
            data2 = (
                {
                    "idfld" : idfld,
                    "source" : ""   
                    
                }
            )
        except:
            pass
        #print(3)
        #print(data['latitude'])
        print(data['identifier'])
        #geocode_text(data['abstract'])
        #scraperwiki.sqlite.save(unique_keys=['identifier'], data = data)


        #locations.append({'idfld':idfld,'name': name, 'country': country, 'latitude': latitude, 'longitude': longitude})


        scraperwiki.sqlite.save(unique_keys=["idfld"], data = data2)


token_dict = {
    "http://www.internationalrivers.org/rss" :get_feed
    #"rigzone" : get_rigzone_feed
    
}



def Main(): 
    # for key in token_dict.iterkeys():
    for key, value in token_dict.iteritems() :
        #print key, value    
        token_dict[key](key)
        #print(items())
        #print(token_dict[key]())
        #token_dict[key]()
    
    

Main()