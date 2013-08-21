import urllib
import csv
import scraperwiki
import re
import datetime
import time

# fill in the input file here
def gp_scrape(url):

    lines = urllib.urlopen(url).readlines()
    #print lines[:9]
    clist = list(csv.reader(lines))
    #print clist[:9]
    while clist[0][1] == "":
        #print "Discarding", clist[0]
        clist.pop(0)

    header = clist.pop(0)   # set 'header' to be the first row of the CSV file
    result = [ dict(zip(header, row))  for row in clist ]

    for i, row in enumerate(clist[:]):
        #print dict(zip(header, row))
    #Uncomment these two lines to store in ScraperWiki datastore
        #unique_keys = header # Change this to the fields that uniquely identify a row
        data = dict(zip(header, row))
        #print data
        if type(data["Amount"]) in [str, unicode]: 
            data["Amount"] = float(re.sub(",", "", data["Amount"]))
        data["Date"] = datetime.datetime(*time.strptime(data["Date"],"%d/%m/%Y")[:3]) 
        data["url"] = url
        data["rownumber"] = i+1
        print data
        scraperwiki.datastore.save(["url", "rownumber"], data)

gp_scrape("http://www.ncuh.nhs.uk/about-us/trust-expenditure/csv/2011/february.csv")
gp_scrape("http://www.wirral.nhs.uk/document_uploads/Expenditure/Feb2011Payments.csv")
#gp_scrape("http://www.kirklees.nhs.uk/fileadmin/documents/publications/Expenditure_over_25000/Nov_10_-_Expenditure_Over_pound25K..csv")
#gp_scrape("http://www.gywpct.nhs.uk/_store/documents/transparency-report-dec-2010.csv")
#gp_scrape("http://www.ealingpct.nhs.uk/Library/publications/EPCT-Oct-2010.csv")
