#Blank Python
# -*- coding: iso-8859-15 -*-
import scraperwiki
import lxml.html
import datetime


html = scraperwiki.scrape("https://www.tg-berlin.de/nc/alle-veranstaltungen/spielstaetten.html")
root = lxml.html.fromstring(html)
count_id = 12345



for el in root.cssselect("div.spielstaette a"):
     print el.text

