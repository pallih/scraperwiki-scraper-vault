import scraperwiki           
import lxml.html


companies = [ 
    ['MCD','http://tools.morningstar.de/de/stockreport/default.aspx?tab=1&SecurityToken=0P000003IJ]3]0]E0WWE$$ALL&Id=0P000003IJ'] , 
    ['CHD','http://tools.morningstar.de/de/stockreport/default.aspx?tab=1&SecurityToken=0P0000019F]3]0]E0WWE$$ALL&Id=0P0000019F'] , 
    ['O'  ,'http://tools.morningstar.de/de/stockreport/default.aspx?tab=1&SecurityToken=0P000004M1]3]0]E0WWE$$ALL&Id=0P000004M1'] 
]


# O-Wertentw  http://tools.morningstar.de/de/stockreport/default.aspx?tab=1         &SecurityToken=0P000004M1]3]0]E0WWE$$ALL&Id=0P000004M1  &ClientFund=0  &CurrencyId=EUR

# O-Uebersicht http://tools.morningstar.de/de/stockreport/default.aspx?tab=0&vw=sum  &SecurityToken=0P000004M1]3]0]E0WWE$$ALL&Id=0P000004M1  &ClientFund=0  &CurrencyId=EUR
#     KGV Rendite ISIN MktCap Sektor/Industrie etc


for comp in companies:

    # get Wertentwicklung
    comp_short = str(comp[0]).strip()
    comp_url = str(comp[1].strip())
    html = scraperwiki.scrape(comp_url)
    root = lxml.html.fromstring(html)

    ret1m  = root.cssselect("div#TrailingReturns.box.trailingReturns td")[0]
    ret3m  = root.cssselect("div#TrailingReturns.box.trailingReturns td")[1]
    ret1y  = root.cssselect("div#TrailingReturns.box.trailingReturns td")[2]
    ret3y  = root.cssselect("div#TrailingReturns.box.trailingReturns td")[3]
    ret5y  = root.cssselect("div#TrailingReturns.box.trailingReturns td")[4]
    ret10y = root.cssselect("div#TrailingReturns.box.trailingReturns td")[5]


    # calculate statistics
    avg  = (float(ret1y.text) + float(ret3y.text) + float(ret5y.text) + float(ret10y.text)) / 4
    sum2 = (float(ret1y.text)**2 + float(ret3y.text)**2 + float(ret5y.text)**2 + float(ret10y.text)**2)
    avg2 = sum2 / 4
    var  = avg2 - (avg**2)
    var2 = var**0.5
    myrank = avg / var2

    # TODO: get Uebersicht with KGV Rendite MktCap ISIN CashFlow


    # print results

    #print '"',comp_short.strip(),'" , "',ret1m.text,'" , "',ret3m.text,'" , "',ret1y.text,'" , "',ret3y.text,'" , "',ret5y.text,'" , "',ret10y.text,'"'
    #print avg , var2, myrank
    #print avg , sum2, avg2, var, var2, myrank
    #print sum2
    #print "Avg: %s   Sum2: %s" % avg, sum2
    print "%s ; %0.1f ; %0.1f ; %0.1f ; %0.1f ; %0.1f ; %0.1f ; %0.1f ; %0.1f ; %0.1f" % \
        ( comp_short, float(ret1m.text), float(ret3m.text), float(ret1y.text), float(ret3y.text), float(ret5y.text), float(ret10y.text), avg, var2, myrank )


    # TODO: save to CSV or Excel or SQLITE


    # Save to DATA tab for copy&paste

    # KO scraperwiki.datastore.save(["day"], record)
    # KO scraperwiki.datastore.save(["test"], ["aaa"])
    # OK scraperwiki.sqlite.save(unique_keys=["a"], data={"a":myrank, "bbb":avg})
    scraperwiki.sqlite.save(unique_keys=["comp_short"], 
        data={"comp_short":comp_short, "ret1y":float(ret1y.text), "ret3y":float(ret3y.text), "ret5y":float(ret5y.text), "ret10y":float(ret10y.text), 
        "avg":avg, "var2":var2, "myrank":myrank})

    # KO scraperwiki.sqlite.save(unique_keys=[comp_short], data={comp_short:1, "bbb":"Hi there"})
    # KO scraperwiki.sqlite.save(unique_keys=[comp_short], data={comp_short:1, "bbb":"Hi there"})


import scraperwiki           
import lxml.html


companies = [ 
    ['MCD','http://tools.morningstar.de/de/stockreport/default.aspx?tab=1&SecurityToken=0P000003IJ]3]0]E0WWE$$ALL&Id=0P000003IJ'] , 
    ['CHD','http://tools.morningstar.de/de/stockreport/default.aspx?tab=1&SecurityToken=0P0000019F]3]0]E0WWE$$ALL&Id=0P0000019F'] , 
    ['O'  ,'http://tools.morningstar.de/de/stockreport/default.aspx?tab=1&SecurityToken=0P000004M1]3]0]E0WWE$$ALL&Id=0P000004M1'] 
]


# O-Wertentw  http://tools.morningstar.de/de/stockreport/default.aspx?tab=1         &SecurityToken=0P000004M1]3]0]E0WWE$$ALL&Id=0P000004M1  &ClientFund=0  &CurrencyId=EUR

# O-Uebersicht http://tools.morningstar.de/de/stockreport/default.aspx?tab=0&vw=sum  &SecurityToken=0P000004M1]3]0]E0WWE$$ALL&Id=0P000004M1  &ClientFund=0  &CurrencyId=EUR
#     KGV Rendite ISIN MktCap Sektor/Industrie etc


for comp in companies:

    # get Wertentwicklung
    comp_short = str(comp[0]).strip()
    comp_url = str(comp[1].strip())
    html = scraperwiki.scrape(comp_url)
    root = lxml.html.fromstring(html)

    ret1m  = root.cssselect("div#TrailingReturns.box.trailingReturns td")[0]
    ret3m  = root.cssselect("div#TrailingReturns.box.trailingReturns td")[1]
    ret1y  = root.cssselect("div#TrailingReturns.box.trailingReturns td")[2]
    ret3y  = root.cssselect("div#TrailingReturns.box.trailingReturns td")[3]
    ret5y  = root.cssselect("div#TrailingReturns.box.trailingReturns td")[4]
    ret10y = root.cssselect("div#TrailingReturns.box.trailingReturns td")[5]


    # calculate statistics
    avg  = (float(ret1y.text) + float(ret3y.text) + float(ret5y.text) + float(ret10y.text)) / 4
    sum2 = (float(ret1y.text)**2 + float(ret3y.text)**2 + float(ret5y.text)**2 + float(ret10y.text)**2)
    avg2 = sum2 / 4
    var  = avg2 - (avg**2)
    var2 = var**0.5
    myrank = avg / var2

    # TODO: get Uebersicht with KGV Rendite MktCap ISIN CashFlow


    # print results

    #print '"',comp_short.strip(),'" , "',ret1m.text,'" , "',ret3m.text,'" , "',ret1y.text,'" , "',ret3y.text,'" , "',ret5y.text,'" , "',ret10y.text,'"'
    #print avg , var2, myrank
    #print avg , sum2, avg2, var, var2, myrank
    #print sum2
    #print "Avg: %s   Sum2: %s" % avg, sum2
    print "%s ; %0.1f ; %0.1f ; %0.1f ; %0.1f ; %0.1f ; %0.1f ; %0.1f ; %0.1f ; %0.1f" % \
        ( comp_short, float(ret1m.text), float(ret3m.text), float(ret1y.text), float(ret3y.text), float(ret5y.text), float(ret10y.text), avg, var2, myrank )


    # TODO: save to CSV or Excel or SQLITE


    # Save to DATA tab for copy&paste

    # KO scraperwiki.datastore.save(["day"], record)
    # KO scraperwiki.datastore.save(["test"], ["aaa"])
    # OK scraperwiki.sqlite.save(unique_keys=["a"], data={"a":myrank, "bbb":avg})
    scraperwiki.sqlite.save(unique_keys=["comp_short"], 
        data={"comp_short":comp_short, "ret1y":float(ret1y.text), "ret3y":float(ret3y.text), "ret5y":float(ret5y.text), "ret10y":float(ret10y.text), 
        "avg":avg, "var2":var2, "myrank":myrank})

    # KO scraperwiki.sqlite.save(unique_keys=[comp_short], data={comp_short:1, "bbb":"Hi there"})
    # KO scraperwiki.sqlite.save(unique_keys=[comp_short], data={comp_short:1, "bbb":"Hi there"})


