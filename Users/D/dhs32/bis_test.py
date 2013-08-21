import scraperwiki
import datetime
import xlrd
import urllib2
import sys
# Blank Python

KEYS = ['complaint_no', 'status', 'date_entered', 'address', 'bin', 'community_board', 'special_district', 'complaint_category', 'unit', 'disposition_date', 'disposition_code', 'inspection_date']


def _calc_url(targetdate):
    url = "http://www.nyc.gov/html/dob/downloads/excel/cb_complaint_%(month)02d%(day)02d%(year)02d.xls" % \
    {"month":targetdate.month, "day":targetdate.day, "year":int(str(targetdate.year)[-2:])}

    return url

def sheet_fetch(lastdate):
    for ii in range(1, 8):
        targetdate = lastdate + datetime.timedelta(ii)

        url = _calc_url(targetdate)

        try:
            xlbin = scraperwiki.scrape(url)
        except urllib2.HTTPError, err:
            # if is 404 error file not found we skip
            if err.getcode() == 404:
                continue #not a problem.  move on to next date.
            else:
                raise
        else:
            break
    try:
        book = xlrd.open_workbook(file_contents=xlbin)
    except UnboundLocalError, err:
        # xlbin doesn't exist.  no file available for download
        print("exiting: no file available for download")
        sys.exit(0)
    
    sheet = book.sheet_by_index(0)
    return book, sheet, targetdate

def cellval(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_DATE:
        datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
        if datetuple[3:] == (0, 0, 0):
            return datetime.date(datetuple[0], datetuple[1], datetuple[2])
        return datetime.date(datetuple[0], datetuple[1], datetuple[2], datetuple[3], datetuple[4], datetuple[5])
    if cell.ctype == xlrd.XL_CELL_EMPTY:    return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:  return cell.value == 1
    return cell.value


def data_scrape(book, sheet, targetdate):
    datalist = []
    for ii in range(3, sheet.nrows):           
        # create dictionary of the row values
        values = [ cellval(c, book.datemode) for c in sheet.row(ii) ]
        data = dict(zip(KEYS, values))
        data["date_sourcefile"] = targetdate.isoformat()

        # check that complaint_no is not None.
        if data["complaint_no"]:
            datalist.append(data)
    
        # only save if it is a full row (rather than a blank line or a note)
    if data['complaint_no'] != None:
        scraperwiki.sqlite.save(unique_keys=['complaint_no'], data=datalist)
    



def runner(lastdate=None):
    print "in runner lastdate: ", lastdate
    if not lastdate:
        lastdate = scraperwiki.sqlite.get_var("lastdate")
        lastdate = datetime.datetime.strptime(lastdate, "%Y-%m-%d %H:%M:%S")
        print "get_var lastdate fetch: ", lastdate

    book, sheet, targetdate = sheet_fetch(lastdate = lastdate)
    print targetdate
    print "start of data scrape"
    data_scrape(book, sheet, targetdate)
    print "end of data_scrape"
    scraperwiki.sqlite.save_var("lastdate", targetdate.isoformat(" "))
    return targetdate

#lastdate = datetime.datetime(2005,6,3)
#scraperwiki.sqlite.save_var("lastdate", lastdate.isoformat(" "))    

lastdate = None
#for ii in range(200):
while 1:
    print "in loop lastdate", lastdate
    lastdate= runner(lastdate)
#    runner()
