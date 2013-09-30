import scraperwiki
import lxml.etree
import urllib

#Print out the content returned by the API; helps with debuggung
url = urllib.urlopen("http://fr.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=Effondrement_d%27un_immeuble_à_Savar_en_2013&rvprop=timestamp|user|comment&rvlimit=500").read()

print url

#Fetch the URL to be read by an XML parser with the appropriate parameters set and separated by an ampersand:
#Format = XML
#Action = Query
#Prop = fetching the article property "revisions"
#Titles = The title of the article we want to query. I think you can only do multiples when you are NOT using the XML parser, though
#Rvprop = The specific revision properties that we want to fetch, separated by vertical dividers
#Rvlimit = Necessary declaration if we want to retrieve more than the latest revision

url = "http://fr.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=Effondrement_d%27un_immeuble_à_Savar_en_2013&rvprop=timestamp|user|comment&rvlimit=500"

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

    print user, time
    
    #print the content of the variables
    #print user, " : ", time, " : ", content 
    
    #store the user name in a list so that it can be counted in the next step
    users.append(user)

    location = urllib.urlopen('http://api.hostip.info/get_json.php?ip=' + user + '&position=true').read()

    try:
        data = {"user": user, "time" : time, "content" : content, "location" : location}
        scraperwiki.sqlite.save(unique_keys=["user"], data=data) 
    except:
        print "error"

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
url = urllib.urlopen("http://fr.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=Effondrement_d%27un_immeuble_à_Savar_en_2013&rvprop=timestamp|user|comment&rvlimit=500").read()

print url

#Fetch the URL to be read by an XML parser with the appropriate parameters set and separated by an ampersand:
#Format = XML
#Action = Query
#Prop = fetching the article property "revisions"
#Titles = The title of the article we want to query. I think you can only do multiples when you are NOT using the XML parser, though
#Rvprop = The specific revision properties that we want to fetch, separated by vertical dividers
#Rvlimit = Necessary declaration if we want to retrieve more than the latest revision

url = "http://fr.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=Effondrement_d%27un_immeuble_à_Savar_en_2013&rvprop=timestamp|user|comment&rvlimit=500"

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

    print user, time
    
    #print the content of the variables
    #print user, " : ", time, " : ", content 
    
    #store the user name in a list so that it can be counted in the next step
    users.append(user)

    location = urllib.urlopen('http://api.hostip.info/get_json.php?ip=' + user + '&position=true').read()

    try:
        data = {"user": user, "time" : time, "content" : content, "location" : location}
        scraperwiki.sqlite.save(unique_keys=["user"], data=data) 
    except:
        print "error"

#import library for counting list items
from collections import Counter

#Count identical items in the list
count = Counter(users)

#Print list of how many revisions were made by each unique user
print count



