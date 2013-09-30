import feedparser
import scrapemark
import scraperwiki

def get_rigzone_feed():
    #feed = feedparser.parse("http://www.rigzone.com/news/rss/rigzone_latest.aspx")
    feed = feedparser.parse("http://api.geonames.org/rssToGeoRSS?feedUrl=http://www.rigzone.com/news/rss/rigzone_latest.aspx&username=ngtait")
    print(feed)
    entries = []
    entries.extend(feed["items"])
    for entry in entries:
        # remove spaces from links
        entry["link"] = entry["link"].replace(" ", "")
        try:
            data = (
                {
                    "title" : entry["title"],
                    "identifier" : entry["link"],
                    "modified" : entry["updated"],
                    "abstract" : entry["description"],
                    "latitude" : entry["geo_lat"],
                    "longitude" : entry["geo_long"],
                    "source" : "http://www.rigzone.com/"    
                }
            )
        except:
            pass
        #print(3)
        #print(data['latitude'])
        #geocode_text(data['abstract'])
        scraperwiki.sqlite.save(unique_keys=['identifier'], data = data)


token_dict = {
    "rigzone" : get_rigzone_feed
    
}



def Main():
    for key in token_dict.iterkeys():
        token_dict[key]()
    
    

Main()import feedparser
import scrapemark
import scraperwiki

def get_rigzone_feed():
    #feed = feedparser.parse("http://www.rigzone.com/news/rss/rigzone_latest.aspx")
    feed = feedparser.parse("http://api.geonames.org/rssToGeoRSS?feedUrl=http://www.rigzone.com/news/rss/rigzone_latest.aspx&username=ngtait")
    print(feed)
    entries = []
    entries.extend(feed["items"])
    for entry in entries:
        # remove spaces from links
        entry["link"] = entry["link"].replace(" ", "")
        try:
            data = (
                {
                    "title" : entry["title"],
                    "identifier" : entry["link"],
                    "modified" : entry["updated"],
                    "abstract" : entry["description"],
                    "latitude" : entry["geo_lat"],
                    "longitude" : entry["geo_long"],
                    "source" : "http://www.rigzone.com/"    
                }
            )
        except:
            pass
        #print(3)
        #print(data['latitude'])
        #geocode_text(data['abstract'])
        scraperwiki.sqlite.save(unique_keys=['identifier'], data = data)


token_dict = {
    "rigzone" : get_rigzone_feed
    
}



def Main():
    for key in token_dict.iterkeys():
        token_dict[key]()
    
    

Main()