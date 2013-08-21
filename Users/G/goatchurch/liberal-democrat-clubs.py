import scraperwiki
import urlparse
import re

from scraperwiki import datastore

libdemclubsindex = "http://www.interface-wizardry.co.uk/nulc/"
#print scraperwiki.scrape(libdemclubsindex)
libdemclubsearch = urlparse.urljoin(libdemclubsindex, "searchclubs1.asp")
#print scraperwiki.scrape(libdemclubsearch)
libdemresults = urlparse.urljoin(libdemclubsearch, "clubresults.asp")
params = { "Submit2":"Search", "Federation":"All" }
a = scraperwiki.scrape(libdemresults, params=params)

# the table is very simple, each pair of columns is a <b>key</b>, value
tableinfo = [ ]
rows = re.findall("(?si)<tr.*?>(.*?)</tr>", a)
for row in rows:
    collist = re.findall("(?si)<td.*?>(.*?)</td>", row)
    tableinfo.extend(collist)
    #print collist


    
# extract first two line and the number of clubs declared from the database
assert tableinfo[0] == '&nbsp;', tableinfo[:10]
mnumberclubs = re.match("Number of clubs found: <B>(\d+)</B> matching <B>All </B> federations", tableinfo[1])
assert mnumberclubs, tableinfo[:10]
numberclubs = int(mnumberclubs.group(1))


# now go through and harvest the key-value pairs
listclubs = [ ]
currentclub = None
currentkey = None
for val in tableinfo[2:]:
    mkey = re.match("<B>(.*?):?</B>", val)
    if mkey:
        assert not currentkey
        key = mkey.group(1)
        if key == "Club Name":
            #print currentclub, "cccc"
            currentclub = { }
            listclubs.append(currentclub)
        currentkey = key
    else:
        assert not re.search("(?i)<b>", val), val
        assert currentkey, val
        if currentkey == "Web Link":
            mwebmatch = re.match(" <a href='(http://(.*?))'", val)
            assert mwebmatch, val
            if mwebmatch.group(2): # most of them are blank
                currentclub[currentkey] = mwebmatch.group(1)
        elif currentkey == "Last Updated":
            mupdateddate = re.match("(\d\d)/(\d\d)/(\d\d\d\d)", val)
            assert mupdateddate, val
            currentclub[currentkey] = "%s-%s-%s" % (mupdateddate.group(3), mupdateddate.group(2), mupdateddate.group(1))
        else:
            currentclub[currentkey] = val
        currentkey = None

# verify we have the club count correct
assert numberclubs == len(listclubs), (numberclubs, len(listclubs))

# enter the clubs into the database    
for club in listclubs:
    datastore.save(unique_keys=['Club Name'], data=club)    

