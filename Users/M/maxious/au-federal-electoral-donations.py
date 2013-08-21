import csv
import mechanize 
import lxml.html
import scraperwiki

annDonorsurl = "http://periodicdisclosures.aec.gov.au/AnalysisDonor.aspx"

annReportingPeriods={"1998-1999":"1",
"1999-2000":"2",
"2000-2001":"3",
"2001-2002":"4",
"2002-2003":"5",
"2003-2004":"6",
"2004-2005":"7",
"2005-2006":"8",
"2006-2007":"9",
"2007-2008":"10",
"2008-2009":"23",
"2009-2010":"24",
"2010-2011":"48",
"2011-2012":"49",
}
for period, periodid in annReportingPeriods.items():
    br = mechanize.Browser()
    response = br.open(annDonorsurl)
    print "Loading data for "+period
    #print "All forms:", [ form.name  for form in br.forms() ]

    br.select_form(name="aspnetForm")
    #print br.form

    br['ctl00$dropDownListPeriod']=[periodid]
    response = br.submit("ctl00$buttonGo")
    response = br.open(annDonorsurl)

    br.select_form(name="aspnetForm")
    #br['ctl00$ContentPlaceHolderBody$dropDownListParties']=["0"]
    response = br.submit("ctl00$ContentPlaceHolderBody$analysisControl$buttonExport")

    br.select_form(name="aspnetForm")
    br['ctl00$ContentPlaceHolderBody$exportControl$dropDownListOptions']=['csv']
    response = br.submit("ctl00$ContentPlaceHolderBody$exportControl$buttonExport")
    
    lines = response.read().split("\n")
    clist = list(csv.reader(lines))
    
    title = clist.pop(0)
    dateupdated = clist.pop(0)
    headers = clist.pop(0)
    if "" in headers:
        headers.remove("")
    headers.append("ReportingPeriod")
    print "Period "+period+" %d columns and %d rows" %  (len(headers), len(clist))
    rows = []
    for row in clist:
        if len(row) == 9: 
            row.append(period) # "ReportingPeriod"
            #print dict(zip(headers, row))
            rows.append(dict(zip(headers, row)))
        else:
            print "Invalid row in "+period
            print dict(zip(headers, row))

    unique_keys =  ['DonorClientNm', 'RecipientClientNm', 'DonationDt'] # Change this to the fields that uniquely identify a row
    scraperwiki.sqlite.save(unique_keys, rows)