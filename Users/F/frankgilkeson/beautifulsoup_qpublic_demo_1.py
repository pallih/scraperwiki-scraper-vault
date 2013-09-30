import scraperwiki

import urllib2
from BeautifulSoup import BeautifulSoup

page = urllib2.urlopen("http://qpublic7.qpublic.net/ga_display.php?county=ga_lumpkin&KEY=074++++036")
soup = BeautifulSoup(page)
for owner in soup('td'):
    
    print owner.strip()
   
import scraperwiki

import urllib2
from BeautifulSoup import BeautifulSoup

page = urllib2.urlopen("http://qpublic7.qpublic.net/ga_display.php?county=ga_lumpkin&KEY=074++++036")
soup = BeautifulSoup(page)
for owner in soup('td'):
    
    print owner.strip()
   
