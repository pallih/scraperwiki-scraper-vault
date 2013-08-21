import scraperwiki

import re
import urllib2

url = "http://www.flipkart.com/laptops/pr?sid=6bo,b5g&_pop=flyout&otracker=hp_submenu_computer/"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
fullpage=str(lines)

print type(lines)

for line in lines: 
 match_item = re.search(r'<div class="items">.{0,20}',fullpage)
 if match_item:
  print match_item.group()



#<span class="items">636</span>
