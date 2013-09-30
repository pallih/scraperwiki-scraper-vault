###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://jp.translink.com.au/travel-information/network-information/buses/all-timetables')


# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <td> tags.
# -- UNCOMMENT THE 6 LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Console' tab again, and you'll see how we're extracting 
# the HTML that was inside <td></td> tags.
# We use lxml, which is a Python library especially for parsing html.
# -----------------------------------------------------------------------------

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
trs = root.cssselect('tr') # get all the <td> tags

scraperwiki.sqlite.execute('Create table if not exists buses (BusNum varchar(255) NOT NULL,BusName varchar(255),Buspath varchar(255), UNIQUE (BusNum))')
scraperwiki.sqlite.execute('Create table if not exists bustimetable (BusNum varchar(255), RouteSide varchar(255), Day varchar(20), time varchar(30))')
for tr in trs:
#    print lxml.html.tostring(td) # the full HTML tag
#    print lxml.html.tostring(tr)
    bnum= tr[0]
    #bname = lxml.html.tostring(tr[1].cssselect('a'))
    bname = tr[1].cssselect('a')
    for element in bname:

        #scraperwiki.sqlite.save(bnum.text,element.text,table_name="buses",verbose=2)
        scraperwiki.sqlite.execute("insert into buses values (?,?,?)",[bnum.text,element.text,element.get('href')])
#        print "Bus Number " +bnum.text + " Path name " +element.text
    
                      # just the text inside the HTML tag


scraperwiki.sqlite.commit() 
###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://jp.translink.com.au/travel-information/network-information/buses/all-timetables')


# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <td> tags.
# -- UNCOMMENT THE 6 LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Console' tab again, and you'll see how we're extracting 
# the HTML that was inside <td></td> tags.
# We use lxml, which is a Python library especially for parsing html.
# -----------------------------------------------------------------------------

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
trs = root.cssselect('tr') # get all the <td> tags

scraperwiki.sqlite.execute('Create table if not exists buses (BusNum varchar(255) NOT NULL,BusName varchar(255),Buspath varchar(255), UNIQUE (BusNum))')
scraperwiki.sqlite.execute('Create table if not exists bustimetable (BusNum varchar(255), RouteSide varchar(255), Day varchar(20), time varchar(30))')
for tr in trs:
#    print lxml.html.tostring(td) # the full HTML tag
#    print lxml.html.tostring(tr)
    bnum= tr[0]
    #bname = lxml.html.tostring(tr[1].cssselect('a'))
    bname = tr[1].cssselect('a')
    for element in bname:

        #scraperwiki.sqlite.save(bnum.text,element.text,table_name="buses",verbose=2)
        scraperwiki.sqlite.execute("insert into buses values (?,?,?)",[bnum.text,element.text,element.get('href')])
#        print "Bus Number " +bnum.text + " Path name " +element.text
    
                      # just the text inside the HTML tag


scraperwiki.sqlite.commit() 
