import xlrd    
import scraperwiki
import datetime
import re
import json
import urllib2

# This dataset comes from the automatic energy meter readings collected by Liverpool City Council 
# every 15 minutes for all its public buildings.  
# As far as we know this information is never used and not published.  
# A sample of it was obtained through an FOI request.  
# Their first response was to send a scanned image of a printout.  
# Only on the second attempt did we get the Excel spreadsheet.
#     http://www.whatdotheyknow.com/request/automated_meter_reading_data


def Main():
    url = 'http://www.whatdotheyknow.com/request/39345/response/116473/attach/2/108731%20Lawson%20att1%20230910.xls'
    book = xlrd.open_workbook(file_contents=scraperwiki.scrape(url))
    sheet = book.sheet_by_index(0)
    print sheet
    
    headings = [ re.match('(\d\d):(\d\d)', sheet.cell(0, column).value).groups()  for column in range(1, sheet.ncols)]
    print headings

    for row in range(99, sheet.nrows):
        ldata = [ ]
        pdata = [ ]
        datecell = sheet.cell(row, 0)
        assert datecell.ctype == xlrd.XL_CELL_DATE
        d = xlrd.xldate_as_tuple(datecell.value, 0)
        datetimes = [ datetime.datetime(d[0], d[1], d[2], int(hour), int(minute))  for hour, minute in headings ]
        values = [sheet.cell(row, column).value  for column in range(1, sheet.ncols)]
        for t, v in zip(datetimes, values):
            ldata.append({"datetime":t, "energyuse":v})
            pdata.append({"at":t.isoformat(), "value":str(v)})
        #scraperwiki.sqlite.save(["datetime"], ldata)
        ppost = json.dumps({"datapoints":pdata})

        req = urllib2.Request(url="http://api.pachube.com/v2/feeds/43644/datastreams/energy/datapoints", data=ppost)
        req.add_header('X-PachubeApiKey', 'tp8XcXN8DOB224SryPBUJZx-MSBEoNtMjXt9LmUhsQQRCxmJ0_DqO-qVl2ncm5ttjQVDZCB5WyR21YEgihhGJdIfJHU96J5YdWPu85dDPCwN6-nP5nw45KJZyiSeSllR')
        try:
            pfin = urllib2.urlopen(req)
        except Exception, e:
            print "Noo", e, e.read()
            break
        print row, d, pfin.read()



Main()
                
# should make an annotated timelines per day from this and per hour of day, and throw it up
# in sqlite it would be easy to group by date and time to make these sums fall out
import xlrd    
import scraperwiki
import datetime
import re
import json
import urllib2

# This dataset comes from the automatic energy meter readings collected by Liverpool City Council 
# every 15 minutes for all its public buildings.  
# As far as we know this information is never used and not published.  
# A sample of it was obtained through an FOI request.  
# Their first response was to send a scanned image of a printout.  
# Only on the second attempt did we get the Excel spreadsheet.
#     http://www.whatdotheyknow.com/request/automated_meter_reading_data


def Main():
    url = 'http://www.whatdotheyknow.com/request/39345/response/116473/attach/2/108731%20Lawson%20att1%20230910.xls'
    book = xlrd.open_workbook(file_contents=scraperwiki.scrape(url))
    sheet = book.sheet_by_index(0)
    print sheet
    
    headings = [ re.match('(\d\d):(\d\d)', sheet.cell(0, column).value).groups()  for column in range(1, sheet.ncols)]
    print headings

    for row in range(99, sheet.nrows):
        ldata = [ ]
        pdata = [ ]
        datecell = sheet.cell(row, 0)
        assert datecell.ctype == xlrd.XL_CELL_DATE
        d = xlrd.xldate_as_tuple(datecell.value, 0)
        datetimes = [ datetime.datetime(d[0], d[1], d[2], int(hour), int(minute))  for hour, minute in headings ]
        values = [sheet.cell(row, column).value  for column in range(1, sheet.ncols)]
        for t, v in zip(datetimes, values):
            ldata.append({"datetime":t, "energyuse":v})
            pdata.append({"at":t.isoformat(), "value":str(v)})
        #scraperwiki.sqlite.save(["datetime"], ldata)
        ppost = json.dumps({"datapoints":pdata})

        req = urllib2.Request(url="http://api.pachube.com/v2/feeds/43644/datastreams/energy/datapoints", data=ppost)
        req.add_header('X-PachubeApiKey', 'tp8XcXN8DOB224SryPBUJZx-MSBEoNtMjXt9LmUhsQQRCxmJ0_DqO-qVl2ncm5ttjQVDZCB5WyR21YEgihhGJdIfJHU96J5YdWPu85dDPCwN6-nP5nw45KJZyiSeSllR')
        try:
            pfin = urllib2.urlopen(req)
        except Exception, e:
            print "Noo", e, e.read()
            break
        print row, d, pfin.read()



Main()
                
# should make an annotated timelines per day from this and per hour of day, and throw it up
# in sqlite it would be easy to group by date and time to make these sums fall out
import xlrd    
import scraperwiki
import datetime
import re
import json
import urllib2

# This dataset comes from the automatic energy meter readings collected by Liverpool City Council 
# every 15 minutes for all its public buildings.  
# As far as we know this information is never used and not published.  
# A sample of it was obtained through an FOI request.  
# Their first response was to send a scanned image of a printout.  
# Only on the second attempt did we get the Excel spreadsheet.
#     http://www.whatdotheyknow.com/request/automated_meter_reading_data


def Main():
    url = 'http://www.whatdotheyknow.com/request/39345/response/116473/attach/2/108731%20Lawson%20att1%20230910.xls'
    book = xlrd.open_workbook(file_contents=scraperwiki.scrape(url))
    sheet = book.sheet_by_index(0)
    print sheet
    
    headings = [ re.match('(\d\d):(\d\d)', sheet.cell(0, column).value).groups()  for column in range(1, sheet.ncols)]
    print headings

    for row in range(99, sheet.nrows):
        ldata = [ ]
        pdata = [ ]
        datecell = sheet.cell(row, 0)
        assert datecell.ctype == xlrd.XL_CELL_DATE
        d = xlrd.xldate_as_tuple(datecell.value, 0)
        datetimes = [ datetime.datetime(d[0], d[1], d[2], int(hour), int(minute))  for hour, minute in headings ]
        values = [sheet.cell(row, column).value  for column in range(1, sheet.ncols)]
        for t, v in zip(datetimes, values):
            ldata.append({"datetime":t, "energyuse":v})
            pdata.append({"at":t.isoformat(), "value":str(v)})
        #scraperwiki.sqlite.save(["datetime"], ldata)
        ppost = json.dumps({"datapoints":pdata})

        req = urllib2.Request(url="http://api.pachube.com/v2/feeds/43644/datastreams/energy/datapoints", data=ppost)
        req.add_header('X-PachubeApiKey', 'tp8XcXN8DOB224SryPBUJZx-MSBEoNtMjXt9LmUhsQQRCxmJ0_DqO-qVl2ncm5ttjQVDZCB5WyR21YEgihhGJdIfJHU96J5YdWPu85dDPCwN6-nP5nw45KJZyiSeSllR')
        try:
            pfin = urllib2.urlopen(req)
        except Exception, e:
            print "Noo", e, e.read()
            break
        print row, d, pfin.read()



Main()
                
# should make an annotated timelines per day from this and per hour of day, and throw it up
# in sqlite it would be easy to group by date and time to make these sums fall out
import xlrd    
import scraperwiki
import datetime
import re
import json
import urllib2

# This dataset comes from the automatic energy meter readings collected by Liverpool City Council 
# every 15 minutes for all its public buildings.  
# As far as we know this information is never used and not published.  
# A sample of it was obtained through an FOI request.  
# Their first response was to send a scanned image of a printout.  
# Only on the second attempt did we get the Excel spreadsheet.
#     http://www.whatdotheyknow.com/request/automated_meter_reading_data


def Main():
    url = 'http://www.whatdotheyknow.com/request/39345/response/116473/attach/2/108731%20Lawson%20att1%20230910.xls'
    book = xlrd.open_workbook(file_contents=scraperwiki.scrape(url))
    sheet = book.sheet_by_index(0)
    print sheet
    
    headings = [ re.match('(\d\d):(\d\d)', sheet.cell(0, column).value).groups()  for column in range(1, sheet.ncols)]
    print headings

    for row in range(99, sheet.nrows):
        ldata = [ ]
        pdata = [ ]
        datecell = sheet.cell(row, 0)
        assert datecell.ctype == xlrd.XL_CELL_DATE
        d = xlrd.xldate_as_tuple(datecell.value, 0)
        datetimes = [ datetime.datetime(d[0], d[1], d[2], int(hour), int(minute))  for hour, minute in headings ]
        values = [sheet.cell(row, column).value  for column in range(1, sheet.ncols)]
        for t, v in zip(datetimes, values):
            ldata.append({"datetime":t, "energyuse":v})
            pdata.append({"at":t.isoformat(), "value":str(v)})
        #scraperwiki.sqlite.save(["datetime"], ldata)
        ppost = json.dumps({"datapoints":pdata})

        req = urllib2.Request(url="http://api.pachube.com/v2/feeds/43644/datastreams/energy/datapoints", data=ppost)
        req.add_header('X-PachubeApiKey', 'tp8XcXN8DOB224SryPBUJZx-MSBEoNtMjXt9LmUhsQQRCxmJ0_DqO-qVl2ncm5ttjQVDZCB5WyR21YEgihhGJdIfJHU96J5YdWPu85dDPCwN6-nP5nw45KJZyiSeSllR')
        try:
            pfin = urllib2.urlopen(req)
        except Exception, e:
            print "Noo", e, e.read()
            break
        print row, d, pfin.read()



Main()
                
# should make an annotated timelines per day from this and per hour of day, and throw it up
# in sqlite it would be easy to group by date and time to make these sums fall out
