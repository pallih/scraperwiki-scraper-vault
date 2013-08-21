import itertools
import scraperwiki
import xlrd

url = "http://www.smhi.se/hfa_coord/nordklim/data/Nordklim_data_set_v1_0_2002.xls"

book = xlrd.open_workbook(file_contents=scraperwiki.scrape(url))

# use BeautifulSoup to get all <td> tags
sheet = book.sheets()[0]
print sheet.name
for id,rows in itertools.groupby((sheet.row(rownum) for rownum in xrange(sheet.nrows)), lambda row:int(row[0].value)):
    station = dict(id=id, tmean={})
    for row in rows:
        year = int(row[2].value)
        for i in range(1, 13):
            col = 2+i
            v = row[col].value
            key = "%s-%02d" % (year,i)
            if v == -9999:
                continue
            station['tmean'][key] = v / 10.0
        scraperwiki.datastore.save(['id'], station)
