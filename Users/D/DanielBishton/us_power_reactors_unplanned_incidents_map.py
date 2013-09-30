import scraperwiki
import gdata.docs.data
import gdata.docs.client
import gdata.acl.data
import urllib2
import xmllib
import feedparser

# Open RSS2 feed of unplanned incidents at US reactors
feed = urllib2.urlopen('https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=rss2&name=us_nuclear_reactor_rss&query=select%20*%20from%20%60swdata%60%20order%20by%20date%20desc',None)

# Parse feed into list
data = feedparser.parse(feed)

# Loop through list of items to extract title, description, date and link
for x in data.entries:
    print x.title
    print x.description
    print x.date
    print x.link
    print x.guid
    


# INSERT INTO <table_id> (<column_name> {, <column_name>}*) VALUES (<value> {, <value>}*)
#{ {;INSERT INTO <table_id> (<column_name> {, <column_name>}*) VALUES (<value> {, <value>}*)}* ;}

# Call an opener to initiate a HTTP Put method 
opener = urllib2.build_opener(urllib2.HTTPHandler)

# Request Google Fusion Tables API and insert statement
request = urllib2.Request('http://www.google.com/fusiontables/api/query?sql=INSERT%20INTO%202339839%20(Title)%20VALUES%20(HEREIAMNOW)')

# Add header and encoding type
request.add_header("text/html", "utf-8")

# Define HTTP Put method
request.get_method = lambda: 'PUT'
url = opener.open(request)import scraperwiki
import gdata.docs.data
import gdata.docs.client
import gdata.acl.data
import urllib2
import xmllib
import feedparser

# Open RSS2 feed of unplanned incidents at US reactors
feed = urllib2.urlopen('https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=rss2&name=us_nuclear_reactor_rss&query=select%20*%20from%20%60swdata%60%20order%20by%20date%20desc',None)

# Parse feed into list
data = feedparser.parse(feed)

# Loop through list of items to extract title, description, date and link
for x in data.entries:
    print x.title
    print x.description
    print x.date
    print x.link
    print x.guid
    


# INSERT INTO <table_id> (<column_name> {, <column_name>}*) VALUES (<value> {, <value>}*)
#{ {;INSERT INTO <table_id> (<column_name> {, <column_name>}*) VALUES (<value> {, <value>}*)}* ;}

# Call an opener to initiate a HTTP Put method 
opener = urllib2.build_opener(urllib2.HTTPHandler)

# Request Google Fusion Tables API and insert statement
request = urllib2.Request('http://www.google.com/fusiontables/api/query?sql=INSERT%20INTO%202339839%20(Title)%20VALUES%20(HEREIAMNOW)')

# Add header and encoding type
request.add_header("text/html", "utf-8")

# Define HTTP Put method
request.get_method = lambda: 'PUT'
url = opener.open(request)