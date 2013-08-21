import scraperwiki, urllib, simplejson


def replaces(_str):
    if len(_str)>0:
        _str = _str.replace(",","");
    return _str

usernames = [
             "alexpettitt",
            ]

#usernames = [
#             "alexpettitt"
#            ]

urlyql = "http://query.yahooapis.com/v1/public/yql?q=select%20content%20from%20html%20where%20url%3D%22http%3A%2F%2Ftwitter.com%2F#username#%22%20and%20(xpath%3D'%2F%2F*%2Fspan%5B%40class%3D%22stat_count%22%5D'%20or%20xpath%3D'%2F%2F*%2Fspan%5B%40class%3D%22stats_count%20numeric%22%5D')&format=json&callback="

for x in usernames:
    
    result = simplejson.load(urllib.urlopen(urlyql.replace("#username#",x)))
    
    if result["query"] and result["query"]["results"] and result["query"]["results"]["span"]:
        dades = result["query"]["results"]["span"]
        scraperwiki.datastore.save(unique_keys=["username"],data={"username":x, "tweets":replaces(dades[0]),"following":replaces(dades[1]), "followers":replaces(dades[2]),"listed":replaces(dades[3])}) 
 


