import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

# Hello World Example #

#scrape page
html = scraperwiki.scrape('http://scraperwiki.com/hello_world.html')
page = BeautifulSoup.BeautifulSoup(html)

#find rows
for table in page.findAll('table'):
    for row in table.findAll('tr')[1:]: 

        #save to datastore
        data = {'message' : row.td.string,}
        datastore.save(unique_keys=['message'], data=data)


import xlrd

def and_(x, y):
    return x and y

class tables(object):
    def __init__(self, workbook_name, sheet_name, row_number):
        book = xlrd.open_workbook(workbook_name)
        self.sheet = None
        self.sheet_name = sheet_name
        for sheet in book.sheets():
            if sheet.name.strip() == sheet_name.strip():
               self.sheet = sheet
        self.headers = [header.value.strip() for header in self.sheet.row(row_number)]
        self.row_number = row_number + 1
        self.current_type = None
    def __iter__(self):
        while self.row_number < self.sheet.nrows:
            if reduce(and_, [c.value == "" for c in self.sheet.row(self.row_number)]):
                self.row_number = self.row_number + 1
                self.current_type = self.sheet.cell(self.row_number, 0)
                self.row_number = self.row_number + 1
            if self.row_number + 1 == self.sheet.nrows or self.sheet.cell(self.row_number + 1, 1).value != "":
                row = [str(c.value) for c in self.sheet.row(self.row_number)]
            else:
                row = [str(c.value) + str(c2.value) for c, c2 in zip(self.sheet.row(self.row_number), self.sheet.row(self.row_number + 1))]
            d = dict(zip(self.headers, row))
            d.update({"denomination": self.current_type, "type": self.sheet_name})
            yield d
            self.row_number = self.row_number + 1 

for type_ in ["
list(tables("tcm21-172601.xls", "PRIMARY", 1))import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

# Hello World Example #

#scrape page
html = scraperwiki.scrape('http://scraperwiki.com/hello_world.html')
page = BeautifulSoup.BeautifulSoup(html)

#find rows
for table in page.findAll('table'):
    for row in table.findAll('tr')[1:]: 

        #save to datastore
        data = {'message' : row.td.string,}
        datastore.save(unique_keys=['message'], data=data)


import xlrd

def and_(x, y):
    return x and y

class tables(object):
    def __init__(self, workbook_name, sheet_name, row_number):
        book = xlrd.open_workbook(workbook_name)
        self.sheet = None
        self.sheet_name = sheet_name
        for sheet in book.sheets():
            if sheet.name.strip() == sheet_name.strip():
               self.sheet = sheet
        self.headers = [header.value.strip() for header in self.sheet.row(row_number)]
        self.row_number = row_number + 1
        self.current_type = None
    def __iter__(self):
        while self.row_number < self.sheet.nrows:
            if reduce(and_, [c.value == "" for c in self.sheet.row(self.row_number)]):
                self.row_number = self.row_number + 1
                self.current_type = self.sheet.cell(self.row_number, 0)
                self.row_number = self.row_number + 1
            if self.row_number + 1 == self.sheet.nrows or self.sheet.cell(self.row_number + 1, 1).value != "":
                row = [str(c.value) for c in self.sheet.row(self.row_number)]
            else:
                row = [str(c.value) + str(c2.value) for c, c2 in zip(self.sheet.row(self.row_number), self.sheet.row(self.row_number + 1))]
            d = dict(zip(self.headers, row))
            d.update({"denomination": self.current_type, "type": self.sheet_name})
            yield d
            self.row_number = self.row_number + 1 

for type_ in ["
list(tables("tcm21-172601.xls", "PRIMARY", 1))