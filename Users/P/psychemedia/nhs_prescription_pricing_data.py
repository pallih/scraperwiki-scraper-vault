import scraperwiki

import xlrd, lxml.html

import time, datetime
from time import mktime


def grabSpreadsheet(sURL):
    xlbin = scraperwiki.scrape(sURL)
    book = xlrd.open_workbook(file_contents=xlbin)
    print book.sheet_names()
    sheetname=book.sheet_names()[0]
    return (book.sheet_by_name(sheetname),sheetname)

def grabSpreadsheet2(sURL):
    xlbin = scraperwiki.scrape(sURL)
    book = xlrd.open_workbook(file_contents=xlbin)
    print book.sheet_names()
    return (book,book.sheet_names())

def dateHack(strdata):
    tmp=strdata.split(' ')
    sheetdateliteral=' '.join( [ tmp[-1].strip(' '),tmp[-2].strip(' ') ])
    print sheetdateliteral
    try:sheetdateraw= datetime.datetime.fromtimestamp(mktime(time.strptime(sheetdateliteral,"%Y %B")))
    except:sheetdateraw= datetime.datetime.fromtimestamp(mktime(time.strptime(sheetdateliteral,"%Y %b")))
    sheetdate=sheetdateraw.strftime("%Y-%m")
    sheetdatenum=(int(sheetdateraw.strftime("%Y"))-2010)*12+int(sheetdateraw.strftime("%m"))
    return (sheetdateliteral,sheetdatenum)

def scrapeSheet2(sheet,sheettable):
    title=sheet.row_values(0)[0]
    title=title.replace('  ',' ')
    strdatalist=title.split(' ')
    strdata= ' '.join([ strdatalist[0], strdatalist[1] ])
    (sheetdateliteral,sheetdatenum)=dateHack(strdata)
    print sheetdateliteral,sheetdatenum
    
    bigdata=[]
    bigcodes=[]

    try: codes=scraperwiki.sqlite.select("codes from codes2Table")
    except: codes=[]

    for nrow in range(1,sheet.nrows):
        rowdata=sheet.row_values(nrow)
        bnfcode=rowdata[0]
        bnfsection=rowdata[1]
        bnfchemical=rowdata[2]
        drugname=rowdata[3]

        data={'sheetdate':sheetdateliteral, 'sheetdatenum':sheetdatenum,'bnfcode':bnfcode }

        data['prepclass']=rowdata[4]
        data['standardquantityunit']=rowdata[5]
        data['itemsdispensed']=rowdata[6]
        data['itemsclass2']=rowdata[7]
        data['quantity']=rowdata[8]
        data['quantityclass2']=rowdata[9]
        data['nic']=rowdata[10]
        data['nicclass2']=rowdata[11]
        
        bigdata.append(data.copy())

        data={'bnfcode':bnfcode,'section':bnfsection,'chemical':bnfchemical,'drugname':drugname}
        if bnfcode not in codes:
            bigcodes.append(data.copy())
        bigcodes.append(data.copy())
        if len(bigdata)>1000:
            scraperwiki.sqlite.save(unique_keys=['bnfcode','sheetdate'],table_name='pcaTable_'+sheettable,data=bigdata,verbose=0)
            bigdata=[]
        if len(bigcodes)>1000:
            scraperwiki.sqlite.save(unique_keys=['bnfcode'],table_name='codes2Table',data=bigcodes,verbose=0)
            bigcodes=[]

    scraperwiki.sqlite.save(unique_keys=['bnfcode','sheetdate'],table_name='pcaTable_'+sheettable,data=bigdata,verbose=0)
    scraperwiki.sqlite.save(unique_keys=['bnfcode'],table_name='codes2Table',data=bigcodes,verbose=0)

def scrapeSheet(sheet,sheetname):
    row=0
    header=0
    while header==0 and row < sheet.nrows:
        cell=sheet.row_values(row)[0].strip().lower()
        if cell=='medicine':
            header=1
        elif row == sheet.nrows-1: return
        row=row+1
    
    try: codes=scraperwiki.sqlite.select("codes from codesTable")
    except: codes=[]

    bigdata=[]
    bigcodes=[]

    tmp=sheetname.split(' ')
    sheettable=' '.join( [ tmp[-1],tmp[-2] ])
    print sheettable
    sheetdateraw= datetime.datetime.fromtimestamp(mktime(time.strptime(sheettable,"%Y %B")))

    sheetdate=sheetdateraw.strftime("%Y-%m")
    sheetdatenum=(int(sheetdateraw.strftime("%Y"))-2010)*12+int(sheetdateraw.strftime("%m"))

    for nrow in range(row+1,sheet.nrows):
        rowdata=sheet.row_values(nrow)
        if rowdata[0].strip()!='':
            #really sloppy - should really grab col headers and do this properly...
            #sheetwidth=len(sheet.row_values())
            code=rowdata[3]
            data={'sheettable':sheettable, 'sheetdate':sheetdate, 'sheetdatenum':sheetdatenum,'code':code,'price':rowdata[5]}
            #scraperwiki.sqlite.save(unique_keys=['code','sheettable'],table_name='priceTable',data=data,verbose=0)
            bigdata.append(data.copy())
            data={'code':code,'category':rowdata[4],'medicine':rowdata[0],'packsize':rowdata[1],'packunit':rowdata[2]}
            if code not in codes:
                #scraperwiki.sqlite.save(unique_keys=['code'],table_name='codesTable',data=data,verbose=0)
                bigcodes.append(data.copy())
    scraperwiki.sqlite.save(unique_keys=['code','sheettable'],table_name='priceTable',data=bigdata,verbose=0)
    scraperwiki.sqlite.save(unique_keys=['code'],table_name='codesTable',data=bigcodes,verbose=0)
    scraperwiki.sqlite.save(unique_keys=['url','sheettable'],table_name='scrapesTable',data={'sheettable':sheettable,'url':sURL})

def grabexcellinks(URL,selector):
    urls=[]
    html = scraperwiki.scrape(URL)
    print html
    root = lxml.html.fromstring(html)
    links = root.cssselect(selector)
    for link in links:
        href=link.attrib.get('href')
        if href.find('xls')>-1:
            urls.append('http://www.nhsbsa.nhs.uk'+href)
    return urls

sURLs=grabexcellinks('http://www.nhsbsa.nhs.uk/PrescriptionServices/2849.aspx','P A')

scrapes=[]
try:
    scrapesdata=scraperwiki.sqlite.select("url from scrapesTable")
    for scrape in scrapesdata:
        scrapes.append(str(scrape['url']))
except: pass

print scrapes
print sURLs


#sURLs=['http://www.nhsbsa.nhs.uk/PrescriptionServices/Documents/PrescriptionServices/Part_VIIIA_December_2012.xls']

for sURL in sURLs:
    if sURL not in scrapes:
        print "grabbing",sURL
        (sheet,sheetname)=grabSpreadsheet(sURL)
        scrapeSheet(sheet,sheetname)

print "looking up Price Analysis files"
sURLs=grabexcellinks('http://www.nhsbsa.nhs.uk/PrescriptionServices/3494.aspx','TD A')

print scrapes
print sURLs


for sURL in sURLs:
    if sURL not in scrapes:
        print sURL
        (book,sheetnames)=grabSpreadsheet2(sURL)
        for sheetname in sheetnames:
            sheettable=sheetname.strip().split(' ')[0]
            sheet=book.sheet_by_name(sheetname)
            scrapeSheet2(sheet,sheettable)
        scraperwiki.sqlite.save(unique_keys=['url','sheettable'],table_name='scrapesTable',data={'sheettable':sheettable,'url':sURL})
import scraperwiki

import xlrd, lxml.html

import time, datetime
from time import mktime


def grabSpreadsheet(sURL):
    xlbin = scraperwiki.scrape(sURL)
    book = xlrd.open_workbook(file_contents=xlbin)
    print book.sheet_names()
    sheetname=book.sheet_names()[0]
    return (book.sheet_by_name(sheetname),sheetname)

def grabSpreadsheet2(sURL):
    xlbin = scraperwiki.scrape(sURL)
    book = xlrd.open_workbook(file_contents=xlbin)
    print book.sheet_names()
    return (book,book.sheet_names())

def dateHack(strdata):
    tmp=strdata.split(' ')
    sheetdateliteral=' '.join( [ tmp[-1].strip(' '),tmp[-2].strip(' ') ])
    print sheetdateliteral
    try:sheetdateraw= datetime.datetime.fromtimestamp(mktime(time.strptime(sheetdateliteral,"%Y %B")))
    except:sheetdateraw= datetime.datetime.fromtimestamp(mktime(time.strptime(sheetdateliteral,"%Y %b")))
    sheetdate=sheetdateraw.strftime("%Y-%m")
    sheetdatenum=(int(sheetdateraw.strftime("%Y"))-2010)*12+int(sheetdateraw.strftime("%m"))
    return (sheetdateliteral,sheetdatenum)

def scrapeSheet2(sheet,sheettable):
    title=sheet.row_values(0)[0]
    title=title.replace('  ',' ')
    strdatalist=title.split(' ')
    strdata= ' '.join([ strdatalist[0], strdatalist[1] ])
    (sheetdateliteral,sheetdatenum)=dateHack(strdata)
    print sheetdateliteral,sheetdatenum
    
    bigdata=[]
    bigcodes=[]

    try: codes=scraperwiki.sqlite.select("codes from codes2Table")
    except: codes=[]

    for nrow in range(1,sheet.nrows):
        rowdata=sheet.row_values(nrow)
        bnfcode=rowdata[0]
        bnfsection=rowdata[1]
        bnfchemical=rowdata[2]
        drugname=rowdata[3]

        data={'sheetdate':sheetdateliteral, 'sheetdatenum':sheetdatenum,'bnfcode':bnfcode }

        data['prepclass']=rowdata[4]
        data['standardquantityunit']=rowdata[5]
        data['itemsdispensed']=rowdata[6]
        data['itemsclass2']=rowdata[7]
        data['quantity']=rowdata[8]
        data['quantityclass2']=rowdata[9]
        data['nic']=rowdata[10]
        data['nicclass2']=rowdata[11]
        
        bigdata.append(data.copy())

        data={'bnfcode':bnfcode,'section':bnfsection,'chemical':bnfchemical,'drugname':drugname}
        if bnfcode not in codes:
            bigcodes.append(data.copy())
        bigcodes.append(data.copy())
        if len(bigdata)>1000:
            scraperwiki.sqlite.save(unique_keys=['bnfcode','sheetdate'],table_name='pcaTable_'+sheettable,data=bigdata,verbose=0)
            bigdata=[]
        if len(bigcodes)>1000:
            scraperwiki.sqlite.save(unique_keys=['bnfcode'],table_name='codes2Table',data=bigcodes,verbose=0)
            bigcodes=[]

    scraperwiki.sqlite.save(unique_keys=['bnfcode','sheetdate'],table_name='pcaTable_'+sheettable,data=bigdata,verbose=0)
    scraperwiki.sqlite.save(unique_keys=['bnfcode'],table_name='codes2Table',data=bigcodes,verbose=0)

def scrapeSheet(sheet,sheetname):
    row=0
    header=0
    while header==0 and row < sheet.nrows:
        cell=sheet.row_values(row)[0].strip().lower()
        if cell=='medicine':
            header=1
        elif row == sheet.nrows-1: return
        row=row+1
    
    try: codes=scraperwiki.sqlite.select("codes from codesTable")
    except: codes=[]

    bigdata=[]
    bigcodes=[]

    tmp=sheetname.split(' ')
    sheettable=' '.join( [ tmp[-1],tmp[-2] ])
    print sheettable
    sheetdateraw= datetime.datetime.fromtimestamp(mktime(time.strptime(sheettable,"%Y %B")))

    sheetdate=sheetdateraw.strftime("%Y-%m")
    sheetdatenum=(int(sheetdateraw.strftime("%Y"))-2010)*12+int(sheetdateraw.strftime("%m"))

    for nrow in range(row+1,sheet.nrows):
        rowdata=sheet.row_values(nrow)
        if rowdata[0].strip()!='':
            #really sloppy - should really grab col headers and do this properly...
            #sheetwidth=len(sheet.row_values())
            code=rowdata[3]
            data={'sheettable':sheettable, 'sheetdate':sheetdate, 'sheetdatenum':sheetdatenum,'code':code,'price':rowdata[5]}
            #scraperwiki.sqlite.save(unique_keys=['code','sheettable'],table_name='priceTable',data=data,verbose=0)
            bigdata.append(data.copy())
            data={'code':code,'category':rowdata[4],'medicine':rowdata[0],'packsize':rowdata[1],'packunit':rowdata[2]}
            if code not in codes:
                #scraperwiki.sqlite.save(unique_keys=['code'],table_name='codesTable',data=data,verbose=0)
                bigcodes.append(data.copy())
    scraperwiki.sqlite.save(unique_keys=['code','sheettable'],table_name='priceTable',data=bigdata,verbose=0)
    scraperwiki.sqlite.save(unique_keys=['code'],table_name='codesTable',data=bigcodes,verbose=0)
    scraperwiki.sqlite.save(unique_keys=['url','sheettable'],table_name='scrapesTable',data={'sheettable':sheettable,'url':sURL})

def grabexcellinks(URL,selector):
    urls=[]
    html = scraperwiki.scrape(URL)
    print html
    root = lxml.html.fromstring(html)
    links = root.cssselect(selector)
    for link in links:
        href=link.attrib.get('href')
        if href.find('xls')>-1:
            urls.append('http://www.nhsbsa.nhs.uk'+href)
    return urls

sURLs=grabexcellinks('http://www.nhsbsa.nhs.uk/PrescriptionServices/2849.aspx','P A')

scrapes=[]
try:
    scrapesdata=scraperwiki.sqlite.select("url from scrapesTable")
    for scrape in scrapesdata:
        scrapes.append(str(scrape['url']))
except: pass

print scrapes
print sURLs


#sURLs=['http://www.nhsbsa.nhs.uk/PrescriptionServices/Documents/PrescriptionServices/Part_VIIIA_December_2012.xls']

for sURL in sURLs:
    if sURL not in scrapes:
        print "grabbing",sURL
        (sheet,sheetname)=grabSpreadsheet(sURL)
        scrapeSheet(sheet,sheetname)

print "looking up Price Analysis files"
sURLs=grabexcellinks('http://www.nhsbsa.nhs.uk/PrescriptionServices/3494.aspx','TD A')

print scrapes
print sURLs


for sURL in sURLs:
    if sURL not in scrapes:
        print sURL
        (book,sheetnames)=grabSpreadsheet2(sURL)
        for sheetname in sheetnames:
            sheettable=sheetname.strip().split(' ')[0]
            sheet=book.sheet_by_name(sheetname)
            scrapeSheet2(sheet,sheettable)
        scraperwiki.sqlite.save(unique_keys=['url','sheettable'],table_name='scrapesTable',data={'sheettable':sheettable,'url':sURL})
