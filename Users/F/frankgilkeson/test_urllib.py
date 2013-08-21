import scraperwiki

# Blank Python

import urllib
ufile = urllib.urlopen("http://qpublic7.qpublic.net/ga_display.php?county=ga_lumpkin&KEY=074++++036")

text = ufile.read()

print text

info = ufile.info()

print info

import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://qpublic7.qpublic.net/ga_display.php?county=ga_lumpkin&KEY=074++++036")
root = lxml.html.fromstring(html)


for el in root.cssselect("div.table_class table"):
    print el

