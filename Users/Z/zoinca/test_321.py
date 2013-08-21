import scraperwiki

# Blank Python
import urllib2
import re

scraperwiki.sqlite.attach('laptops-ib-pages-results','urls')
list_urls = scraperwiki.sqlite.select('* from urls.swdata')

count = 1
for dict_urls in list_urls:
 url = dict_urls['url']
 #print url
 
 open = urllib2.urlopen(url)
 page = str(open.readlines())
 

 matches = re.findall(r'(href=")(/Laptop/[./?=\w\d-]+)',page)
 for match in matches:
  pagelink = 'http://www.infibeam.com'+match[1]
  print pagelink
  print count
  count = count + 1
  scraperwiki.sqlite.save(['link'],data={'link':pagelink})

print 'total count : '+str(count)

"""

#<a href="/Laptop/i-Samsung-Laptop-NP550P5C-S01IN/P-CA-L-Samsung-NP550P5C-S01IN.html?id=Silver" title="Samsung NP550P5C Laptop (Silver)">
                            <img src="http://cdn-img-a-tata.infibeam.net/img/2acf123a/Samsung/NP550P5C-S01IN/upload/front/Samsung-NP550P5C-S01IN_a80f7.jpg?op_sharpen=1&amp;wid=120&amp;hei=130" title="Samsung NP550P5C Laptop (Silver)" alt="Samsung NP550P5C Laptop (Silver)">
                        <span class="title"><br> Samsung NP550P5C Laptop (Silver)</span>
                    </a>"""