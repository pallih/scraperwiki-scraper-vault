# NORDKLIM locations
# 2010-11-02, David Jones, Climate Code Foundation.

import scraperwiki
# https://secure.simplistix.co.uk/svn/xlrd/trunk/xlrd/doc/xlrd.html
import xlrd

if 0: scraperwiki.sqlite.execute("drop table swdata;")
scraperwiki.sqlite.commit()
exit(0)

url = 'http://www.smhi.se/hfa_coord/nordklim/data/Nordklim_station_catalogue_v1_0_2002.xls'

def convertlatlon(s):
    """Convert a string of the form "56 46 N 08 19 E" to fractional
    (lat,lon) tuple."""
    
    dn,mn,ns,de,me,ew = s.split()
    lat = float(dn) + float(mn)/60
    lon = float(de) + float(me)/60
    if ns.lower() == 's':
        lat = -lat
    if ew.lower() == 'w':
        lon = -lon
    return lat,lon

def scrapeit(url):
    # Map from spreadsheet column index to NORDKLIM element.
    elementmap = None
    bytes = scraperwiki.scrape(url)
    xl = xlrd.open_workbook(file_contents=bytes)
    sheet = xl.sheet_by_index(0)
    for i in range(sheet.nrows):
        row = sheet.row(i)
        print row
        if not row[0].value:
            if not elementmap and row[1].value == u"Station name":
                elementmap = make_element_map(row)
            continue
        meta = dict(n=int(row[0].value), name=row[1].value,
          Elevation=row[2].value,
          country=row[3].value, nordklimid=int(row[4].value),
          loc=row[5].value)
        meta['id'] = meta['nordklimid']
        series = []
        for key,coli in elementmap.iteritems():
            # Extract start and stop years for the various elements.
            if row[coli].value:
                series.append(dict(id=meta['id'], element=key,
                    yearmin=int(row[coli].value),
                    yearmax=int(row[coli+1].value)))
        ll = convertlatlon(meta['loc'])
        meta.update(Latitude=ll[0], Longitude=ll[1])
        scraperwiki.sqlite.save(['id'], meta, table_name='meta')
        scraperwiki.sqlite.save(['id', 'element'], series, table_name='series')

def make_element_map(row):
    """Each NORDKLIM element (mean temp, sunshine, etc) is represented
    by a 3 figure number.  The numbers are featured in a particular
    row of the spreadsheet, which is how we know what column represents
    temperature.
    
    The meaning of each element is on this page:
    http://www.smhi.se/hfa_coord/nordklim/param.php
    """

    result = {}

    codes = dict(tmeanM=101, tmaxM=111, tminM=121)
    for key,code in codes.items():
        col = [i for i,cell in enumerate(row) if cell.value == code][0]
        result[key] = col
    return result


print __name__
if __name__ == 'scraper':
    scrapeit(url)
