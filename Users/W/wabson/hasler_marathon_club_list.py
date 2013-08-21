import datetime
import scraperwiki
import xlrd

keys = [ 'name', 'code', 'region_code' ]
unique_keys = [ 'code' ]

def main():
    xlbin = scraperwiki.scrape("http://dl.dropbox.com/u/55716759/hrmTemplate.xlt")
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_name('Clubs')

    for rownumber in range(0, sheet.nrows):
        # create dictionary of the row values
        values = [ cellval(sheet.cell(rownumber, c), book.datemode) for c in range(0, 3) ]

        # Only save if there are enough values
        if len(values) == len(keys):
            data = dict(zip(keys, values))

            # only save if it is a full row (rather than a blank line or a note)
            if data['name'] != None and data['code'] != None:
                scraperwiki.sqlite.save(unique_keys=unique_keys, data=data)
            else:
                print 'WARNING: Not enough values on row %s' % (rownumber)
        else:
            print 'WARNING: Not enough values on row %s' % (rownumber)

def cellval(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_EMPTY:
        return None
    return cell.value

main()