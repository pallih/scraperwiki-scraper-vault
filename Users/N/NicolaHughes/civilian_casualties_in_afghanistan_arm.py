import scraperwiki
import datetime
import urllib
import xlrd

surl = "http://www.sciencemag.org/content/suppl/2011/03/09/331.6022.1256.DC1/ARM-Feb2011.xls"
book = xlrd.open_workbook(file_contents=urllib.urlopen(surl).read())
placements = {'Herat':['RCW'],'Badghis':['RCW'],'Ghor':['RCW'],'Farah':['RCW'],'Faryab':['RCN'],'Jawzjan':['RCN'],'Sari Pul':['RCN'],'Balkh':['RCN'],'Samangan':['RCN'],'Kunduz':['RCN'],'Baghlan':['RCN'],'Takhar':['RCN'],'Badakshan':['RCN'],'Kabul':['RCC'],
'Paktika':['RCE'], 'Ghazni':['RCE'], 'Bamyan':['RCE'], 'Wardak':['RCE'], 'Parwan':['RCE'], 'Nuristan':['RCE'], 'Panjshir':['RCE'], 'Kunar':['RCE'], 'Kapisa':['RCE'], 'Laghman':['RCE'], 'Nangarhar':['RCE'], 'Logar':['RCE'], 'Paktya':['RCE'], 'Khost':['RCE'], 'Kandahar':['RCS'], 'Uruzgan':['RCS'], 'Zabul':['RCS'], 'Day Kundi':['RCS'], 'Nimroz':['RCSW', 'RCS'], 'Helmand':['RCSW', 'RCS']}

#for n, sheet in enumerate(book.sheets()):
    #print "Sheet %d has %d columns and %d rows" % (n, sheet.ncols, sheet.nrows)

def lexigraphical(d):
    d = str(d)
    #print d
    if d == "JAN":
        d = None
    elif d == "FEB":
        d = None
    elif d == "MAR":
        d = None
    elif d == "APR":
        d = None
    elif d == "MAY":
        d = None
    elif d == "JUN":
        d = None
    elif d == "18-19-june":
        d = "2010-06-18"
    elif d == "12-19-apr":
        d = "2010-04-12"
    elif d == "5/6-mar":
        d = "2010-03-05"
    elif d == "8/9-Mar":
        d = "2010-03-08"
    elif d == "15-16-Mar":
        d = "2010-03-15"
    elif d == "13-24-Feb":
        d = "2010-02-13"
    elif d == "27-28-Feb":
        d = "2010-02-27"
    elif d == "29-Feb":
        d = "2010-02-29"
    elif d == "None":
        d = None
    else:
        d = "2010-%s-%s" % (d[5:7], d[-2:])
    #print d
    return d

headers = []
sheet = book.sheets()[0]
for c in range(10):
    header = sheet.cell(8,c).value
    headers.append(header)
    #print headers

def cellval(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_DATE:
        datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
        if datetuple[3:] == (0, 0, 0):
            return datetime.date(datetuple[0], datetuple[1], datetuple[2])
        return datetime.date(datetuple[0], datetuple[1], datetuple[2], datetuple[3], datetuple[4], datetuple[5])
    if cell.ctype == xlrd.XL_CELL_EMPTY:    return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:  return cell.value == 1
    return cell.value


for r in range(12,316):
    time = cellval(sheet.cell(r-1,0), book.datemode)
    #print time
    coldata = []
    for c in range(10):
        coldata.append( sheet.cell(r-1,c).value )
    
    data = dict(zip(headers, coldata))
    #print data
    data['Date'] = lexigraphical(time)
    #print data['Date']
    #if (type(data['Date']) == datetime.date) or (len(data['Date'])>3):
    if data['Date'] == None:
        continue
    #if type(data['Date']) == unicode and len(data['Date']) <=3:
     #   continue
    
    scraperwiki.sqlite.save(unique_keys=['Date','Location','Killed','Wounded'], data=data)

import scraperwiki
import datetime
import urllib
import xlrd

surl = "http://www.sciencemag.org/content/suppl/2011/03/09/331.6022.1256.DC1/ARM-Feb2011.xls"
book = xlrd.open_workbook(file_contents=urllib.urlopen(surl).read())
placements = {'Herat':['RCW'],'Badghis':['RCW'],'Ghor':['RCW'],'Farah':['RCW'],'Faryab':['RCN'],'Jawzjan':['RCN'],'Sari Pul':['RCN'],'Balkh':['RCN'],'Samangan':['RCN'],'Kunduz':['RCN'],'Baghlan':['RCN'],'Takhar':['RCN'],'Badakshan':['RCN'],'Kabul':['RCC'],
'Paktika':['RCE'], 'Ghazni':['RCE'], 'Bamyan':['RCE'], 'Wardak':['RCE'], 'Parwan':['RCE'], 'Nuristan':['RCE'], 'Panjshir':['RCE'], 'Kunar':['RCE'], 'Kapisa':['RCE'], 'Laghman':['RCE'], 'Nangarhar':['RCE'], 'Logar':['RCE'], 'Paktya':['RCE'], 'Khost':['RCE'], 'Kandahar':['RCS'], 'Uruzgan':['RCS'], 'Zabul':['RCS'], 'Day Kundi':['RCS'], 'Nimroz':['RCSW', 'RCS'], 'Helmand':['RCSW', 'RCS']}

#for n, sheet in enumerate(book.sheets()):
    #print "Sheet %d has %d columns and %d rows" % (n, sheet.ncols, sheet.nrows)

def lexigraphical(d):
    d = str(d)
    #print d
    if d == "JAN":
        d = None
    elif d == "FEB":
        d = None
    elif d == "MAR":
        d = None
    elif d == "APR":
        d = None
    elif d == "MAY":
        d = None
    elif d == "JUN":
        d = None
    elif d == "18-19-june":
        d = "2010-06-18"
    elif d == "12-19-apr":
        d = "2010-04-12"
    elif d == "5/6-mar":
        d = "2010-03-05"
    elif d == "8/9-Mar":
        d = "2010-03-08"
    elif d == "15-16-Mar":
        d = "2010-03-15"
    elif d == "13-24-Feb":
        d = "2010-02-13"
    elif d == "27-28-Feb":
        d = "2010-02-27"
    elif d == "29-Feb":
        d = "2010-02-29"
    elif d == "None":
        d = None
    else:
        d = "2010-%s-%s" % (d[5:7], d[-2:])
    #print d
    return d

headers = []
sheet = book.sheets()[0]
for c in range(10):
    header = sheet.cell(8,c).value
    headers.append(header)
    #print headers

def cellval(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_DATE:
        datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
        if datetuple[3:] == (0, 0, 0):
            return datetime.date(datetuple[0], datetuple[1], datetuple[2])
        return datetime.date(datetuple[0], datetuple[1], datetuple[2], datetuple[3], datetuple[4], datetuple[5])
    if cell.ctype == xlrd.XL_CELL_EMPTY:    return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:  return cell.value == 1
    return cell.value


for r in range(12,316):
    time = cellval(sheet.cell(r-1,0), book.datemode)
    #print time
    coldata = []
    for c in range(10):
        coldata.append( sheet.cell(r-1,c).value )
    
    data = dict(zip(headers, coldata))
    #print data
    data['Date'] = lexigraphical(time)
    #print data['Date']
    #if (type(data['Date']) == datetime.date) or (len(data['Date'])>3):
    if data['Date'] == None:
        continue
    #if type(data['Date']) == unicode and len(data['Date']) <=3:
     #   continue
    
    scraperwiki.sqlite.save(unique_keys=['Date','Location','Killed','Wounded'], data=data)

