import scraperwiki
import datetime
import urllib
import xlrd

surl = "http://www.sciencemag.org/content/suppl/2011/03/09/331.6022.1256.DC1/CIVCAS-Jan2011.xls"
book = xlrd.open_workbook(file_contents=urllib.urlopen(surl).read())
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def parsemonths(d):
    d = d.strip()
    imonth = months.index(d)+1
    month = "%02d" % imonth
    return month

for n, sheet in enumerate(book.sheets()):
    print "Sheet %d has %d columns and %d rows" % (n, sheet.ncols, sheet.nrows)

rownumber = 1

         # Row, Col, Length
tables = [ (14,2,7,'2010', 'ISAF', 'Killed', 'RCS'), (14,12,7,'2009', 'ISAF', 'Killed','RCS'), (14,22,7,'2008', 'ISAF', 'Killed', 'RCS'), (30,2,7,'2010', 'ISAF', 'Wounded', 'RCS'), (30,12,7,'2009', 'ISAF', 'Wounded','RCS'), (30,22,7,'2008', 'ISAF', 'Wounded', 'RCS'), (47,2,7,'2010', 'ISAF', 'Killed', 'RCSW'), (47,12,7,'2009', 'ISAF', 'Killed','RCSW'), (47,22,7,'2008', 'ISAF', 'Killed', 'RCE'), (63,2,7,'2010', 'ISAF', 'Wounded', 'RCSW'), (63,12,7,'2009', 'ISAF', 'Wounded','RCSW'), (63,22,7,'2008', 'ISAF', 'Wounded', 'RCE'), (79,2,7,'2010', 'ISAF', 'Killed', 'RCE'), (79,12,7,'2009', 'ISAF', 'Killed','RCE'), (79,22,7,'2008', 'ISAF', 'Killed', 'RCN'), (95,2,7,'2010', 'ISAF', 'Wounded', 'RCE'), (95,12,7,'2009', 'ISAF', 'Wounded','RCE'), (95,22,7,'2008', 'ISAF', 'Wounded', 'RCN'), (111,2,7,'2010', 'ISAF', 'Killed', 'RCN'), (111,12,7,'2009', 'ISAF', 'Killed','RCN'), (111,22,7,'2008', 'ISAF', 'Killed', 'RCW'), (127,2,7,'2010', 'ISAF', 'Wounded', 'RCN'), (127,12,7,'2009', 'ISAF', 'Wounded','RCN'), (127,22,7,'2008', 'ISAF', 'Wounded', 'RCW'), (144,2,7,'2010', 'ISAF', 'Killed', 'RCW'), (144,12,7,'2009', 'ISAF', 'Killed','RCW'), (144,22,7,'2008', 'ISAF', 'Killed', 'RCC'), (160,2,7,'2010', 'ISAF', 'Wounded', 'RCW'), (160,12,7,'2009', 'ISAF', 'Wounded','RCW'), (160,22,7,'2008', 'ISAF', 'Wounded', 'RCC'), (176,2,7,'2010', 'ISAF', 'Killed', 'RCC'), (176,12,7,'2009', 'ISAF', 'Killed','RCC'), (192,2,7,'2010', 'ISAF', 'Wounded', 'RCC'), (192,12,7,'2009', 'ISAF', 'Wounded','RCC')]
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun' ,'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
headers = ['CAS', 'CCA', 'EOF ROE', 'DF', 'IDF', 'RTA', 'Unknown']

sheet = book.sheets()[0]
for (row, col, length, year, by, wk, etype) in tables:
    for i,m in enumerate(months):
        y = row + i
        datarow = []
        for x in range( col, col + length ):
            datarow.append( sheet.cell(y-1,x-1).value )
        data = dict(zip(headers,datarow))
        data['Year'] = year
        data['Type'] = etype 
        data['By'] = by
        data['Casualty_type'] = wk
        data['Month'] = m
        data['Date'] = year + "-" + parsemonths(data['Month'])
        #print data  
        scraperwiki.sqlite.save(unique_keys=['Year','Month', 'Casualty_type', 'Type'], data=data, table_name="ByISAF")    

tables2 = [(14, 34, 5, '2009', 'Insurgents', 'Killed', 'RCS'), (14, 42, 5, '2010', 'Insurgents', 'Killed', 'RCS'), (31, 34, 5, '2009', 'Insurgents', 'Wounded', 'RCS'), (31, 42, 5, '2010', 'Insurgents', 'Wounded', 'RCS'), (48, 34, 5, '2009', 'Insurgents', 'Killed', 'RCE'), (48, 42, 5, '2010', 'Insurgents', 'Killed', 'RCe'), (64, 34, 5, '2009', 'Insurgents', 'Wounded', 'RCE'), (64, 42, 5, '2010', 'Insurgents', 'Wounded', 'RCE'),(80, 34, 5,'2009', 'Insurgents', 'Killed', 'RCN'), (80, 42, 5, '2010', 'Insurgents', 'Killed', 'RCN'), (96, 34, 5, '2009', 'Insurgents', 'Wounded', 'RCN'), (96, 42, 5, '2010', 'Insurgents', 'Wounded', 'RCN'), (113, 34, 5, '2009', 'Insurgents', 'Killed', 'RCW'), (113, 42, 5, '2010', 'Insurgents', 'Killed', 'RCW'), (129, 34, 5, '2009', 'Insurgents', 'Wounded', 'RCW'), (129, 42, 5, '2010', 'Insurgents', 'Wounded', 'RCW'), (145, 34, 5, '2009', 'Insurgents', 'Killed', 'RCC'), (145, 42, 5, '2010', 'Insurgents', 'Killed', 'RCC'), (161, 34, 5, '2009', 'Insurgents', 'Wounded', 'RCC'), (161, 42, 5, '2010', 'Insurgents', 'Wounded', 'RCC'), (177, 34, 5, '2009', 'Insurgents', 'Killed', 'RCSW'), (177, 42, 5, '2010', 'Insurgents', 'Killed', 'RCSW'), (193, 34, 5,'2009', 'Insurgents', 'Wounded', 'RCSW'), (193, 42, 5, '2010', 'Insurgents', 'Wounded', 'RCSW')]
headers2 = ['DF', 'IDF', 'IED', 'ComplexAttack', 'Other']

for (row, col, length, year2, by2, wk2, etype2) in tables2:
    for i,m in enumerate(months):
        y = row + i
        datarow2 = []
        for x in range( col, col + length ):
            datarow2.append( sheet.cell(y-1,x-1).value )
        data2 = dict(zip(headers2,datarow2))
        data2['Year'] = year2
        data2['Type'] = etype2
        data2['By'] = by2
        data2['Casualty_type'] = wk2
        data2['Month'] = m
        data2['Date'] = year2 + "-" + parsemonths(data['Month'])
        #print data2  
        scraperwiki.sqlite.save(unique_keys=['Year','Month', 'Casualty_type', 'Type'], data=data2, table_name="ByInsurgents") 

sheet2 = book.sheets()[1]
for r in range(3,31):
    k = sheet2.cell(r-1,0).value.replace('(','').replace(')','')
    if k:
        value = sheet2.cell(r-1,1).value
        data3 = {'Term' : k, 'Meaning' : value }
        scraperwiki.sqlite.save(unique_keys=['Term'], data=data3, table_name='Glossary')
        