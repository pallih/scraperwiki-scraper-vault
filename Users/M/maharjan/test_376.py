# PLEASE READ THIS BEFORE EDITING
#
# This script generates your email alerts, to tell you when your scrapers
# are broken or someone has edited them.
#
# It works by emailing you the output of this script. If you read the code and
# know what you're doing, you can customise it, and make it send other emails
# for other purposes.

import scraperwiki
import urllib2
import BeautifulSoup as bs
import re
url ='http://202.166.205.141/bbvrs/index.php'
page = urllib2.urlopen(url,None,10)
print page
html = bs.BeautifulSoup(page)

       