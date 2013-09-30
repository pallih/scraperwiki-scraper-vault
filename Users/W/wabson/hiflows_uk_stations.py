import datetime
import scraperwiki
import xlrd

keys = [ 'ceh_number', 'watercourse', 'location', 'nominal_area', 'gauging_authority_or_region', 'annual_maxima_file', 'pot_file', 'catchment_descriptors_file', 'easting', 'northing', 'ngr', 'status', 'ok_qmed', 'ok_pooling' ]
unique_keys = [ 'ceh_number' ]

data_items = []

def main():
    xlbin = scraperwiki.scrape("http://www.environment-agency.gov.uk/static/documents/Research/List_of_stations_v3.1.2.xls")
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0)

    columns = get_columns(sheet)
    if not check_columns(columns):
        raise Exception('Column list not as expected!')

    for rownumber in range(11, sheet.nrows):
        # create dictionary of the row values
        values = [ cellval(c, book.datemode) for c in sheet.row(rownumber) ]

        # Remove empty cell which seems to be present on all rows, corresponding to the update date
        #if len(values) == 7 and values[6] is None:
        #    del values[6]

        # Only save if there are enough values
        if len(values) == len(keys):
            data = dict(zip(keys, values))

            data['easting'] = float(data['easting']) / 10
            data['northing'] = float(data['northing']) / 10
            data['ceh_number'] = str(data['ceh_number'])

            # Convert to latlng from northing and easting
            latlng = scraperwiki.geo.os_easting_northing_to_latlng(data['easting'], data['northing'])
            data['latlng_lat'] = latlng[0]
            data['latlng_lng'] = latlng[1]

            # only save if it is a full row (rather than a blank line or a note)
            if data['ceh_number']:
                data_items.append(data)
            else:
                print 'WARNING: Not enough values on row %s' % (rownumber)
        else:
            print 'WARNING: Not enough values on row %s' % (rownumber)

    #scraperwiki.sqlite.save_var('last_updated', updated_str)
    scraperwiki.sqlite.save(unique_keys=unique_keys, data=data_items)

def check_columns(columns):
    for n in range(0, len(columns)):
        if columns[n] != keys[n]:
            return False
    return True

def get_columns(sheet):
    return [c.partition('(')[0].strip().lower().replace(' ', '_').replace('?', '') for c in sheet.row_values(10)]

def get_last_updated(sheet):
    return sheet.cell(0,6)

def cellval(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_DATE:
        datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
        if datetuple[3:] == (0, 0, 0):
            return datetime.date(datetuple[0], datetuple[1], datetuple[2])
        return datetime.date(datetuple[0], datetuple[1], datetuple[2], datetuple[3], datetuple[4], datetuple[5])
    if cell.ctype == xlrd.XL_CELL_EMPTY:
        return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:
        return cell.value == 1
    return cell.value

main()
import datetime
import scraperwiki
import xlrd

keys = [ 'ceh_number', 'watercourse', 'location', 'nominal_area', 'gauging_authority_or_region', 'annual_maxima_file', 'pot_file', 'catchment_descriptors_file', 'easting', 'northing', 'ngr', 'status', 'ok_qmed', 'ok_pooling' ]
unique_keys = [ 'ceh_number' ]

data_items = []

def main():
    xlbin = scraperwiki.scrape("http://www.environment-agency.gov.uk/static/documents/Research/List_of_stations_v3.1.2.xls")
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0)

    columns = get_columns(sheet)
    if not check_columns(columns):
        raise Exception('Column list not as expected!')

    for rownumber in range(11, sheet.nrows):
        # create dictionary of the row values
        values = [ cellval(c, book.datemode) for c in sheet.row(rownumber) ]

        # Remove empty cell which seems to be present on all rows, corresponding to the update date
        #if len(values) == 7 and values[6] is None:
        #    del values[6]

        # Only save if there are enough values
        if len(values) == len(keys):
            data = dict(zip(keys, values))

            data['easting'] = float(data['easting']) / 10
            data['northing'] = float(data['northing']) / 10
            data['ceh_number'] = str(data['ceh_number'])

            # Convert to latlng from northing and easting
            latlng = scraperwiki.geo.os_easting_northing_to_latlng(data['easting'], data['northing'])
            data['latlng_lat'] = latlng[0]
            data['latlng_lng'] = latlng[1]

            # only save if it is a full row (rather than a blank line or a note)
            if data['ceh_number']:
                data_items.append(data)
            else:
                print 'WARNING: Not enough values on row %s' % (rownumber)
        else:
            print 'WARNING: Not enough values on row %s' % (rownumber)

    #scraperwiki.sqlite.save_var('last_updated', updated_str)
    scraperwiki.sqlite.save(unique_keys=unique_keys, data=data_items)

def check_columns(columns):
    for n in range(0, len(columns)):
        if columns[n] != keys[n]:
            return False
    return True

def get_columns(sheet):
    return [c.partition('(')[0].strip().lower().replace(' ', '_').replace('?', '') for c in sheet.row_values(10)]

def get_last_updated(sheet):
    return sheet.cell(0,6)

def cellval(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_DATE:
        datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
        if datetuple[3:] == (0, 0, 0):
            return datetime.date(datetuple[0], datetuple[1], datetuple[2])
        return datetime.date(datetuple[0], datetuple[1], datetuple[2], datetuple[3], datetuple[4], datetuple[5])
    if cell.ctype == xlrd.XL_CELL_EMPTY:
        return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:
        return cell.value == 1
    return cell.value

main()
