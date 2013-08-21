import scraperwiki
import requests
import openpyxl
import tempfile
import time
import pprint

BASEURL = 'http://www.parliament.uk/'
URL = 'http://www.parliament.uk/business/lords/whos-in-the-house-of-lords/house-of-lords-expenses/'
#set a variable for the spreadsheet location
XLS = 'http://www.parliament.uk/documents/lords-finance-office/2012-13/allowances-expenses-2012-13-month-10-january-2013.xlsx'

def getworkbook(url):
    # Loads an xlsx file from the internet
    raw = requests.get(url, verify=False).content
    f = tempfile.NamedTemporaryFile('wb')
    f.write(raw)
    f.seek(0)
    wb = openpyxl.load_workbook(f.name)
    f.close()
    return wb

def getdata(wb, sheet='Sheet1'):
    #Turn a sheet on a workbook into an array
    data = wb.get_sheet_by_name(sheet)
    return [[unicode(cell.value).strip() for cell in row] for row in data.rows]

def import_data():
    wb = getworkbook('http://www.parliament.uk/documents/lords-finance-office/2012-13/allowances-expenses-2012-13-month-10-january-2013.xlsx')
    
    rows = getdata(wb, 'Sheet1')
    pprint.pprint(rows)

    local_authorities = []
#NEED TO GRAB HEADINGS FROM ROW 6

    for i in range(7,805):
        print rows[i][0]
        local_authorities.append({
            'name': rows[i][0],
            'additionalinfo': rows[i][1],
            'addressarea': rows[i][2],
            'daysattended': rows[i][3],
            'daysaway': rows[i][4],
            'dailyallowance': rows[i][5],
            'travelcosts': rows[i][6],
            'travelonParlBus': rows[i][7],
            'EUdevolvedTravel': rows[i][8],
            'car': rows[i][9],
            'rail_ferry_coach': rows[i][10],
            'air': rows[i][11]
            })
    scraperwiki.sqlite.save(['name'], local_authorities, 'local_authorities')


import_data()