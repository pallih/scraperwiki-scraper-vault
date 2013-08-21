# Scraper for facebook profile log

import scraperwiki
import urllib2
import lxml.html

website = urllib2.urlopen("http://www.yellowpages.com/scottsboro-al/mip/talk-of-the-town-10403487")
#website = urllib2.urlopen("http://www.rodrigoayala.me")

#read the content of the url in text format                                                                        
text = website.read()
print text

