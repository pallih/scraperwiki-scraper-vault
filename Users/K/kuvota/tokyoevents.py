# -*- coding: utf-8 -*-
import scraperwiki
#html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")
html = scraperwiki.scrape("http://www.enjoytokyo.jp/search/museum/event/")
#print html

import lxml.html           
root = lxml.html.fromstring(html)

#for tr in root.cssselect("table[align='left'] tr.tcont"):
#    tds = tr.cssselect("td")
#    data = {
#      'country' : tds[0].text_content(),
#      'years_in_school' : int(tds[4].text_content())
#    }
#    print data
#
#

#print root

#for div in root.cssselect("div.searchList div.vevent p.name a"):
for div in root.cssselect("div.searchList div.vevent"):
#    a = div.cssselect("div.vevent p a")
#    print div
#    print div.text
#    div2 = div.cssselect("p.name a")
#    print div2
    data = {
#        'eventname' : div.text
        'eventname' : (div.cssselect("p.name a"))[0].text,
        'Date' : (div.cssselect("div.dtl-txtb.clearfix div.dtl-txtb-rb2 p.ymd"))[0].text_content(),
        'location' : (div.cssselect("div.dtl-txtb.clearfix div.dtl-txtb-rb2 p.cate-txt.location"))[0].text,
        'description' : (div.cssselect("div.dtl-txtb.clearfix div.dtl-txtb-rb2 p.description"))[0].text,
        'station' : (div.cssselect("div.dtl-txtb.clearfix div.dtl-txtb-rb2 ul.cate li span"))[2].text
#        'date' : (div.cssselect("div div.dtl-txtb-rb2 p.ymd")).text
    }
    scraperwiki.sqlite.save(unique_keys=['eventname'], data=data)





# -*- coding: utf-8 -*-
import scraperwiki
#html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")
html = scraperwiki.scrape("http://www.enjoytokyo.jp/search/museum/event/")
#print html

import lxml.html           
root = lxml.html.fromstring(html)

#for tr in root.cssselect("table[align='left'] tr.tcont"):
#    tds = tr.cssselect("td")
#    data = {
#      'country' : tds[0].text_content(),
#      'years_in_school' : int(tds[4].text_content())
#    }
#    print data
#
#

#print root

#for div in root.cssselect("div.searchList div.vevent p.name a"):
for div in root.cssselect("div.searchList div.vevent"):
#    a = div.cssselect("div.vevent p a")
#    print div
#    print div.text
#    div2 = div.cssselect("p.name a")
#    print div2
    data = {
#        'eventname' : div.text
        'eventname' : (div.cssselect("p.name a"))[0].text,
        'Date' : (div.cssselect("div.dtl-txtb.clearfix div.dtl-txtb-rb2 p.ymd"))[0].text_content(),
        'location' : (div.cssselect("div.dtl-txtb.clearfix div.dtl-txtb-rb2 p.cate-txt.location"))[0].text,
        'description' : (div.cssselect("div.dtl-txtb.clearfix div.dtl-txtb-rb2 p.description"))[0].text,
        'station' : (div.cssselect("div.dtl-txtb.clearfix div.dtl-txtb-rb2 ul.cate li span"))[2].text
#        'date' : (div.cssselect("div div.dtl-txtb-rb2 p.ymd")).text
    }
    scraperwiki.sqlite.save(unique_keys=['eventname'], data=data)





