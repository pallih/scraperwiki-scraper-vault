import scraperwiki

import re
import urllib2

scraperwiki.sqlite.attach('laptops-flipkart-producturls',"urls")
urls = scraperwiki.sqlite.select('* from urls.swdata')

for url in urls:
 listurl = url.values()
 productlink = listurl[0]  
 open = urllib2.urlopen(productlink)
 product = open.readlines()
 count = 1
 for line in product:
  match_product_title = re.search(r'<h1 itemprop="name".{0,100}.[\w\d\s\(\)\/]+',str(line))
  if match_product_title:
    print match_product_title.group()

#<h1 itemprop="name" title="Acer Aspire 5560 Laptop (APU Quad Core A6/ 4GB/ 500GB/ Win7 HB/ 512MB Graph) (NX.RUNS1.001)">Acer Aspire 5560 Laptop (APU Quad Core A6/ 4GB/ 500GB/ Win7 HB/ 512MB Graph) (NX.RUNS1.001)</h1>
import scraperwiki

import re
import urllib2

scraperwiki.sqlite.attach('laptops-flipkart-producturls',"urls")
urls = scraperwiki.sqlite.select('* from urls.swdata')

for url in urls:
 listurl = url.values()
 productlink = listurl[0]  
 open = urllib2.urlopen(productlink)
 product = open.readlines()
 count = 1
 for line in product:
  match_product_title = re.search(r'<h1 itemprop="name".{0,100}.[\w\d\s\(\)\/]+',str(line))
  if match_product_title:
    print match_product_title.group()

#<h1 itemprop="name" title="Acer Aspire 5560 Laptop (APU Quad Core A6/ 4GB/ 500GB/ Win7 HB/ 512MB Graph) (NX.RUNS1.001)">Acer Aspire 5560 Laptop (APU Quad Core A6/ 4GB/ 500GB/ Win7 HB/ 512MB Graph) (NX.RUNS1.001)</h1>
