###############################################################################
# Scrapes 20 latest notable fish catches from the Angling Times website
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://www.gofishing.co.uk/Angling-Times/Section/News--Catches/?N=606+190+508+526&Rpp=20&Ns=P_Publication_Date%7c1')

# clear existing datastore
#scraperwiki.sqlite.execute("delete from ttt where xx=9")
scraperwiki.sqlite.execute("drop table if exists swdata")


import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object

# Get the top story which is in a different heading tag to the others
topstory = root.cssselect("div.resultFirstItemContent h3 a")[0]           
print topstory.text
print "http://www.gofishing.co.uk" + topstory.get('href')
scraperwiki.sqlite.save(unique_keys=[], data={'Headline' : topstory.text, 'URL' :"http://www.gofishing.co.uk" + topstory.get('href')})

# Get all the other stories
headlines = root.cssselect('div.resultItemContent h2 a') # get all the headlines tags

for headline in headlines:

     print headline.text                # just the text inside the HTML tag
     print "http://www.gofishing.co.uk" + headline.get('href')
     # add a datestamp so we now which is newest 
     import datetime
     now = datetime.datetime.now()
     print str(now)
     scraperwiki.sqlite.save(unique_keys=[], data={'Headline' : headline.text, 'URL' :"http://www.gofishing.co.uk" + headline.get('href'), 'Timestamp' :str(now)})

###############################################################################
# Scrapes 20 latest notable fish catches from the Angling Times website
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://www.gofishing.co.uk/Angling-Times/Section/News--Catches/?N=606+190+508+526&Rpp=20&Ns=P_Publication_Date%7c1')

# clear existing datastore
#scraperwiki.sqlite.execute("delete from ttt where xx=9")
scraperwiki.sqlite.execute("drop table if exists swdata")


import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object

# Get the top story which is in a different heading tag to the others
topstory = root.cssselect("div.resultFirstItemContent h3 a")[0]           
print topstory.text
print "http://www.gofishing.co.uk" + topstory.get('href')
scraperwiki.sqlite.save(unique_keys=[], data={'Headline' : topstory.text, 'URL' :"http://www.gofishing.co.uk" + topstory.get('href')})

# Get all the other stories
headlines = root.cssselect('div.resultItemContent h2 a') # get all the headlines tags

for headline in headlines:

     print headline.text                # just the text inside the HTML tag
     print "http://www.gofishing.co.uk" + headline.get('href')
     # add a datestamp so we now which is newest 
     import datetime
     now = datetime.datetime.now()
     print str(now)
     scraperwiki.sqlite.save(unique_keys=[], data={'Headline' : headline.text, 'URL' :"http://www.gofishing.co.uk" + headline.get('href'), 'Timestamp' :str(now)})

