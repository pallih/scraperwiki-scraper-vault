###########################################################################################
# This scraper extracts information from a charity's Summary Information Return
# , from the Charity Commission website
###########################################################################################

import scraperwiki
import json
from BeautifulSoup import BeautifulSoup
import re

charnum=[209131,1036733,1089464,205846,268369,202918,1052183,213890,216250,1097940,225971,210183,222377,216401,214779,1123636,218186,270901,207994,1104951,206061,219279,1084952,208076,207076]
#charnum=[202918]

for i in charnum:
    ccnum = i
    year = 2009
    url = str(ccnum).rjust(10,"0")
    yearurl = str(year)[2:4]
    ends = url[8:10]
    pdfurl = "http://www.charity-commission.gov.uk/SIR/ENDS" + ends + "/" + url + "_SIR_" + yearurl + "_E.PDF"
    print pdfurl
    try:
        a = scraperwiki.scrape(pdfurl)
        s = BeautifulSoup(scraperwiki.pdftoxml(a))
        ccnum = long(pdfurl[48:58])
        year = long(pdfurl[64:65]) + 2000

        #print charnum, year
    
        #print s

        name = None
        all = []
        data = {}
        state = None
        l = []
        comparison1 = u'\u00a3 000s'
        comparison2 = u'Activity \u00a3 000s'

        pTag = s.find(text=comparison1)
        for i, t in enumerate(pTag.findAllNext(limit=6)):
            record = int(round((i+2)/2,0))
            if i==0 or i==2 or i==4:
                scraperwiki.datastore.save(["ccnum","record","year"], { "ccnum" : ccnum, "year" : year, "record" : record, "type" : "Charitable Activities" } )
                scraperwiki.datastore.save(["ccnum","record","year"], { "ccnum" : ccnum, "year" : year, "record" : record, "title": t.text.replace('&amp;','&') } )
            else:
                charact = long(re.sub(r'[^0-9]', '', t.text))
                scraperwiki.datastore.save(["ccnum","record","year"], { "ccnum" : ccnum, "year" : year, "record" : record, "value": charact } )
        pTag = s.find(text=comparison2)
        for i, t in enumerate(pTag.findAllNext(limit=9)):
            record = int((i+3)/3)+3
            if t.text=='Explanatory Comments':
                break
            else:
                if i==0 or i==3 or i==6:
                    scraperwiki.datastore.save(["ccnum","record","year"], { "ccnum" : ccnum, "year" : year, "record" : record, "type" : "Income from Fundraising"})
                    scraperwiki.datastore.save(["ccnum","record","year"], { "ccnum" : ccnum, "year" : year, "record" : record, "title": t.text.replace('&amp;','&') } )
                    scraperwiki.datastore.save(["ccnum","record","year"], { "ccnum" : ccnum, "year" : year, "record" : record+3, "type" : "Cost of Fundraising"})
                    scraperwiki.datastore.save(["ccnum","record","year"], { "ccnum" : ccnum, "year" : year, "record" : record+3, "title": t.text.replace('&amp;','&') } )
                elif i==1 or i==4 or i==7:
                    try:
                        income = long(re.sub(r'[^0-9]', '', t.text))
                        scraperwiki.datastore.save(["ccnum","record","year"], { "ccnum" : ccnum, "year" : year, "record" : record, "value": income})
                    except ValueError:
                        continue
                else:
                    try:
                        cost = long(re.sub(r'[^0-9]', '', t.text))
                        scraperwiki.datastore.save(["ccnum","record","year"], { "ccnum" : ccnum, "year" : year, "record" : record+3, "value": cost})
                    except ValueError:
                        continue
    except:
        print "account not found"
        continue

