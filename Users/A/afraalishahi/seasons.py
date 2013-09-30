import scraperwiki
import urllib2
import lxml.html

website = urllib2.urlopen("http://timeanddate.com/calendar/seasons.html")

#read the content of the url in text format                                                                        
text = website.read()

#parse the html content                                                                                            
root = lxml.html.fromstring(text)

for tr in root.cssselect("div tr"):
    tds = tr.cssselect("td")
    if (len(tds) == 9):
        data = {'year' : tds[0].text_content(), 
                'spring' : tds[1].text_content(),
                'summer' : tds[3].text_content() 
        }
        print data
        scraperwiki.sqlite.save(unique_keys=['year'], data=data)

import scraperwiki
import urllib2
import lxml.html

website = urllib2.urlopen("http://timeanddate.com/calendar/seasons.html")

#read the content of the url in text format                                                                        
text = website.read()

#parse the html content                                                                                            
root = lxml.html.fromstring(text)

for tr in root.cssselect("div tr"):
    tds = tr.cssselect("td")
    if (len(tds) == 9):
        data = {'year' : tds[0].text_content(), 
                'spring' : tds[1].text_content(),
                'summer' : tds[3].text_content() 
        }
        print data
        scraperwiki.sqlite.save(unique_keys=['year'], data=data)

