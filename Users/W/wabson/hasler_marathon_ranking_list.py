import datetime
import scraperwiki
import xlrd

keys = [ 'surname', 'first_name', 'club', 'class', 'bcu_number', 'division' ]
unique_keys = [ 'surname', 'first_name', 'club', 'class' ]

def main():
    #xlbin = scraperwiki.scrape("http://dl.dropboxusercontent.com/u/22425821/RankingList.xls")
    xlbin = scraperwiki.scrape("http://www.marathon-canoeing.org.uk/marathon/media/RankingList.xls")
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0)
    datarows = []

    columns = get_columns(sheet)
    if not check_columns(columns):
        raise Exception('Column list not as expected!')

    updated = cellval(get_last_updated(sheet), book.datemode)
    updated_str = '%s-%s-%s' % (updated.year, updated.month, updated.day)

    for rownumber in range(1, sheet.nrows):
        # create dictionary of the row values
        values = [ cellval(c, book.datemode) for c in sheet.row(rownumber) ]

        # Remove empty cell which seems to be present on all rows, corresponding to the update date
        if len(values) == 7 and values[6] is None:
            del values[6]

        # Only save if there are enough values
        if len(values) == len(keys):
            data = dict(zip(keys, values))
            data['updated'] = updated_str

            # Division/BCU number seem to be read as a real number when numeric (e.g. 4.0 not 4)
            if data['division'] is not None and isinstance(data['division'], float):
                data['division'] = str(int(data['division']))
            if data['bcu_number'] is not None and isinstance(data['bcu_number'], float):
                data['bcu_number'] = str(int(data['bcu_number']))

            # Set club to empty string value (cannot be None since it is part of the unique key)
            if data['club'] is None:
                data['club'] = ''

            # only save if it is a full row (rather than a blank line or a note)
            if data['surname'] != None and data['first_name'] != None:
                datarows.append(data)
            else:
                print 'WARNING: Not enough values on row %s' % (rownumber)
        else:
            print 'WARNING: Not enough values on row %s' % (rownumber)

    scraperwiki.sqlite.save(unique_keys=unique_keys, data=datarows)

    scraperwiki.sqlite.save_var('last_updated', updated_str)

def check_columns(columns):
    for n in range(0, len(columns)):
        if columns[n] != keys[n]:
            return False
    return True

def get_columns(sheet):
    return [c.strip().lower().replace(' ', '_') for c in sheet.row_values(0)[0:6]]

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

keys = [ 'surname', 'first_name', 'club', 'class', 'bcu_number', 'division' ]
unique_keys = [ 'surname', 'first_name', 'club', 'class' ]

def main():
    #xlbin = scraperwiki.scrape("http://dl.dropboxusercontent.com/u/22425821/RankingList.xls")
    xlbin = scraperwiki.scrape("http://www.marathon-canoeing.org.uk/marathon/media/RankingList.xls")
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0)
    datarows = []

    columns = get_columns(sheet)
    if not check_columns(columns):
        raise Exception('Column list not as expected!')

    updated = cellval(get_last_updated(sheet), book.datemode)
    updated_str = '%s-%s-%s' % (updated.year, updated.month, updated.day)

    for rownumber in range(1, sheet.nrows):
        # create dictionary of the row values
        values = [ cellval(c, book.datemode) for c in sheet.row(rownumber) ]

        # Remove empty cell which seems to be present on all rows, corresponding to the update date
        if len(values) == 7 and values[6] is None:
            del values[6]

        # Only save if there are enough values
        if len(values) == len(keys):
            data = dict(zip(keys, values))
            data['updated'] = updated_str

            # Division/BCU number seem to be read as a real number when numeric (e.g. 4.0 not 4)
            if data['division'] is not None and isinstance(data['division'], float):
                data['division'] = str(int(data['division']))
            if data['bcu_number'] is not None and isinstance(data['bcu_number'], float):
                data['bcu_number'] = str(int(data['bcu_number']))

            # Set club to empty string value (cannot be None since it is part of the unique key)
            if data['club'] is None:
                data['club'] = ''

            # only save if it is a full row (rather than a blank line or a note)
            if data['surname'] != None and data['first_name'] != None:
                datarows.append(data)
            else:
                print 'WARNING: Not enough values on row %s' % (rownumber)
        else:
            print 'WARNING: Not enough values on row %s' % (rownumber)

    scraperwiki.sqlite.save(unique_keys=unique_keys, data=datarows)

    scraperwiki.sqlite.save_var('last_updated', updated_str)

def check_columns(columns):
    for n in range(0, len(columns)):
        if columns[n] != keys[n]:
            return False
    return True

def get_columns(sheet):
    return [c.strip().lower().replace(' ', '_') for c in sheet.row_values(0)[0:6]]

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
