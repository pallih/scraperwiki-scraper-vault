# 20110629 Working on a scraper to get all UK railway stations by category

import scraperwiki
import urllib
import xlrd
import re
import sys
import lxml.html




def ScrapeXL(xlurl):
    content = urllib.urlopen(xlurl).read()
    book = xlrd.open_workbook(file_contents=content)
    sheetnames = book.sheet_names()
    print xlurl, sheetnames, [ (sheet.ncols, sheet.nrows)  for sheet in book.sheets() ]

    sheet = None
    for sheetname in ['Station Usage 2009-10 v1', 'Station Usage 2008-09 v3.3', 'Data']:
        if sheetname in sheetnames:
            sheet = book.sheet_by_name(sheetname)
            break
    assert sheet

    headers = [ ]
    for header in sheet.row_values(0):
        lheader = re.sub("\s+", " ", header)
        lheader = re.sub("&", "and", lheader)
        lheader = re.sub(" \(GOR\)", "", lheader)
        lheader = re.sub("\d\d\d\d\s+", "", lheader)
        headers.append(lheader)
    print headers

    assert headers == [u'NLC', u'TLC', u'Station Name', u'Government Office Region', u'County or Unitary Authority', u'District or Unitary Authority', u'NUTS2 Spatial Unit Code', u'NUTS2 Spatial Unit', u'Station Facility Owner', u'Station Group', u'PTE Urban Area Station', u'London Travelcard Area', u'London Joint Station', u'Entries Full', u'Entries Reduced', u'Entries Season', u'Entries Total', u'Exits Full', u'Exits Reduced', u'Exits Season', u'Exits Total', u'Entries and Exits', u'Entries and Exits', u'Interchanges', u'Check', u'Check Detail', u'Check Reason'], headers

    ldata = [ ]
    for j in range(1, sheet.nrows):
        if sheet.cell(j, 0).value:
            data = dict(zip(headers, sheet.row_values(j)))
            data["nrow"] = j
            data["url"] = xlurl
            data["sheetname"] = sheetname
            ldata.append(data)
    scraperwiki.sqlite.save(unique_keys=["sheetname", "url", "TLC"], data=ldata)



root = lxml.html.parse("http://www.rail-reg.gov.uk/server/show/nav.1529").getroot()
for a in root.cssselect("div.bodyText a"):
    xlurl = a.attrib.get("href")
    if xlurl[-4:] != ".xls":
        continue
    if scraperwiki.sqlite.get_var(xlurl, False):
        continue
    try:
        ScrapeXL(xlurl)
        scraperwiki.sqlite.save_var(xlurl, True)
    except TypeError, e:
        print e
    
    


def ScrapeORR():
    railuseurl = "http://www.rail-reg.gov.uk/upload/xls/station_usage_0910.xls"
    book = xlrd.open_workbook(file_contents=urllib.urlopen(railuseurl).read())
    sheet = list(book.sheets())[1]
    
    headers = [ ]
    for header in sheet.row_values(0):
        lheader = re.sub("&", "and", header)
        lheader = re.sub("\s+", " ", lheader)
        lheader = re.sub("\(|\)", "", lheader)
        headers.append(lheader)
    print headers
    
    
    for row in range(1, sheet.nrows):
        values = sheet.row_values(row)
        if values[0]:
            data = dict(zip(headers, values))
            scraperwiki.sqlite.save(unique_keys=["TLC"], data=data, verbose=0)

#########################################################################################


def ScrapeRailStationCategories():
    railuseurl = "http://en.wikipedia.org/wiki/Category:DfT_Category_A_stations"
#    railuseurl = http://www.rail-reg.gov.uk/upload/xls/station_usage_0910.xls
#    book = xlrd.open_workbook(file_contents=urllib.urlopen(railuseurl).read())
#    sheet = list(book.sheets())[1]
    
#    headers = [ ]
#    for header in sheet.row_values(0):
#        lheader = re.sub("&", "and", header)
#        lheader = re.sub("\s+", " ", lheader)
#        lheader = re.sub("\(|\)", "", lheader)
#        headers.append(lheader)
#    print headers
    
    
#    for row in range(1, sheet.nrows):
#        values = sheet.row_values(row)
#        if values[0]:
#            data = dict(zip(headers, values))
#            scraperwiki.sqlite.save(unique_keys=["TLC"], data=data, verbose=0)


#print scraperwiki.sqlite.select("TLC from swdata")

from BeautifulSoup import BeautifulSoup


record = {}
unique_record_id = 0
stationName_db ={}
stationName_db = []

print tlc_db

CatACount = 21 # will hard code these constants for how many stations are in each category

for stationName in stationName_db:
    print "=============================="
    url_start = 'http://en.wikipedia.org/wiki'
    url_end = '/Category:DfT_Category_A_stations'
    starting_url = url_start + url_end
    print starting_url
        
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object

    print html

    dts = soup.findAll('dt') # get all the <dt> tags that show the variable name
    dds = soup.findAll('dd') # get all the <dd> tags that show the variable value
    i2=0

    for dt in dts:
        print unique_record_id
        print dt
        record ['id']= unique_record_id
        record ['station_code']=tlc
        record ['station_var']= dts [i2].text
        record ['station_val']= dds [i2].text
    #    print database, '------------'
    #    scraperwiki.metadata.save('data_columns', ['id', 'station_var', 'station_val'])
        scraperwiki.datastore.save(['id'],record) # save the records one by one
    
        i2=i2+1
        unique_record_id=unique_record_id+1                    
