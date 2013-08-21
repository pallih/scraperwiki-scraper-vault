import scraperwiki

# Blank Python
import re
import urllib2

url = "http://www.homeshop18.com/pen-drives/usb-pen-drives/categoryid:8899/search:pen+drives/?it_category=MN&it_action=CA-MNT203&it_label=MN-MNT203-CA-1207041826-O-O-PH-SR_PenDrives&it_value=0"
count = 0
open = urllib2.urlopen(url)
lines = open.readlines()
lines.reverse()

matches = re.findall(r'http://www.homeshop18.com/[\w-]+/computer-peripherals/storage-devices/product:\d+/cid:\d+/',str(lines).strip('[]'))
matches.sort()
for match in matches:
  match_count = matches.count(match)
  if match_count > 1:
    match_index = matches.index(match)
    while match_count !=1:
      matches.pop(match_index + 1)
      match_count -= 1
  count = count + 1
for match in matches:
   url_product = match.strip('[]')
   url_product = url_product.replace("'","")
   print url_product
   data = {'url':url_product}
   scraperwiki.sqlite.save(unique_keys=["url"], data=data)


