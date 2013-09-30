import scraperwiki
import lxml.etree
import urllib

#Print out the content returned by the API; helps with debuggung
url = urllib.urlopen("http://en.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=2013_Savar_building_collapse&rvprop=timestamp|user|comment&rvlimit=500").read()

print url

#Fetch the URL to be read by an XML parser with the appropriate parameters set and separated by an ampersand:
#Format = XML
#Action = Query
#Prop = fetching the article property "revisions"
#Titles = The title of the article we want to query. I think you can only do multiples when you are NOT using the XML parser, though
#Rvprop = The specific revision properties that we want to fetch, separated by vertical dividers
#Rvlimit = Necessary declaration if we want to retrieve more than the latest revision

url = "http://en.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=2013_Savar_building_collapse&rvprop=timestamp|user|comment&rvlimit=500"

#Parse the url as xml

article = lxml.etree.parse(urllib.urlopen(url))

#Use XPath to select the element we want to look at

revs = article.xpath('//rev')

#Make an empty list for counting purposes
users = []


#Iterate over <rev> elements, get the value of the attributes, and store them in variables
for rev in revs:
    user = rev.get('user')
    time = rev.get('timestamp')
    content = rev.get('comment')
    
    #print the content of the variables
    #print user, " : ", time, " : ", content 
    
    #store the user name in a list so that it can be counted in the next step
    users.append(user)

    # location of a wiki editor's IP address returned by the hostip API:
    location = urllib.urlopen('http://api.hostip.info/get_json.php?ip=' + user + '&position=true').read()
    
    # Select only the latitude and longitude from the location string:
    indexLat = location.find("lat")
    
    info = location[indexLat + 5:]

    indexComma = info.find(",")
    indexCurly = info.find("}")
    
    # Format lat properly:
    lat = info[0:indexComma]
    lat = lat.strip('"')

    # Setting null values to 0:
    null = lat.find("null")
    if null == 0:
        lat = 0

    # Format lng properly:
    lng = info[indexComma + 7:indexCurly]
    lng = lng.strip('"')

    # Setting null values to 0:
    null = lng.find("null")
    if null == 0:
        lng = 0

    #if 'Private' in location == True:
        #lat = "wikiUser"
        #lng = "wikiUser"

    #else:
        #print locationString

        #lat = locationList[4].lstrip('"lat":')
        #lng = locationList[5].lstrip('"lng"').rstrip('"}')

    data = {"user": user, "time" : time, "content" : content, "lat" : lat, "long" : lng}
    scraperwiki.sqlite.save(unique_keys=["user"], data=data) 

#import library for counting list items
from collections import Counter

#Count identical items in the list
count = Counter(users)

#Print list of how many revisions were made by each unique user
print count



import scraperwiki
import lxml.etree
import urllib

#Print out the content returned by the API; helps with debuggung
url = urllib.urlopen("http://en.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=2013_Savar_building_collapse&rvprop=timestamp|user|comment&rvlimit=500").read()

print url

#Fetch the URL to be read by an XML parser with the appropriate parameters set and separated by an ampersand:
#Format = XML
#Action = Query
#Prop = fetching the article property "revisions"
#Titles = The title of the article we want to query. I think you can only do multiples when you are NOT using the XML parser, though
#Rvprop = The specific revision properties that we want to fetch, separated by vertical dividers
#Rvlimit = Necessary declaration if we want to retrieve more than the latest revision

url = "http://en.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=2013_Savar_building_collapse&rvprop=timestamp|user|comment&rvlimit=500"

#Parse the url as xml

article = lxml.etree.parse(urllib.urlopen(url))

#Use XPath to select the element we want to look at

revs = article.xpath('//rev')

#Make an empty list for counting purposes
users = []


#Iterate over <rev> elements, get the value of the attributes, and store them in variables
for rev in revs:
    user = rev.get('user')
    time = rev.get('timestamp')
    content = rev.get('comment')
    
    #print the content of the variables
    #print user, " : ", time, " : ", content 
    
    #store the user name in a list so that it can be counted in the next step
    users.append(user)

    # location of a wiki editor's IP address returned by the hostip API:
    location = urllib.urlopen('http://api.hostip.info/get_json.php?ip=' + user + '&position=true').read()
    
    # Select only the latitude and longitude from the location string:
    indexLat = location.find("lat")
    
    info = location[indexLat + 5:]

    indexComma = info.find(",")
    indexCurly = info.find("}")
    
    # Format lat properly:
    lat = info[0:indexComma]
    lat = lat.strip('"')

    # Setting null values to 0:
    null = lat.find("null")
    if null == 0:
        lat = 0

    # Format lng properly:
    lng = info[indexComma + 7:indexCurly]
    lng = lng.strip('"')

    # Setting null values to 0:
    null = lng.find("null")
    if null == 0:
        lng = 0

    #if 'Private' in location == True:
        #lat = "wikiUser"
        #lng = "wikiUser"

    #else:
        #print locationString

        #lat = locationList[4].lstrip('"lat":')
        #lng = locationList[5].lstrip('"lng"').rstrip('"}')

    data = {"user": user, "time" : time, "content" : content, "lat" : lat, "long" : lng}
    scraperwiki.sqlite.save(unique_keys=["user"], data=data) 

#import library for counting list items
from collections import Counter

#Count identical items in the list
count = Counter(users)

#Print list of how many revisions were made by each unique user
print count



