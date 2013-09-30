import scraperwiki
import urllib
import xlrd
import StringIO

try:
    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS Meta_Activism_Dataset")
    scraperwiki.sqlite.execute("CREATE TABLE Meta_Activism_Dataset ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 'sheet_id' STRING, 'title' STRING, 'country' STRING, 'year' STRING, 'source1' STRING, 'source2' STRING, 'source3' STRING, 'source4' STRING, 'source5' STRING, 'source6' STRING, 'source7' STRING, 'entered_by' STRING, 'notes' STRING)")
except:
    pass

url = 'http://www.meta-activism.org/wp-content/uploads/2010/08/GDADS-Final-Case-Study-List-_In-Use_020611.xls'
response = urllib.urlopen(url)
stream = response.read()
file = StringIO.StringIO(stream)

wb = xlrd.open_workbook(file_contents=file.read())

for s in wb.sheets():
    
    
    for row in range(1, s.nrows-1):
        
        values = []
        
        for col in range(s.ncols):
            values.append(unicode(s.cell(row,col).value))

        #print values
        scraperwiki.sqlite.execute("INSERT INTO Meta_Activism_Dataset ('sheet_id', 'title', 'country', 'year', 'source1', 'source2', 'source3', 'source4', 'source5', 'source6', 'source7', 'entered_by', 'notes') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", values)  

scraperwiki.sqlite.commit()
import scraperwiki
import urllib
import xlrd
import StringIO

try:
    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS Meta_Activism_Dataset")
    scraperwiki.sqlite.execute("CREATE TABLE Meta_Activism_Dataset ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 'sheet_id' STRING, 'title' STRING, 'country' STRING, 'year' STRING, 'source1' STRING, 'source2' STRING, 'source3' STRING, 'source4' STRING, 'source5' STRING, 'source6' STRING, 'source7' STRING, 'entered_by' STRING, 'notes' STRING)")
except:
    pass

url = 'http://www.meta-activism.org/wp-content/uploads/2010/08/GDADS-Final-Case-Study-List-_In-Use_020611.xls'
response = urllib.urlopen(url)
stream = response.read()
file = StringIO.StringIO(stream)

wb = xlrd.open_workbook(file_contents=file.read())

for s in wb.sheets():
    
    
    for row in range(1, s.nrows-1):
        
        values = []
        
        for col in range(s.ncols):
            values.append(unicode(s.cell(row,col).value))

        #print values
        scraperwiki.sqlite.execute("INSERT INTO Meta_Activism_Dataset ('sheet_id', 'title', 'country', 'year', 'source1', 'source2', 'source3', 'source4', 'source5', 'source6', 'source7', 'entered_by', 'notes') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", values)  

scraperwiki.sqlite.commit()
