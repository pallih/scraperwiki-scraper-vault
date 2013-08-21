import scraperwiki

# Blank Python

import scraperwiki
import lxml.html
import string
import socket
#173.203.204.123
links =[]
levels =[]
baseURLs=[]

#get html object
#url = "http://www.ncl.ac.uk/apl/about/news/item/new-masters-programme-ma-architectural-design-research-starts-sept"

addr = "192.0.0.0.0.0.0"
print socket.gethostbyaddr("173.203.204.123")
val = 0
count = 1
#0 and 255 are reserved
while (count < 255):
    addr = "192." +str(count)+ ".100.100"
    print addr
    try:
        domain = socket.gethostbyaddr(addr)
        print domain[0]

    except:
        val + 1
    count = count + 1




try:
    socket.inet_aton(addr)
    # legal
    print "legal argument"
except socket.error:
    # Not legal
    print "illegal argument"

