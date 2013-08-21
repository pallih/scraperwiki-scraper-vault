import scraperwiki           
import lxml.html

#html = scraperwiki.scrape("https://scraperwiki.com/")
#html = scraperwiki.scrape("http://serv4/")


companies = [ 
['MCD','http://tools.morningstar.de/de/stockreport/default.aspx?tab=1&SecurityToken=0P000003IJ]3]0]E0WWE$$ALL&Id=0P000003IJ'] , 
['CHD','http://tools.morningstar.de/de/stockreport/default.aspx?tab=1&SecurityToken=0P0000019F]3]0]E0WWE$$ALL&Id=0P0000019F'] 
]

# get MCD
# MCD NYSE USD   http://tools.morningstar.de/de/stockreport/default.aspx?tab=1&SecurityToken=0P000003IJ]3]0]E0WWE$$ALL&Id=0P000003IJ&ClientFund=0&CurrencyId=EUR
html = scraperwiki.scrape("http://tools.morningstar.de/de/stockreport/default.aspx?tab=1&SecurityToken=0P000003IJ]3]0]E0WWE$$ALL&Id=0P000003IJ")

# get CHD
# CHD NYSE USD   http://tools.morningstar.de/de/stockreport/default.aspx?tab=1&SecurityToken=0P0000019F]3]0]E0WWE$$ALL&Id=0P0000019F&ClientFund=0&CurrencyId=EUR
#html = scraperwiki.scrape("http://tools.morningstar.de/de/stockreport/default.aspx?tab=1&SecurityToken=0P0000019F]3]0]E0WWE$$ALL&Id=0P0000019F")

for comp in companies:
    #print comp[0], ": ", comp[1]
    html = scraperwiki.scrape(comp[1])
    root = lxml.html.fromstring(html)

    ret1m = root.cssselect("div#TrailingReturns.box.trailingReturns td")[0]
    #print "1m: " , ret1m.text
    ret3m = root.cssselect("div#TrailingReturns.box.trailingReturns td")[1]
    #print "3m: " , ret3m.text
    ret1y = root.cssselect("div#TrailingReturns.box.trailingReturns td")[2]
    #print "1y: " , ret1y.text
    ret3y = root.cssselect("div#TrailingReturns.box.trailingReturns td")[3]
    #print "3y: " , ret3y.text, " pa"
    ret5y = root.cssselect("div#TrailingReturns.box.trailingReturns td")[4]
    #print "5y: " , ret5y.text, " pa"
    ret10y = root.cssselect("div#TrailingReturns.box.trailingReturns td")[5]
    #print "10y: " , ret10y.text, " pa"

    print comp[0], ret1m.text, ret3m.text, ret1y.text, ret3y.text, ret5y.text, ret10y.text


'''
root = lxml.html.fromstring(html)
# 1m
el = root.cssselect("div#TrailingReturns.box.trailingReturns td")[0]
print "1m: " , el.text
# 3m
el = root.cssselect("div#TrailingReturns.box.trailingReturns td")[1]
print "3m: " , el.text
# 1y
el = root.cssselect("div#TrailingReturns.box.trailingReturns td")[2]
print "1y: " , el.text
# 3y
el = root.cssselect("div#TrailingReturns.box.trailingReturns td")[3]
print "3y: " , el.text, " pa"
# 5y
el = root.cssselect("div#TrailingReturns.box.trailingReturns td")[4]
print "5y: " , el.text, " pa"
# 10y
el = root.cssselect("div#TrailingReturns.box.trailingReturns td")[5]
print "10y: " , el.text, " pa"
'''

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

