import scraperwiki
import lxml.html
import lxml.etree
import collections
import time 
import string
import re
from datetime import datetime
import time
import operator

#attach the database. db is a list. each list item is a dict containing one topic (date, link, posts etc)
scraperwiki.sqlite.attach("eg-analyseposts", "src")
data = scraperwiki.sqlite.select("* from src.swdata")


"""
print len(data)
total = 0
for i in range(len(data)):
    total = total + data[i]['no of replies']
    #print data[i]['no of replies']
print total
"""

print data[2]['posts']
print len(re.findall(r'\w+', data[2]['posts']))


print len(data)
total = 0
for i in range(len(data)):
    total = total + len(re.findall(r'\w+', data[i]['posts']))
print totalimport scraperwiki
import lxml.html
import lxml.etree
import collections
import time 
import string
import re
from datetime import datetime
import time
import operator

#attach the database. db is a list. each list item is a dict containing one topic (date, link, posts etc)
scraperwiki.sqlite.attach("eg-analyseposts", "src")
data = scraperwiki.sqlite.select("* from src.swdata")


"""
print len(data)
total = 0
for i in range(len(data)):
    total = total + data[i]['no of replies']
    #print data[i]['no of replies']
print total
"""

print data[2]['posts']
print len(re.findall(r'\w+', data[2]['posts']))


print len(data)
total = 0
for i in range(len(data)):
    total = total + len(re.findall(r'\w+', data[i]['posts']))
print total