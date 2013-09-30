import scraperwiki
from BeautifulSoup import BeautifulSoup
import xlrd

XLS_FILE = "http://www2.camara.gov.br/deputados/pesquisa/arquivos/arquivo-formato-excel-com-informacoes-dos-deputados-1"
# Name, party, state, whether s/he is the elected one or his substitute (I don't know how to say it in english), address...
# building, room, address, phone, fax, birthday month and day, email, name without accent marks, title, profession..
# and, lastly, civil names. The first name is the name used in the campaign, could be a nickname



# Get the excel file and open it with xlrd
f = xlrd.open_workbook(file_contents=scraperwiki.scrape(XLS_FILE))
# The data is in the first sheet
sheet = f.sheet_by_index(0)
for r in xrange(1,sheet.nrows): # Skip the first row
    scraperwiki.datastore.save(["name", ], {
        "name": sheet.row(r)[0].value,
        "party": sheet.row(r)[1].value,
        "state": sheet.row(r)[2].value,
        "address": sheet.row(r)[4].value,
        "building": sheet.row(r)[5].value,
        "room": sheet.row(r)[6].value,
        "phone": sheet.row(r)[9].value,
        "fax": sheet.row(r)[10].value,
        "email": sheet.row(r)[13].value,
        "title": sheet.row(r)[15].value,
        "proffession": sheet.row(r)[16].value,
    })
    import scraperwiki
from BeautifulSoup import BeautifulSoup
import xlrd

XLS_FILE = "http://www2.camara.gov.br/deputados/pesquisa/arquivos/arquivo-formato-excel-com-informacoes-dos-deputados-1"
# Name, party, state, whether s/he is the elected one or his substitute (I don't know how to say it in english), address...
# building, room, address, phone, fax, birthday month and day, email, name without accent marks, title, profession..
# and, lastly, civil names. The first name is the name used in the campaign, could be a nickname



# Get the excel file and open it with xlrd
f = xlrd.open_workbook(file_contents=scraperwiki.scrape(XLS_FILE))
# The data is in the first sheet
sheet = f.sheet_by_index(0)
for r in xrange(1,sheet.nrows): # Skip the first row
    scraperwiki.datastore.save(["name", ], {
        "name": sheet.row(r)[0].value,
        "party": sheet.row(r)[1].value,
        "state": sheet.row(r)[2].value,
        "address": sheet.row(r)[4].value,
        "building": sheet.row(r)[5].value,
        "room": sheet.row(r)[6].value,
        "phone": sheet.row(r)[9].value,
        "fax": sheet.row(r)[10].value,
        "email": sheet.row(r)[13].value,
        "title": sheet.row(r)[15].value,
        "proffession": sheet.row(r)[16].value,
    })
    