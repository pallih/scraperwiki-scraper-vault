import scraperwiki
import xlrd

print dir(scraperwiki.geo)


def nlud_scrape(url):
    data = scraperwiki.scrape(url)
    
    book = xlrd.open_workbook(file_contents=data)
    sheet = book.sheets()[1]
    
    columns = list(sheet.row_values(0))
    
    for i in range(2, sheet.nrows):
        row = sheet.row_values(i)
        data = dict(zip(columns, row))
        easting = data.pop("EASTING")
        northing = data.pop("NORTHING")
        latlng = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
        uk = list(data.keys())
        data["latlng_lat"] = latlng[0]
        data["latlng_lng"] = latlng[1]
        scraperwiki.sqlite.save(unique_keys=uk, data=data, verbose=0, commit=False)
    scraperwiki.sqlite.commit()

nlud_scrape("http://www.islington.gov.uk/DownloadableDocuments/CouncilandDemocracy/xls/20100601-June_spend.xls")
