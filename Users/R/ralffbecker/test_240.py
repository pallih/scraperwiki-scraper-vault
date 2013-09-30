import re
import scraperwiki           
import lxml.html

BLLinks = ['http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/2011-12/1/0/spieltag.html', 
                'http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/2011-12/2/0/spieltag.html', 
                'http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/2011-12/3/0/spieltag.html', 
                'http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/2011-12/4/0/spieltag.html', 
                'http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/2011-12/5/0/spieltag.html']

BLLookUp = dict()
BLLookUp['http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/2011-12/1/0/spieltag.html'] = 'ST1'
BLLookUp['http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/2011-12/2/0/spieltag.html'] = 'ST2'
BLLookUp['http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/2011-12/3/0/spieltag.html'] = 'ST3'
BLLookUp['http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/2011-12/4/0/spieltag.html'] = 'ST4'
BLLookUp['http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/2011-12/5/0/spieltag.html'] = 'ST5'

#get the data for the capacity and commissioning date
for BLLink in BLLinks:
    html = scraperwiki.scrape(BLLink)
    root = lxml.html.fromstring(html)
    
    rows = root.xpath("//table[@class='tStat']/tr")
    print "Hello"
   
    for row in rows:
        print row.xpath("./td[1]/text()")
import re
import scraperwiki           
import lxml.html

BLLinks = ['http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/2011-12/1/0/spieltag.html', 
                'http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/2011-12/2/0/spieltag.html', 
                'http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/2011-12/3/0/spieltag.html', 
                'http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/2011-12/4/0/spieltag.html', 
                'http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/2011-12/5/0/spieltag.html']

BLLookUp = dict()
BLLookUp['http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/2011-12/1/0/spieltag.html'] = 'ST1'
BLLookUp['http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/2011-12/2/0/spieltag.html'] = 'ST2'
BLLookUp['http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/2011-12/3/0/spieltag.html'] = 'ST3'
BLLookUp['http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/2011-12/4/0/spieltag.html'] = 'ST4'
BLLookUp['http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/2011-12/5/0/spieltag.html'] = 'ST5'

#get the data for the capacity and commissioning date
for BLLink in BLLinks:
    html = scraperwiki.scrape(BLLink)
    root = lxml.html.fromstring(html)
    
    rows = root.xpath("//table[@class='tStat']/tr")
    print "Hello"
   
    for row in rows:
        print row.xpath("./td[1]/text()")
