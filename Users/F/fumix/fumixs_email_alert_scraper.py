# PLEASE READ THIS BEFORE EDITING
#
# This script generates your email alerts, to tell you when your scrapers
# are broken or someone has edited them.
#
# It works by emailing you the output of this script. If you read the code and
# know what you're doing, you can customise it, and make it send other emails
# for other purposes.

import scraperwiki
from BeautifulSoup import BeautifulSoup
import lxml.html

html = scraperwiki.scrape("http://www.xvideos.com/?k=japanese")
soup = BeautifulSoup(html)
links = soup.findAll("a",{"class":"miniature"})
for link in links:
    data = {
      'title' : link.find("span").string,
      'link' : link['href'],
      'thumbnail' : link.find("img")['src'],
    }
    scraperwiki.sqlite.save(unique_keys=['link'], data=data)
# PLEASE READ THIS BEFORE EDITING
#
# This script generates your email alerts, to tell you when your scrapers
# are broken or someone has edited them.
#
# It works by emailing you the output of this script. If you read the code and
# know what you're doing, you can customise it, and make it send other emails
# for other purposes.

import scraperwiki
from BeautifulSoup import BeautifulSoup
import lxml.html

html = scraperwiki.scrape("http://www.xvideos.com/?k=japanese")
soup = BeautifulSoup(html)
links = soup.findAll("a",{"class":"miniature"})
for link in links:
    data = {
      'title' : link.find("span").string,
      'link' : link['href'],
      'thumbnail' : link.find("img")['src'],
    }
    scraperwiki.sqlite.save(unique_keys=['link'], data=data)
