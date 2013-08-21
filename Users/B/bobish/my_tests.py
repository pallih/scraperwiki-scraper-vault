import scraperwiki
import urlparse
import lxml.html

# Blank Python

url = "http://www.organic-bio.com/en/advanced-search2/?country=174&prgrp2=0&prodgrp2=0&prgrp3=0&prodgrp3=0&name=&city=&contact=&certification=0&service=0&fair=0"
html = scraperwiki.scrape(url)

tree = lxml.html.parse(url)

test = tree.xpath(".//*[@id='pages']/a[12]/text()")
print int(test[0])+1

#test = str(test).replace("\'","")

#print test

