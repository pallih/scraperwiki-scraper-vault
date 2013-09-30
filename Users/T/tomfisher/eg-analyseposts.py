import scraperwiki
import lxml.html
import lxml.etree
import collections
import time 
import string
import re
from datetime import datetime
#import datetime
import time
import operator

#attach the database. db is a list. each list item is a dict containing one topic (date, link, posts etc)
scraperwiki.sqlite.attach("eg-getposts", "src")
test = scraperwiki.sqlite.select("* from src.swdata limit 10")

#attach local db
localdb = scraperwiki.sqlite.select("* from swdata limit 2500")


#sort database
localdb = sorted(localdb, key=operator.itemgetter('date'))


#print various stuff for testing
#print len(test)
#print test
#print type(test)
#print type(test[0])
#print test[0]

"""


for topic in localdb:
    #print type(topic)
    #print topic
    print topic['date']


    

for key in test[0].keys():
    print "key is | " + str(key) + " int is: | " + str(int) + " | value is " #+ str(test[int])
    print key
    int = int + 1
"""

print "Welcome to post analysis program..."

global superstring
superstring = ""
global count
count = 0



def get_data_combined_posts():
    count = 0

    for eachtopic in test:
        #now have a dict called eachtopic which contains one topic only (link, date, post number 1;2;3 etc)
        print "Now working on number " + str(count) + " of " + str(len(test)) #status update
        superstring = "" #clear the superstring at start of this topic
        count = count + 1 #increase status count by 1 
        
        #deal with date
        date = eachtopic['date'] #get the date
        if "Yesterday" not in date and "Today" not in date: 
            #print "neither yesterday or today"
            datestrings = date.split()
            monthnumber = re.sub("\D", "", datestrings[0])
            month = datestrings[1]
            year = datestrings[2]
            time = datestrings[3]
            amorpm = datestrings[4]
            totaldate = monthnumber + " " + month + " " + year + " " + time + " " + amorpm
            #print totaldate
            #print datetime.now()
            datetimeobject = datetime.strptime(totaldate, "%d %B %Y, %I:%M %p")
            print datetimeobject
        else:
            print "this one has a weird date"
            datetimeobject = datetime.now()
        
        #print datetimeobject

        link = eachtopic['link']
        noreplies = eachtopic['no of replies']
        for i in range(0,116):
            postnumber = "post number " + str(i)
            post = eachtopic[postnumber] 
            if post is not None:
                superstring = superstring + " " + post
        #print "now saving"
        scraperwiki.sqlite.save(["link"], { "link": link, "date": datetimeobject, "posts":superstring, "no of replies":noreplies})                 
    return

"""
for key, value in test[i].iteritems():
            if ( "post number" in key and value is not None):
                superstring = superstring + " " + value
            if "link" in key:
                link = value
            if "date" in key:
                date = value
        scraperwiki.sqlite.save(["link"], { "link": link, "date": date, "posts":superstring})
"""

def createueberstring():
    ueberstring = ""
    print "here comes ueber!"
    #print type(localdb)
    #print localdb
    i = 0
    for row in localdb:
        i = i + 1 
        print "We're now on row number: " + str(i)
        for key, value in row.iteritems():
            #print "row is type: " + str(type(row))
            #print "row is: " + str(row)
            #print "key is: " + str(key)
            #print "value is: " + str(value)
            
            if "posts" in key:
                ueberstring = ueberstring + " " + value 
            #print  "ueber is at +++" + ueberstring
    scraperwiki.sqlite.save(["ueber"], { "ueber":ueberstring}, "allinone")
    return

print "now combining posts..."
#get_data_combined_posts()
createueberstring()



"""
global ncolumnsmax
ncolumnsmax = 0 


info = scraperwiki.sqlite.table_info(name="src.swdata")
for column in info:
    #print column.name, column.type
    #print column[u'name']
    if "post number" in column[u'name']:
        #print "this one yes!" 
        ncolumns = int(column[u'name'][-2:])
        if ncolumns > ncolumnsmax:
            ncolumnsmax = ncolumns
    else: 
        print column[u'name']

print ncolumnsmax
        

print test
print type(test)
print test[0]

print type(test[0])


for row in test:
    for value in row.values():
        if isinstance(value, basestring):
            if value.find('capita') != -1:
                print value
"""import scraperwiki
import lxml.html
import lxml.etree
import collections
import time 
import string
import re
from datetime import datetime
#import datetime
import time
import operator

#attach the database. db is a list. each list item is a dict containing one topic (date, link, posts etc)
scraperwiki.sqlite.attach("eg-getposts", "src")
test = scraperwiki.sqlite.select("* from src.swdata limit 10")

#attach local db
localdb = scraperwiki.sqlite.select("* from swdata limit 2500")


#sort database
localdb = sorted(localdb, key=operator.itemgetter('date'))


#print various stuff for testing
#print len(test)
#print test
#print type(test)
#print type(test[0])
#print test[0]

"""


for topic in localdb:
    #print type(topic)
    #print topic
    print topic['date']


    

for key in test[0].keys():
    print "key is | " + str(key) + " int is: | " + str(int) + " | value is " #+ str(test[int])
    print key
    int = int + 1
"""

print "Welcome to post analysis program..."

global superstring
superstring = ""
global count
count = 0



def get_data_combined_posts():
    count = 0

    for eachtopic in test:
        #now have a dict called eachtopic which contains one topic only (link, date, post number 1;2;3 etc)
        print "Now working on number " + str(count) + " of " + str(len(test)) #status update
        superstring = "" #clear the superstring at start of this topic
        count = count + 1 #increase status count by 1 
        
        #deal with date
        date = eachtopic['date'] #get the date
        if "Yesterday" not in date and "Today" not in date: 
            #print "neither yesterday or today"
            datestrings = date.split()
            monthnumber = re.sub("\D", "", datestrings[0])
            month = datestrings[1]
            year = datestrings[2]
            time = datestrings[3]
            amorpm = datestrings[4]
            totaldate = monthnumber + " " + month + " " + year + " " + time + " " + amorpm
            #print totaldate
            #print datetime.now()
            datetimeobject = datetime.strptime(totaldate, "%d %B %Y, %I:%M %p")
            print datetimeobject
        else:
            print "this one has a weird date"
            datetimeobject = datetime.now()
        
        #print datetimeobject

        link = eachtopic['link']
        noreplies = eachtopic['no of replies']
        for i in range(0,116):
            postnumber = "post number " + str(i)
            post = eachtopic[postnumber] 
            if post is not None:
                superstring = superstring + " " + post
        #print "now saving"
        scraperwiki.sqlite.save(["link"], { "link": link, "date": datetimeobject, "posts":superstring, "no of replies":noreplies})                 
    return

"""
for key, value in test[i].iteritems():
            if ( "post number" in key and value is not None):
                superstring = superstring + " " + value
            if "link" in key:
                link = value
            if "date" in key:
                date = value
        scraperwiki.sqlite.save(["link"], { "link": link, "date": date, "posts":superstring})
"""

def createueberstring():
    ueberstring = ""
    print "here comes ueber!"
    #print type(localdb)
    #print localdb
    i = 0
    for row in localdb:
        i = i + 1 
        print "We're now on row number: " + str(i)
        for key, value in row.iteritems():
            #print "row is type: " + str(type(row))
            #print "row is: " + str(row)
            #print "key is: " + str(key)
            #print "value is: " + str(value)
            
            if "posts" in key:
                ueberstring = ueberstring + " " + value 
            #print  "ueber is at +++" + ueberstring
    scraperwiki.sqlite.save(["ueber"], { "ueber":ueberstring}, "allinone")
    return

print "now combining posts..."
#get_data_combined_posts()
createueberstring()



"""
global ncolumnsmax
ncolumnsmax = 0 


info = scraperwiki.sqlite.table_info(name="src.swdata")
for column in info:
    #print column.name, column.type
    #print column[u'name']
    if "post number" in column[u'name']:
        #print "this one yes!" 
        ncolumns = int(column[u'name'][-2:])
        if ncolumns > ncolumnsmax:
            ncolumnsmax = ncolumns
    else: 
        print column[u'name']

print ncolumnsmax
        

print test
print type(test)
print test[0]

print type(test[0])


for row in test:
    for value in row.values():
        if isinstance(value, basestring):
            if value.find('capita') != -1:
                print value
"""