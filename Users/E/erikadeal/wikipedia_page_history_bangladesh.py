import scraperwiki
import lxml.etree
import urllib

#Print out the content returned by the API; helps with debuggung
url = urllib.urlopen("http://bn.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=২০১৩_সাভার_ভবন_ধস&rvprop=timestamp|user|comment&rvlimit=500").read()

print url

#Fetch the URL to be read by an XML parser with the appropriate parameters set and separated by an ampersand:
#Format = XML
#Action = Query
#Prop = fetching the article property "revisions"
#Titles = The title of the article we want to query. I think you can only do multiples when you are NOT using the XML parser, though
#Rvprop = The specific revision properties that we want to fetch, separated by vertical dividers
#Rvlimit = Necessary declaration if we want to retrieve more than the latest revision

url = "http://bn.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=২০১৩_সাভার_ভবন_ধস&rvprop=timestamp|user|comment&rvlimit=500"

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

    #print user, time, content
    
    #print the content of the variables
    #print user, " : ", time, " : ", content 
    
    #store the user name in a list so that it can be counted in the next step
    users.append(user)
    
    try:
        location = urllib.urlopen('http://api.hostip.info/get_json.php?ip=' + user + '&position=true').read()

        data = {"user": user, "time" : time, "content" : content, "location" : location}
        scraperwiki.sqlite.save(unique_keys=["user"], data=data) 
    except UnicodeError:
        print "Registered User"

#import library for counting list items
from collections import Counter

#Count identical items in the list
count = Counter(users)

#Print list of how many revisions were made by each unique user
print count