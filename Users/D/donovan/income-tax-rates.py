import xlrd, re,string
from scraperwiki import datastore, scrape, metadata

sources = [
               ('http://www.hmrc.gov.uk/stats/tax_structure/incometaxrates_1974to1990.xls',1),
               ('http://www.hmrc.gov.uk/stats/tax_structure/table-a2a.xls',2)
          ]

def matchCell(cell,pattern):
    return re.match(pattern,unicode(cell.value),re.I)

def getYearRange(cell):
    match = matchCell(cell,"(\d{4}-\d{2,4})") 
    return match.group(1) if match else None
                                          
def getFirstDataRow(cell):
    match = matchCell(cell,"(Up to |1-)((\d*,)?\d*)")
    return match.group(2) if match else None

def getLastDataRow(cell):
    match = matchCell(cell,"Over(.*)")
    return match.group(1) if match else None

def stripCommas(number):
    if number:
        return str(number).replace(',','').strip()
    return None

def getIncomeRange(cell):
    first = getFirstDataRow(cell)
    last = getLastDataRow(cell)
    middle = matchCell(cell,"((\d*,)?\d*)(\s-\s|-)((\d*,)?\d*)")
    if first:
        start = 1
        end = first
    elif last:
        start = last
        end = None
    else:
        start = middle.group(1) if middle else None
        end = middle.group(4) if middle else None
    return (stripCommas(start),stripCommas(end))

def getCoordinate(row,column):
    return "%s%s" %(string.uppercase[column],row+1)

def process():
    for url,offset in sources:
        book = xlrd.open_workbook(file_contents=scrape(url))
        sheet = book.sheets()[0]
                         
        for row in range(0,sheet.nrows):
            for column in range(0,sheet.ncols):
                cell = sheet.cell(row,column)
                yearRange = getYearRange(cell)        
                if yearRange:                
                    rowCursor = row
                    while True:
                        rowCursor += 1
                        startIncome,endIncome = getIncomeRange(sheet.cell(rowCursor,column))
                        data = {
                                    'url'                : url,
                                    'incomeCoordinate'   : getCoordinate(rowCursor,column),
                                    'taxCoordinate'      : getCoordinate(rowCursor,column+offset),
                                    'yearRange'          : yearRange,
                                    'startIncome'        : startIncome,
                                    'endIncome'          : endIncome,
                                    'taxRate'            : sheet.cell(rowCursor,column+offset).value
                               }
                        if startIncome or endIncome:
                              print data
                              datastore.save(['url','incomeCoordinate','taxCoordinate'],data)
                        if startIncome and not endIncome:
                              break
                              
process()

import xlrd, re,string
from scraperwiki import datastore, scrape, metadata

sources = [
               ('http://www.hmrc.gov.uk/stats/tax_structure/incometaxrates_1974to1990.xls',1),
               ('http://www.hmrc.gov.uk/stats/tax_structure/table-a2a.xls',2)
          ]

def matchCell(cell,pattern):
    return re.match(pattern,unicode(cell.value),re.I)

def getYearRange(cell):
    match = matchCell(cell,"(\d{4}-\d{2,4})") 
    return match.group(1) if match else None
                                          
def getFirstDataRow(cell):
    match = matchCell(cell,"(Up to |1-)((\d*,)?\d*)")
    return match.group(2) if match else None

def getLastDataRow(cell):
    match = matchCell(cell,"Over(.*)")
    return match.group(1) if match else None

def stripCommas(number):
    if number:
        return str(number).replace(',','').strip()
    return None

def getIncomeRange(cell):
    first = getFirstDataRow(cell)
    last = getLastDataRow(cell)
    middle = matchCell(cell,"((\d*,)?\d*)(\s-\s|-)((\d*,)?\d*)")
    if first:
        start = 1
        end = first
    elif last:
        start = last
        end = None
    else:
        start = middle.group(1) if middle else None
        end = middle.group(4) if middle else None
    return (stripCommas(start),stripCommas(end))

def getCoordinate(row,column):
    return "%s%s" %(string.uppercase[column],row+1)

def process():
    for url,offset in sources:
        book = xlrd.open_workbook(file_contents=scrape(url))
        sheet = book.sheets()[0]
                         
        for row in range(0,sheet.nrows):
            for column in range(0,sheet.ncols):
                cell = sheet.cell(row,column)
                yearRange = getYearRange(cell)        
                if yearRange:                
                    rowCursor = row
                    while True:
                        rowCursor += 1
                        startIncome,endIncome = getIncomeRange(sheet.cell(rowCursor,column))
                        data = {
                                    'url'                : url,
                                    'incomeCoordinate'   : getCoordinate(rowCursor,column),
                                    'taxCoordinate'      : getCoordinate(rowCursor,column+offset),
                                    'yearRange'          : yearRange,
                                    'startIncome'        : startIncome,
                                    'endIncome'          : endIncome,
                                    'taxRate'            : sheet.cell(rowCursor,column+offset).value
                               }
                        if startIncome or endIncome:
                              print data
                              datastore.save(['url','incomeCoordinate','taxCoordinate'],data)
                        if startIncome and not endIncome:
                              break
                              
process()

