"""    
Obtains Halifax House Price Data

The .xls file was found linked to at:
  http://www.lloydsbankinggroup.com/media/excel/04_06_10_historic_data.xls
"""

from scraperwiki import sqlite, scrape, metadata
from pygooglechart import SimpleLineChart
import xlrd

def process (name, date):
    newdate = date[8:10] + "_" + date[5:7] + "_" + date[0:4]
    url = r"http://www.lloydsbankinggroup.com/media/excel/2010/%s_historic_data.xls" % newdate
    print url
    url = r"http://www.lloydsbankinggroup.com/media/excel/2010/04_06_10_historic_data.xls"
    book = xlrd.open_workbook(file_contents=scrape(url))
    sheet = book.sheet_by_name (name)
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    data = []
    i = 1
    while i < 500:
        try:
            month = sheet.cell_value (i, 0)
            year  = sheet.cell_value (i, 1)
            level = sheet.cell_value (i, 2)
        except:
            break
        when= "%04d-%02d-01" % (int(year), months.index (month) + 1)
        i = i + 1
        data.append (level)        
        sqlite.save(unique_keys=["Date"], data={"Date":when, "Index":level})

    chart = SimpleLineChart(500, 255, y_range=[0, 700])
    chart.add_data (data)
    metadata.save("chart", chart.get_url())

def main():
    process ('AllMon(NSA)', '2010-06-04')
    
main()
"""    
Obtains Halifax House Price Data

The .xls file was found linked to at:
  http://www.lloydsbankinggroup.com/media/excel/04_06_10_historic_data.xls
"""

from scraperwiki import sqlite, scrape, metadata
from pygooglechart import SimpleLineChart
import xlrd

def process (name, date):
    newdate = date[8:10] + "_" + date[5:7] + "_" + date[0:4]
    url = r"http://www.lloydsbankinggroup.com/media/excel/2010/%s_historic_data.xls" % newdate
    print url
    url = r"http://www.lloydsbankinggroup.com/media/excel/2010/04_06_10_historic_data.xls"
    book = xlrd.open_workbook(file_contents=scrape(url))
    sheet = book.sheet_by_name (name)
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    data = []
    i = 1
    while i < 500:
        try:
            month = sheet.cell_value (i, 0)
            year  = sheet.cell_value (i, 1)
            level = sheet.cell_value (i, 2)
        except:
            break
        when= "%04d-%02d-01" % (int(year), months.index (month) + 1)
        i = i + 1
        data.append (level)        
        sqlite.save(unique_keys=["Date"], data={"Date":when, "Index":level})

    chart = SimpleLineChart(500, 255, y_range=[0, 700])
    chart.add_data (data)
    metadata.save("chart", chart.get_url())

def main():
    process ('AllMon(NSA)', '2010-06-04')
    
main()
