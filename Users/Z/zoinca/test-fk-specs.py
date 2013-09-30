import scraperwiki

# Blank Python
import re
import urllib2

scraperwiki.sqlite.attach('laptops-fk-products-urls_1',"urls")
urls = scraperwiki.sqlite.select('* from urls.swdata')

for url in urls:
 listurl = url.values()
 pagelink = listurl[0]
 open = urllib2.urlopen(pagelink)
 page = open.readlines()
 #page.reverse()
 specs=""
 for line in page:
  #print line

  match_th = re.search(r'<th colspan.*>(.*)</th>',str(line))
  if match_th:
   specs =  specs+'<tr><th>'+match_th.group(1)+'</th></tr>'
   print specs
  match_td_key = re.search(r'specs-key.*>(.*)</.*',str(line))
  if match_td_key:
   specs = specs+'<tr><td>'+match_td_key.group(1)+'</td>'
   print specs
  match_td_value = re.search(r'<td.*specs-value.*>(.*)</td>.*',str(line))
  if match_td_value:
   specs = specs+'<td>'+match_td_value.group(1)+'</td></tr>'
   print specs
 scraperwiki.sqlite.save(['url'],data={'url':pagelink,'specs':specs})


import scraperwiki

# Blank Python
import re
import urllib2

scraperwiki.sqlite.attach('laptops-fk-products-urls_1',"urls")
urls = scraperwiki.sqlite.select('* from urls.swdata')

for url in urls:
 listurl = url.values()
 pagelink = listurl[0]
 open = urllib2.urlopen(pagelink)
 page = open.readlines()
 #page.reverse()
 specs=""
 for line in page:
  #print line

  match_th = re.search(r'<th colspan.*>(.*)</th>',str(line))
  if match_th:
   specs =  specs+'<tr><th>'+match_th.group(1)+'</th></tr>'
   print specs
  match_td_key = re.search(r'specs-key.*>(.*)</.*',str(line))
  if match_td_key:
   specs = specs+'<tr><td>'+match_td_key.group(1)+'</td>'
   print specs
  match_td_value = re.search(r'<td.*specs-value.*>(.*)</td>.*',str(line))
  if match_td_value:
   specs = specs+'<td>'+match_td_value.group(1)+'</td></tr>'
   print specs
 scraperwiki.sqlite.save(['url'],data={'url':pagelink,'specs':specs})


