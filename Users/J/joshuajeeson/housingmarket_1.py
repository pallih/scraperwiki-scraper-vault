import scraperwiki

import xlrd


try:
    scraperwiki.sqlite.execute("drop table housing_market")
except:
    pass

string_fields = ("area",)

int_fields = ("year",
              "bungalow",
              "detached",
              "semi",
              "terraced",
              "flatmaisonetteconverted",
              "flatmaisonetteoriginal",
              "alldwellings")

all_fields = ["%s string" % name for name in string_fields] + ["%s int" % name for name in int_fields]

scraperwiki.sqlite.execute("create table housing_market (%s)" % ', '.join(all_fields))

xlbin = scraperwiki.scrape("http://www.communities.gov.uk/documents/housing/xls/140990.xls")
book = xlrd.open_workbook(file_contents=xlbin)
sheet = book.sheet_by_index(0)

empty_row_count = 0


for row_num in range(8, sheet.nrows):
    row = sheet.row(row_num)
    
    # one empty row delimits an area, two empty rows is end of data
    if row[0].ctype == xlrd.XL_CELL_EMPTY:
        empty_row_count += 1
        if empty_row_count > 1:
            break
    else:
        empty_row_count = 0
        
        if row[0].ctype == xlrd.XL_CELL_TEXT:
            area = row[0].value
        else:
            del(row[1]) # remove empty column
            result = {}
            for i, field in enumerate(int_fields):
                if row[i].ctype == xlrd.XL_CELL_NUMBER:
                    result.update({field: int(row[i].value)})
                else:
                    result.update({field: 0})
            scraperwiki.sqlite.execute('insert into housing_market values (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                        (area,
                                         result['year'],
                                         result['bungalow'],
                                         result['detached'],
                                         result['semi'],
                                         result['terraced'],
                                         result['flatmaisonetteconverted'],
                                         result['flatmaisonetteoriginal'],
                                         result['alldwellings']))
            scraperwiki.sqlite.commit()
    

import scraperwiki

import xlrd


try:
    scraperwiki.sqlite.execute("drop table housing_market")
except:
    pass

string_fields = ("area",)

int_fields = ("year",
              "bungalow",
              "detached",
              "semi",
              "terraced",
              "flatmaisonetteconverted",
              "flatmaisonetteoriginal",
              "alldwellings")

all_fields = ["%s string" % name for name in string_fields] + ["%s int" % name for name in int_fields]

scraperwiki.sqlite.execute("create table housing_market (%s)" % ', '.join(all_fields))

xlbin = scraperwiki.scrape("http://www.communities.gov.uk/documents/housing/xls/140990.xls")
book = xlrd.open_workbook(file_contents=xlbin)
sheet = book.sheet_by_index(0)

empty_row_count = 0


for row_num in range(8, sheet.nrows):
    row = sheet.row(row_num)
    
    # one empty row delimits an area, two empty rows is end of data
    if row[0].ctype == xlrd.XL_CELL_EMPTY:
        empty_row_count += 1
        if empty_row_count > 1:
            break
    else:
        empty_row_count = 0
        
        if row[0].ctype == xlrd.XL_CELL_TEXT:
            area = row[0].value
        else:
            del(row[1]) # remove empty column
            result = {}
            for i, field in enumerate(int_fields):
                if row[i].ctype == xlrd.XL_CELL_NUMBER:
                    result.update({field: int(row[i].value)})
                else:
                    result.update({field: 0})
            scraperwiki.sqlite.execute('insert into housing_market values (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                        (area,
                                         result['year'],
                                         result['bungalow'],
                                         result['detached'],
                                         result['semi'],
                                         result['terraced'],
                                         result['flatmaisonetteconverted'],
                                         result['flatmaisonetteoriginal'],
                                         result['alldwellings']))
            scraperwiki.sqlite.commit()
    

