import scraperwiki
import lxml.html
import urllib2
import datetime
import re


# Because the website I'm scraping keeps throwing me out, I needed a way to check what the last record gathered was. Below is an ugly hack that gets me the info I need. 
# If anyone would like to improve on this please do and leave me some comments so I can learn some more...
# Oh and if you were wondering why the <> '000' etc. thats because I first started from 1, then changed my mind and then started from the maximum record.
# I can't figure how to delete records from the original database so I can get rid of that.

def MainParse():
    rows = scraperwiki.sqlite.attach("iom_company_registry_parse", "src")
    maxB = scraperwiki.sqlite.select("Number FROM src.swdata WHERE substr(Number,7,1)='B' AND substr(Number,1,3) <> '000' ORDER BY substr(Number,1,6) DESC LIMIT 1")
    maxC = scraperwiki.sqlite.select("CompanyNumber FROM src.swdata WHERE substr(CompanyNumber,7,1)='C' AND substr(CompanyNumber,1,3) <> '000' ORDER BY substr(CompanyNumber,1,6) DESC LIMIT 1")
    maxF = scraperwiki.sqlite.select("CompanyNumber FROM src.swdata WHERE substr(CompanyNumber,7,1)='F' AND substr(CompanyNumber,1,4) <> '0000' ORDER BY substr(CompanyNumber,1,6) DESC LIMIT 1")
    maxL = scraperwiki.sqlite.select("CompanyNumber FROM src.swdata WHERE substr(CompanyNumber,7,1)='L' ORDER BY substr(CompanyNumber,1,6) DESC LIMIT 1")
    maxV = scraperwiki.sqlite.select("CompanyNumber FROM src.swdata WHERE substr(CompanyNumber,7,1)='V' ORDER BY substr(CompanyNumber,1,6) DESC LIMIT 1")
    minB = scraperwiki.sqlite.select("Number FROM src.swdata WHERE substr(Number,7,1)='B' AND substr(Number,1,3) <> '000' ORDER BY substr(Number,1,6) ASC LIMIT 1")
    minC = scraperwiki.sqlite.select("CompanyNumber FROM src.swdata WHERE substr(CompanyNumber,7,1)='C' AND substr(CompanyNumber,1,3) <> '000' ORDER BY substr(CompanyNumber,1,6) ASC LIMIT 1")
    minF = scraperwiki.sqlite.select("CompanyNumber FROM src.swdata WHERE substr(CompanyNumber,7,1)='F' AND substr(CompanyNumber,1,4) <> '0000' ORDER BY substr(CompanyNumber,1,6) ASC LIMIT 1")
    minL = scraperwiki.sqlite.select("CompanyNumber FROM src.swdata WHERE substr(CompanyNumber,7,1)='L' ORDER BY substr(CompanyNumber,1,6) ASC LIMIT 1")
    minV = scraperwiki.sqlite.select("CompanyNumber FROM src.swdata WHERE substr(CompanyNumber,7,1)='V' ORDER BY substr(CompanyNumber,1,6) ASC LIMIT 1")
    rows = scraperwiki.sqlite.select("* FROM src.swdata WHERE substr(CompanyNumber,7,1)='F'  AND substr(CompanyNumber,1,4) <> '0000' ")


    print "Min B = ", int(str(minB[0].values())[3:9]), " Max B = ", int(str(maxB[0].values())[3:9])
    print "Min C = ", int(str(minC[0].values())[3:9]), " Max C = ", int(str(maxC[0].values())[3:9])
    print "Min F = ", int(str(minF[0].values())[3:9]), " Max F = ", int(str(maxF[0].values())[3:9])
    print "Min L = ", int(str(minL[0].values())[3:9]), " Max L = ", int(str(maxL[0].values())[3:9])
    print "Min V = ", int(str(minV[0].values())[3:9]), " Max V = ", int(str(maxV[0].values())[3:9])


#    for row in rows:
#        Parse(row["number"], row["code"], row["html"])


MainParse()
