import urllib2
import re
import scraperwiki
import datetime
import lxml.html
import hotshot

ipextract = re.compile('rtmp://(?P<IP>[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+):443/tinyconf')

def getrooms(n):

    ## Get list of tinychat room names from page n of the public listing
    response = urllib2.urlopen("http://tinychat.com/channel?frame=true&page=" + n)
    html = response.read()

    ## Method 1 of extracting room names, using the string find function
    #x = 0
    #i1 = 0
    #i2 = 0
    #x = html.find('picwrapper')
    #while x > -1 and i1 > -1 and i2 > -1:
    #    i1 = html.find("<span class='blip_live'>Live</span>\n   <b><a href=", x)
    #    i2 = html.find('>', i1+52)
    #    if i1>-1 and i2>-1:
    #        s.add(html[i1+52:i2-1])
    #    x = i2

    ## Method 2 of extracting room names, using lxml
    root = lxml.html.fromstring(html)
    for el in root.find_class('avatar'):
        room_name = el.iterlinks().next()[2][1:]
        getip(room_name)

def getip(room_name):

    # to add: if room closed or with password, remove it

    ## Get configuration of tinychat room called roomname
    response = urllib2.urlopen('http://tinychat.com/api/find.room/' + room_name)
    room_config = response.read()
    
    ## Method 2 for extracting IP address, using a regular expression
    match = ipextract.search(room_config)
    if not match:
        ## Room seems to be closed or now has password
        return
    ip = match.group('IP')
    
    scraperwiki.sqlite.execute("INSERT INTO associations values(NULL,?,?,?)", (ip, room_name, str(datetime.datetime.now())))

def maintain():
    scraperwiki.sqlite.execute("DROP TABLE associations")
    scraperwiki.sqlite.execute("CREATE TABLE associations (id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT, room TEXT, date TEXT)")

def get():
    for i in range(50): 
        getrooms(str(i))
        scraperwiki.sqlite.commit()

#maintain()
get()






