import scraperwiki
import re
import time


# Blank Python


errors =""

def logError(iter,  msg):
    global errors
    time_ = str(time.time())
    errdata = { "time":time_,"iter":iter, "msg":msg, "source":"khgtesthree_osvdb1" }
    scraperwiki.sqlite.save(unique_keys=['iter', 'time'], data=errdata, table_name="errors")
    errors += iter + ": "  + msg + "\n"
    print msg
    





print str(time.time())

url = "http://scraperwiki.com"
test = "http://anonymouse.org/cgi-bin/anon-www.cgi/http://www.google.com/webhp?hl=en"
#html = scraperwiki.scrape("http://anonymouse.org/cgi-bin/anon-www.cgi/"+url+"/webhp?hl=en")
print "http://anonymouse.org/cgi-bin/anon-www.cgi/"+url+"/webhp?hl=en"
print test
#print html

db = scraperwiki.sqlite.select("* from swdata")
for row in db:
    print row
    print type(row)

import scraperwiki
import re
import time


# Blank Python


errors =""

def logError(iter,  msg):
    global errors
    time_ = str(time.time())
    errdata = { "time":time_,"iter":iter, "msg":msg, "source":"khgtesthree_osvdb1" }
    scraperwiki.sqlite.save(unique_keys=['iter', 'time'], data=errdata, table_name="errors")
    errors += iter + ": "  + msg + "\n"
    print msg
    





print str(time.time())

url = "http://scraperwiki.com"
test = "http://anonymouse.org/cgi-bin/anon-www.cgi/http://www.google.com/webhp?hl=en"
#html = scraperwiki.scrape("http://anonymouse.org/cgi-bin/anon-www.cgi/"+url+"/webhp?hl=en")
print "http://anonymouse.org/cgi-bin/anon-www.cgi/"+url+"/webhp?hl=en"
print test
#print html

db = scraperwiki.sqlite.select("* from swdata")
for row in db:
    print row
    print type(row)

