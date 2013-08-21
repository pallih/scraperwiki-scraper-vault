import scraperwiki
import urllib2
from BeautifulSoup import BeautifulStoneSoup
import re,string,time
from datetime import datetime

queryPage  = "http://services2.hdb.gov.sg/webapp/BB33RTIS/BB33PReslTrans.jsp"
searchPage = "http://services2.hdb.gov.sg/webapp/BB33RTIS/BB33SSearchWidget"

datePeriodsToScrape     = 2  # In case there's incomplete entries for the most recent month
retriesOnNetworkFailure = 3


# Retry connections for temporary network issues to prevent exceptions during long scrape sessions
def scrape(url, params=None, level=0):
    try:
        return scraperwiki.scrape(url,params)
    except urllib2.URLError, e:
        if level == retriesOnNetworkFailure:
            raise
        else:
            print "Error downloading %s. Retrying in 30s.." % url
            time.sleep(30)
            return scrape(url,params,level+1)


# Get a list of searchable flat types, locations and time periods
def getParams():
    query = scrape(queryPage)
    querySoup = BeautifulStoneSoup(query,convertEntities=BeautifulStoneSoup.HTML_ENTITIES)

    flatTypes = [(tag['value'],tag.contents[0]) for tag in querySoup.find('select', {'name':'FLAT_TYPE'}  ).findAll('option') if len(tag['value'])>0]
    towns      = [tag['value'] for tag in querySoup.find('select', {'name':'NME_NEWTOWN'}).findAll('option') if len(tag['value'])>0]
    dates      = [tag['value'] for tag in querySoup.find('select', {'name':'DTE_APPROVAL_FROM'}).findAll('option') if len(tag['value'])>0]
    return (dict(flatTypes), towns, dates)

def getTextFromCell(cell):
    try:
        return getTextFromCell(cell.contents[0])
    except AttributeError:
        return cell.strip()


print "Scraping started at %s" % datetime.now().strftime("%a %Y-%m-%d %H:%M")
# Search for all possible data from the HDB website
(flatTypeList, townList, dateList) = getParams()

townList.sort()
dateList = sorted(dateList, reverse=True)[0:datePeriodsToScrape]

###
# Uncomment to limit the scrape parameters
#  In particular, use the dateList override to fill older date periods as the scraper
#  takes too long in one go (about 20-30 minutes per date period)
#
#flatTypeList  = dict({"01":"1 Room","02":"2 Room","03":"3 Room","04":"4 Room","05":"5 Room","06":"Executive","07":"HUDC","08":"Multi-Generation"})
#flatTypeList  = dict({"03":"3 Room"})
#townList       = ["CT      Central Area"]
#dateList       = ["201202"]
###

dataTableAlreadyExists = ("swdata" in scraperwiki.sqlite.show_tables())
for date in dateList:
    print "Scraping datecode %s started at %s" % (date, datetime.now().strftime("%a %Y-%m-%d %H:%M"))
    for town in townList:
        for flatType in sorted(flatTypeList.keys()):
            entryNumber = 1
            postParams = [ ("site", "hdb"),
                            ("q", ""),
                            ("filter_s", "Within+HDB+Website#hdb|Within+All+Government+Websites#default|"),
                            ("feedback_url", "https://services2.hdb.gov.sg/webapp/BE05Feedback/BE05SFrontController?service=ServiceFeedback"),
                            ("operation", "createFeedback"),
                            ("contact_url", "http://www.hdb.gov.sg/fi10/fi10296p.nsf/WPDis/Contact+UsOverview?OpenDocument"),
                            ("client", "default"),
                            ("proxystylesheet", "default"),
                            ("output", "xml_no_dtd"),
                            ("Process", "continue"),
                            ("FLAT_TYPE", flatType),
                            ("NME_NEWTOWN", town),
                            ("NME_STREET", ""),
                            ("NUM_BLK_FROM", ""),
                            ("NUM_BLK_TO", ""),
                            ("AMT_RESALE_PRICE_FROM", ""),
                            ("AMT_RESALE_PRICE_TO", ""),
                            ("DTE_APPROVAL_FROM", date),
                            ("DTE_APPROVAL_TO", date)]

            searchResults = scrape(searchPage,postParams)
            searchSoup = BeautifulStoneSoup(searchResults,convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
            errorList = searchSoup.findAll('td',{'class':"svcErrorMsg"})
            rowList = searchSoup.findAll('tr',{'class':re.compile('svcTableRow.*')})
            if len( errorList ) == 0 and len(rowList) > 0:
                # Clear old entries for these scrape parameters so if there's
                # inconsistent data we'll just refresh with the new scrape
                if dataTableAlreadyExists or "swdata" in scraperwiki.sqlite.show_tables():
                    scraperwiki.sqlite.execute( "DELETE FROM swdata WHERE Date=? AND Town=? AND FlatType=?", (date,town,flatTypeList[flatType]))
                    dataTableAlreadyExists = True
                    
                for row in rowList:
                    #print "entries = %s", [getTextFromCell(cell) for cell in row.findAll('td') ]
                    entries = [getTextFromCell(cell) for cell in row.findAll('td') ]
                    data = dict( [ ("Date",date),
                                   ("Town",town),
                                   ("EntryNum",entryNumber),
                                   ("FlatType",flatTypeList[flatType]),
                                   ("Block",entries[0]),
                                   ("Street",entries[1]),
                                   ("Floor",entries[2]),
                                   ("Area",entries[3]),
                                   ("YearConstructed",entries[4]),
                                   ("Price",entries[5]) ] )
                    scraperwiki.sqlite.save(['Date','Town','FlatType','EntryNum'], data)
                    entryNumber+=1
            else:
                if ( re.search("no matching records found", errorList[0].contents[0], re.IGNORECASE) ):
                    print "No records found for %s, %s, %s" % (date, town, flatTypeList[flatType])
                else:
                    raise UserWarning, "Unspecified error found in return result: %s" % errorList[0].contents[0]
print "Scraping finished at %s" % (datetime.now().strftime("%a %Y-%m-%d %H:%M"))

