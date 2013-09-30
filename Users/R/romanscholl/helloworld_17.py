import scraperwiki           
import lxml.html

#html = scraperwiki.scrape("https://scraperwiki.com/")
#html = scraperwiki.scrape("http://serv4/")

# get MCD 
html = scraperwiki.scrape("http://tools.morningstar.de/de/stockreport/default.aspx?tab=1&SecurityToken=0P000003IJ]3]0]E0WWE$$ALL&Id=0P000003IJ&ClientFund=0&CurrencyId=EUR")

root = lxml.html.fromstring(html)

# 1m
el = root.cssselect("div#TrailingReturns.box.trailingReturns td")[0]
print el.text

# 3m
el = root.cssselect("div#TrailingReturns.box.trailingReturns td")[1]
print el.text

# 1y
el = root.cssselect("div#TrailingReturns.box.trailingReturns td")[2]
print el.text

# 3y
el = root.cssselect("div#TrailingReturns.box.trailingReturns td")[3]
print el.text

# 5y
el = root.cssselect("div#TrailingReturns.box.trailingReturns td")[4]
print el.text

# 10y
el = root.cssselect("div#TrailingReturns.box.trailingReturns td")[5]
print el.text


#for el in root:
#    print el.tag
#    for el2 in el:
#        print "--", el2.tag, el2.attrib


##for el in root.cssselect("div.featured a"):
##    print el

##import scraperwiki
##html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")


##print root

#print html

import scraperwiki           
import lxml.html

#html = scraperwiki.scrape("https://scraperwiki.com/")
#html = scraperwiki.scrape("http://serv4/")

# get MCD 
html = scraperwiki.scrape("http://tools.morningstar.de/de/stockreport/default.aspx?tab=1&SecurityToken=0P000003IJ]3]0]E0WWE$$ALL&Id=0P000003IJ&ClientFund=0&CurrencyId=EUR")

root = lxml.html.fromstring(html)

# 1m
el = root.cssselect("div#TrailingReturns.box.trailingReturns td")[0]
print el.text

# 3m
el = root.cssselect("div#TrailingReturns.box.trailingReturns td")[1]
print el.text

# 1y
el = root.cssselect("div#TrailingReturns.box.trailingReturns td")[2]
print el.text

# 3y
el = root.cssselect("div#TrailingReturns.box.trailingReturns td")[3]
print el.text

# 5y
el = root.cssselect("div#TrailingReturns.box.trailingReturns td")[4]
print el.text

# 10y
el = root.cssselect("div#TrailingReturns.box.trailingReturns td")[5]
print el.text


#for el in root:
#    print el.tag
#    for el2 in el:
#        print "--", el2.tag, el2.attrib


##for el in root.cssselect("div.featured a"):
##    print el

##import scraperwiki
##html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")


##print root

#print html

