# sqlite.save saved every row to conserve memory resources on ScraperWiki, when doing one big save the process would get killed
import scraperwiki
import lxml.html
import dateutil.parser

url = 'http://www.contractregistry.nt.ca/Public/ListProcurements.asp?Action=View&PageNumber=1&SearchType=%s&ResultsPerPage=500' # Type=Historical or Current

data = []

def bidDetails (row, bidroot, reference):
    for bidel in bidroot.cssselect("tr.%s" % row): # detailRow, detailRowAlt, detailRow strong
        biddata = []
        bidtds = bidel.cssselect("td")

        isWinning = "false"
        if len(bidel.find_class("strong")) == 1: # Make the bid as the winning bid if it is tagged as 'strong'/bold
            isWinning = "true"

        #print row, "  ", bidel.find_class("strong"), "  ", len(bidel.find_class("strong")), "  ", bidtds[0].text_content()

        # Three different bid data saves depending on how much info the GNWT has published, these three take into account all cases I've seen. Doesn't add row to db if it's a header row from the page
        if len(bidtds) > 2 and bidtds[0].text_content() != "Status" and bidtds[0].text_content() != "Bidder Name" and bidtds[0].text_content() != "Awarded" and bidtds[0].text_content() != "Closed":
            biddata.append({
             'Reference' : reference,
             'Bidder Name' : bidtds[0].text_content(),
             'Bid Price' : bidtds[1].text_content(),
             'NWT-Only Eligible Amount' : bidtds[2].text_content(),
             'NWT-Local Eligible Amount' : bidtds[3].text_content(),
             'Adjusted Bid Price' : bidtds[4].text_content(),
             'Contract Amount' : bidtds[5].text_content(),
             'Winning': isWinning
            })
        elif len(bidtds) == 2 and bidtds[0].text_content() != "Status" and bidtds[0].text_content() != "Bidder Name" and bidtds[0].text_content() != "Awarded" and bidtds[0].text_content() != "Closed":
            biddata.append({
             'Reference' : reference,
             'Bidder Name' : bidtds[0].text_content(),
             'Contract Amount' : bidtds[1].text_content(),
             'Winning': isWinning
            })
        elif len(bidtds) == 1 and bidtds[0].text_content() != "Status" and bidtds[0].text_content() != "Bidder Name" and bidtds[0].text_content() != "Awarded" and bidtds[0].text_content() != "Closed":
            biddata.append({
             'Reference' : reference,
             'Bidder Name' : bidtds[0].text_content(),
             'Winning': isWinning
            })

        #if isWinning == "true":
        #    print bidtds[0].text_content()
        scraperwiki.sqlite.save(['Reference','Bidder Name'], biddata, table_name="bids", verbose=1)

def readRFPs (row, root):    
    for el in root.cssselect("tr.%s" % row):
        data = []
        tds = el.cssselect("td")
        if tds[0].text_content() != "Status":
            # Format closing date as a date
            closingdate = tds[6].text_content()
            closingdate = closingdate.replace(u"\xa0", " ")
            data.append({
                'Status' : tds[0].text_content(),
                'Reference' : tds[1].text_content(),
                'Type' : tds[2].text_content(),
                'Title' : tds[3].text_content(),
                'Location' : tds[4].text_content(),
                'Department' : tds[5].text_content(),
                'Closing Date' : dateutil.parser.parse(closingdate)
            })
            scraperwiki.sqlite.save(['Reference'], data, verbose=1)

            # If RFP has been closed or awarded then attempt to scrape bid information
            if tds[0].text_content() == "Awarded" or tds[0].text_content() == "Closed":
                bidurl = 'http://www.contractregistry.nt.ca/Public/ViewBidDetails.asp?Action=View&Procurement_ID=%s'
                bidhtml = scraperwiki.scrape(bidurl % tds[1].text_content())
                bidroot = lxml.html.fromstring(bidhtml)

                bidDetails("detailRow",bidroot,tds[1].text_content())
                bidDetails("detailRowAlt",bidroot,tds[1].text_content())


# Main Function

#scraperwiki.sqlite.execute("CREATE TABLE `bids` (`Reference` text, `Bidder Name` text, `Bid Price` text, `NWT-Only Eligible Amount` text, `NWT-Local Eligible Amount` text, `Adjusted Bid Price` text,  `Contract Amount` text, `Winning` text)")

# run this twice (once for current rfps, once against the historical rfps)
for type in range (1,3):
    if type == 1:
        html = scraperwiki.scrape(url % ('Current'))
    else:
        html = scraperwiki.scrape(url % ('Historical'))

    root = lxml.html.fromstring(html) 
    readRFPs("detailRow", root) # step through the form once with detailRow and again with alternate coloured row (detailRowAlt)
    readRFPs("detailRowAlt", root)

#http://www.contractregistry.nt.ca/Public/ViewPublicNotice.asp?Action=View&Procurement_ID=PM014313 # RFP Details
#http://www.contractregistry.nt.ca/Public/ViewBidDetails.asp?Action=View&Procurement_ID=AC433336 # Bid Details

#print data
#scraperwiki.sqlite.save(['Reference'], data)

#import lxml.html
#root = lxml.html.fromstring(html)
#for tr in root.cssselect("div[align='left'] tr"): 
#    tds = tr.cssselect("td")
#    if len(tds)==12:
#        data = { 'country' : tds[0].text_content(), 'years_in_school' : int(tds[4].text_content()) }
#        print data 
