# V2
# actually an idea to be tested
# Suppose the structure of the PDF can be very chaotic, first we read all the date we need, as second step we combine the data 
# the PDF Page Structure we get from 

# also possible
#scraperwiki.sqlite.execute("delete from ttt where xx=9")           
#scraperwiki.sqlite.execute("drop table if exists ttt")

import scraperwiki
import urllib
import lxml.etree 
import re
import locale
from datetime import date



locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8') # use German locale; name might vary with platform >>>
encoding = locale.nl_langinfo(locale.CODESET) #encode: how data comes in, decode: how data gets out
print 'Encoding: ', encoding # tells what codeset is used, dont remove, from time to time necessary to activate code

# Spain Islas Canarias
pdfurl = "http://www.dgfc.sgpg.meh.es/sitios/DGFC/es-ES/Beneficiarios%20Fondos%20Feder%20y%20Fondos%20de%20Cohesin/IC34.pdf"

# pdfurl = "http://infolution.net/diplomarbeit/20110822_EFRE_Spain_IslasCanarias_IC34_P01_to16.pdf"

pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)

StartlinePageInitial = 163
StartlinePageFollowing = 163

RecNo = 0 

for page in root:

    assert page.tag == 'page'

    pagelines = {}
    if RecNo <= 1:   
        TableContentStart = StartlinePageInitial # Variable who has the startline for the 1st page
    else:
        TableContentStart = StartlinePageFollowing # Variable who has the startine for the 2nd until the last page 
    today = date.today()

    for v in page:
        if v.tag == 'text':
#            if (VertPos >= TableContentStart): # first line of values in the table, below header and header line of table

#Receiver # Thats the structure of a field in a pdf which can have one or more lines.

#                    print 'Pagenumber: ' , page.attrib.get('number')
                    print 'PageNo & x-left/y-down  &  lxh : ', page.attrib.get('number') , str(int(v.attrib.get('left'))) + '/' + str(int(v.attrib.get('top'))) + ' - ' + str(int(v.attrib.get('width'))) + ' x ' + str(int(v.attrib.get('height')))

#StringfieldOneLine
#Pos16, LATER 18 - Receiver, Pos 319 LATER 323 Subject, Pos 640-662 Amount, Pos718-746 AmountPaid, Pos 811 Year. Pos 811 (starting from Page 135 it changed to 812 (Year also defines Lines/Blocks
#                    if (len(re.findall('left="16"|left="18"|left="319"|left="323"|left="635"|left="640"|left="645"|left="652"|left="657"|left="662"|left="718"|left="723"|left="728"|left="736"|left="741"|left="746"|left="811"|left="812"',lxml.etree.tostring(v)))) == 1:



                    if (len(re.findall('left="16"|left="18"|left="319"|left="323"|left="635"|left="640"|left="645"|left="652"|left="657"|left="662"|left ="670"|left="675"|left="718"|left="723"|left="728"|left="736"|left="741"|left="746"|left="753"|left="758"|left="811"|left="812"', lxml.etree.tostring(v)))) == 1:
                        if (((len(re.findall('left="811"',lxml.etree.tostring(v)))) == 1) or ((len(re.findall('left="812"',lxml.etree.tostring(v)))) == 1)): # The Year defines each individual record, means when there is a year entry the record number changes
                            RecNo += 1
                        Sequencenumber = int(( float(page.attrib.get('number'))*100000)  + float(v.attrib.get('top')))
                        PrId = int(( float(page.attrib.get('number'))*10000)  + float(RecNo))
                        print Sequencenumber # int(page.attrib.get('number') * 100000)  , int(v.attrib.get('top'))
                        scraperwiki.sqlite.save(table_name="PDF_DATA_UNSTRUCTURED", unique_keys=[ 'Page', 'x_leftPos', 'y_downPos' ], data={ 'Sequencenumber' : Sequencenumber ,'PrId' : PrId , 'RecNo' : RecNo , 'Page' : int(page.attrib.get('number')) , 'x_leftPos' : int(v.attrib.get('left')), 'y_downPos' : int(v.attrib.get('top')), 'BlockLength' : int(v.attrib.get('width')) , 'BlockHeigth' : int(v.attrib.get('height')), 'UniCodeString' : lxml.etree.tostring(v, encoding=unicode, method='text') , 'InsertTimestamp' : today.isoformat()})


# First SQL Transformation:
#select  
#PrId
#, sequencenumber 
#, case  when (ByDn is null) then ((sequencenumber / 1000) *1000 ) + 999 
#else ByDn 
#end ByDn 
#from 
#(
#  select 
#  distinct 
#    a.PrId 
#    , (a.sequencenumber -1) as sequencenumber 
#    , ((select b.sequencenumber from PDF_DATA_UNSTRUCTURED b where a.recno = b.recno-1 and b.page = a.page and a.recno >= 1)-1)  as ByDn 
#  from PDF_DATA_UNSTRUCTURED a 
#  where a.RecNo > 0 and ((ByDn > a.sequencenumber) or (ByDn is null))
#)


# changed
# select PrId, sequencenumber , case  when (ByDn is null) then ((sequencenumber / 1000) *1000 ) + 999 else ByDn end ByDn from (select distinct a.PrId , (a.sequencenumber -1) as sequencenumber , ((select b.sequencenumber from PDF_DATA_UNSTRUCTURED b where a.recno = b.recno-1 and b.page = a.page and a.recno >= 1)-1)  as ByDn from PDF_DATA_UNSTRUCTURED a where a.RecNo > 0 and ((ByDn > a.sequencenumber) or (ByDn is null)))

#scraperwiki.sqlite.attach('pdf_reader_template');

#results = scraperwiki.sqlite.select('a.PrId , (a.sequencenumber -1) as sequencenumber , ((select b.sequencenumber from PDF_DATA_UNSTRUCTURED b where a.recno = b.recno-1 and b.page = a.page and a.recno >= 1)-1)  as ByDn from PDF_DATA_UNSTRUCTURED a where a.RecNo > 0 and ((ByDn > a.sequencenumber) or (ByDn is null))' )

results = scraperwiki.sqlite.select(' PrId, sequencenumber , case  when (ByDn is null) then ((sequencenumber / 1000) *1000 ) + 999 else ByDn end ByDn from (select distinct a.PrId , (a.sequencenumber -1) as sequencenumber , ((select b.sequencenumber from PDF_DATA_UNSTRUCTURED b where a.recno = b.recno-1 and b.page = a.page and a.recno >= 1)-1)  as ByDn from PDF_DATA_UNSTRUCTURED a where a.RecNo > 0 and ((ByDn > a.sequencenumber) or (ByDn is null)))')

scraperwiki.sqlite.save([], results, table_name="TransformTestTable")




# Second SQL Transformation:
#select 
#a.PrId 
#, a.sequencenumber as seqmin
#, a.bydn as seqmax
#, (select group_concat(UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and  ((i.x_leftPos = 16) or (i.x_leftPos = 18)) group by i.x_leftPos) as Receiver 
#, (select group_concat(UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and ((i.x_leftPos = 319) or (i.x_leftPos = 323)) group by i.x_leftPos) as Subject 
#, (select group_concat(UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and ((i.x_leftPos = 811) or ((i.x_leftPos =  812))) group by i.x_leftPos) as Year 
#, (select (UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and (i.x_leftPos >= 635 and i.x_leftPos <= 670) group by i.x_leftPos) as Amount 
#, (select  (UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and (i.x_leftPos >= 718 and i.x_leftPos <= 753) group by i.x_leftPos) as AmountPaid 
#, (select group_concat(sequencenumber)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and ((i.x_leftPos = 811) or ((i.x_leftPos =  812))) group by i.x_leftPos) as SeqRespCol 
#from TransformTestTable a 
#where SeqRespCol not in
#(
#select sequencenumber
#from
#(
# select sequencenumber from  pdf_data_unstructured where ((x_leftPos >= 635) and (x_leftPos <= 675)) 
# except 
#  select sequencenumber from  pdf_data_unstructured where ((x_leftPos = 811) or (x_leftPos = 812))
#   except -- because bad line accuracy the following line 
#  select sequencenumber-1 from  pdf_data_unstructured where ((x_leftPos = 811) or (x_leftPos = 812))
#   except -- because bad line accuracy the following line 
#    select sequencenumber+1 from  pdf_data_unstructured where ((x_leftPos = 811) or (x_leftPos = 812))
# ) 
#)




# scraperwiki.sqlite.attach('pdf_reader_template'); # Its already attached !

results = scraperwiki.sqlite.select('a.PrId , a.sequencenumber as seqmin , a.bydn as seqmax, (select group_concat(UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and  ((i.x_leftPos = 16) or (i.x_leftPos = 18)) group by i.x_leftPos) as Receiver , (select group_concat(UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and ((i.x_leftPos = 319) or (i.x_leftPos = 323)) group by i.x_leftPos) as Subject , (select group_concat(UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and ((i.x_leftPos = 811) or ((i.x_leftPos =  812))) group by i.x_leftPos) as Year , (select (UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and (i.x_leftPos >= 635 and i.x_leftPos <= 675) group by i.x_leftPos) as Amount , (select  (UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and (i.x_leftPos >= 718 and i.x_leftPos <= 758) group by i.x_leftPos) as AmountPaid, (select  (Inserttimestamp)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and (i.x_leftPos >= 811 and i.x_leftPos <= 812) group by i.x_leftPos) as DateAndTime, (select group_concat(sequencenumber)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and ((i.x_leftPos = 811) or ((i.x_leftPos =  812))) group by i.x_leftPos) as SeqRespCol from TransformTestTable a where SeqRespCol not in ( select sequencenumber from ( select sequencenumber from  pdf_data_unstructured where ((x_leftPos >= 635) and (x_leftPos <= 675)) except select sequencenumber from  pdf_data_unstructured where ((x_leftPos = 811) or (x_leftPos = 812)) except select sequencenumber-1 from  pdf_data_unstructured where ((x_leftPos = 811) or (x_leftPos = 812))except select sequencenumber+1 from  pdf_data_unstructured where ((x_leftPos = 811) or (x_leftPos = 812))))') 


print results
scraperwiki.sqlite.save([], results, table_name="Synthesis")


#select 
#a.seqmin
#,a.seqmax
#,a.Amount
#,a.Year
#,a.SeqRespCol
#,a.AmountPaid
#,a.Subject
#,a.prid 
#,case 
#  when a.receiver is null 
#    then (select b.receiver from synthesis b where b.receiver is not null and b.prid < a.prid order by b.prid desc limit 1) 
#    else a.receiver
#  end as Receiver
#from synthesis a


# Synthesis [41727 rows] CREATE TABLE `Synthesis` (`seqmin` integer, `Receiver` text, `seqmax` integer, `PrId` integer, `Amount` text, `Year` text, `SeqRespCol` text, `AmountPaid` text, `Subject` text)


# scraperwiki.sqlite.attach('pdf_reader_template'); # Its already attached !

# results = scraperwiki.sqlite.select('a.prid ,a.SeqRespCol ,a.seqmin ,a.seqmax ,case when a.receiver is null then (select b.receiver from synthesis b where b.receiver is not null and b.prid < a.prid order by b.prid desc limit 1)  else a.receiver end ,a.Subject ,a.Amount ,a.AmountPaid ,a.Year from synthesis a limit 200')

results = scraperwiki.sqlite.select('"Spain" as Country, "Islas-Canarias" as State, a.prid ,a.SeqRespCol ,a.seqmin ,a.seqmax  ,case when a.receiver is null then (select b.receiver from synthesis b where b.receiver is not null and b.prid < a.prid order by b.prid desc limit 1) else a.receiver end as Receiver ,a.Subject ,a.Amount ,a.AmountPaid, a.Year, DateAndTime from synthesis a ')


#results = scraperwiki.sqlite.select('a.prid ,a.SeqRespCol ,a.seqmin ,a.seqmax ,a.Subject ,a.Amount ,a.AmountPaid ,a.Year from synthesis a') 

# scraperwiki.sqlite.save(unique_keys, data, table_name="swdata", verbose=2)
print results
scraperwiki.sqlite.save([], results, table_name="EFRE_EU_SPAIN_ISLAS_CANARIAS" , verbose=2)

# Line 5 - scraperwiki.datastore.save(unique_keys=['table_cell'], data) -- non-keyword arg after keyword arg SyntaxError('non-keyword arg after keyword arg', ('<string>', 5, None, None))
