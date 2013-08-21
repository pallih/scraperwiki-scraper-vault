import xlrd
import string
from datetime import datetime
from time import time
import scraperwiki
from scraperwiki import scrape
from geopy import geocoders

url = "http://www.olcc.state.or.us/pdfs/licenses_by_type_excel.xls?" + str(time())
book = xlrd.open_workbook(file_contents=scrape(url))
licenses = book.sheet_by_index(0)
g = geocoders.Google()


data = []
for row in range(8, licenses.nrows):
    if licenses.cell(row, 2).value:
        # address, (lat, lng) = g.geocode(licenses.cell(row, 6).value + " " + licenses.cell(row, 7).value + " " + licenses.cell(row, 9).value + " " + licenses.cell(row, 10).value[:5])
        datum = {
            "license_number": int(licenses.cell(row, 0).value),
            "premises_number" : int(licenses.cell(row, 1).value),
            "expiration" : datetime(*xlrd.xldate_as_tuple(float(licenses.cell(row, 2).value), 0)),
            "tradename" : licenses.cell(row, 3).value,
            "licensee_name" : licenses.cell(row, 4).value,
            "license_type" : licenses.cell(row, 5).value,
            "address" : licenses.cell(row, 6).value,
            "city" : licenses.cell(row, 7).value,
            "county" : licenses.cell(row, 8).value,
            "state" : licenses.cell(row, 9).value,
            "zip" : licenses.cell(row, 10).value[:5],
            "phone" : licenses.cell(row, 11).value # ,
            # "lat" : lat,
            # "lng" : lng
        }
        data.append(datum)
        # print datum
scraperwiki.sqlite.save(["license_number"], data)