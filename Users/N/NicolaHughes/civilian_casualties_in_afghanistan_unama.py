import scraperwiki
import datetime
import urllib
import xlrd

surl = "http://www.sciencemag.org/content/suppl/2011/03/09/331.6022.1256.DC1/UNAMA-Feb2011.xls"
book = xlrd.open_workbook(file_contents=urllib.urlopen(surl).read())
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
placements = {'Herat':['RCW'],'Badghis':['RCW'],'Ghor':['RCW'],'Farah':['RCW'],'Faryab':['RCN'],'Jawzjan':['RCN'],'Sari Pul':['RCN'],'Balkh':['RCN'],'Samangan':['RCN'],'Kunduz':['RCN'],'Baghlan':['RCN'],'Takhar':['RCN'],'Badakshan':['RCN'],'Kabul':['RCC'],
'Paktika':['RCE'], 'Ghazni':['RCE'], 'Bamyan':['RCE'], 'Wardak':['RCE'], 'Parwan':['RCE'], 'Nuristan':['RCE'], 'Panjshir':['RCE'], 'Kunar':['RCE'], 'Kapisa':['RCE'], 'Laghman':['RCE'], 'Nangarhar':['RCE'], 'Logar':['RCE'], 'Paktya':['RCE'], 'Khost':['RCE'], 'Kandahar':['RCS'], 'Uruzgan':['RCS'], 'Zabul':['RCS'], 'Day Kundi':['RCS'], 'Nimroz':['RCSW', 'RCS'], 'Helmand':['RCSW', 'RCS']}

def parsemonths(d):
    d = d.strip()
    imonth = months.index(d)+1
    month = "%02d" % imonth
    return month

for n, sheet in enumerate(book.sheets()):
    print "Sheet %d has %d columns and %d rows" % (n, sheet.ncols, sheet.nrows)

headers = ['Province', 'District', 'Number of Incidents', 'Civilians Killed', 'Civilians Injured']

tables = [(11,2,9,'January','2009','Air',1), (23,2,6,'February','2009','Air',1), (33,2,10,'March','2009','Air',1), (47,2,12,'April','2009','Air',1), (63,2,10,'May','2009','Air',1), (77,2,16,'June','2009','Air',1), (97,2,4,'July','2009','Air',1), (105,2,10,'August','2009','Air',1), 
(119,2,14,'September','2009','Air',1), (137,2,9,'October','2009','Air',1), (150,2,8,'November','2009','Air',1), (163,2,13,'December','2009','Air',1), (182,2,6,'January','2010','Air',1), (192,2,11,'February','2010','Air',1), (207,2,4,'March','2010','Air',1), (218,2,8,'May','2010','Air',1), (230,2,10,'June','2010','Air',1), (11,2,14,'January','2009','Escalation of Force',2), (29,2,9,'February','2009','Escalation of Force',2), (42,2,10,'March','2009','Escalation of Force',2), (56,2,6,'April','2009','Escalation of Force',2), (66,2,12,'May','2009','Escalation of Force',2), (82,2,8,'June','2009','Escalation of Force',2), (94,2,8,'July','2009','Escalation of Force',2), (106,2,1,'August','2009','Escalation of Force',2), (112,2,3,'September','2009','Escalation of Force',2), (120,2,2,'October','2009','Escalation of Force',2), (127,2,12,'November','2009','Escalation of Force',2), (144,2,9,'December','2009','Escalation of Force',2), (160,2,16,'January','2010','Escalation of Force',2), (181,2,7,'February','2010','Escalation of Force',2), (193,2,8,'March','2010','Escalation of Force',2), (206,2,11,'April','2010','Escalation of Force',2), (222,2,9,'May','2010','Escalation of Force',2), (236,2,2,'June','2010','Escalation of Force',2), (11,2,9,'January','2009','Search Raids',3), (25,2,11,'February','2009','Search Raids',3), (41,2,11,'March','2009','Search Raids',3), (57,2,15,'April','2009','Search Raids',3), (77,2,5,'May','2009','Search Raids',3), (87,2,3,'June','2009','Search Raids',3), (95,2,2,'July','2009','Search Raids',3), (102,2,1,'August','2009','Search Raids',3), (108,2,7,'September','2009','Search Raids',3), (120,2,9,'October','2009','Search Raids',3), (134,2,9,'November','2009','Search Raids',3), (148,2,3,'December','2009','Search Raids',3), (158,2,3,'January','2010','Search Raids',3), (166,2,3,'February','2010','Search Raids',3), (174,2,1,'March','2010','Search Raids',3), (180,2,8,'April','2010','Search Raids',3), (193,2,1,'May','2010','Search Raids',3), (199,2,7,'June','2010','Search Raids',3)]
    
last_province = ''

for (row, col, breadth, month, year, attacktype, z) in tables:
    sheet = book.sheets()[z]
    for x in range( row, row + breadth ):
        datarow = []
        for i in range(5):
            y = col + i        
            datarow.append( sheet.cell(x-1,y-1).value )
        data = dict(zip(headers,datarow))
        data['Year'] = year
        data['Month'] = month
        data['Type of Attack'] = attacktype
        data['Regional'] = 
        data['Date'] = year + "-" + parsemonths(data['Month'])
        print data  
        if data['Province'].lower().find('total') >= 0:
            continue
        if data['Province'] == u'\xa0': 
            data['Province'] = last_province
        last_province = data['Province']

             
        scraperwiki.sqlite.save(unique_keys=['Year','Month', 'Type of Attack'], data=data)  