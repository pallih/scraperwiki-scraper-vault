import scraperwiki
import lxml.html
import re
import time

yelpurl = "http://www.yelp.com/search?find_desc=MK+Catering&find_loc=&ns=1"

html = scraperwiki.scrape(yelpurl)
time.sleep(.2)
root = lxml.html.fromstring(html)
entered = "false"
productname = ""
rem = ""
phonenumber = ""

spans = root.cssselect('span.highlighted')
divs = root.cssselect('div.phone')

for a in spans:
    print a.text

for div in divs:
    phonenumber = div.text


print phonenumber


    