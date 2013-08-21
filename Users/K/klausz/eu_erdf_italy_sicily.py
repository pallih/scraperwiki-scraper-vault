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

# Italy - Sicily
pdfurl = "http://www.euroinfosicilia.it/Portals/0/elenco_beneficiari/elenco_dei_beneficiari_finali_al_31_maggio_2011.pdf"

print '123' + pdfurl

pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)

StartlinePageInitial = 36
StartlinePageFollowing = 27
#Receiver
ScrPosF01 = 'left="84"|left="88"|left="94"|'
#NotNeeded
ScrPosF02 = 'left="200"|'
#Subject
ScrPosF03 = 'left="279"|'
#ProjectExpensesTotal
ScrPosF04 = 'left="381"|left="384"|left="388"|left="394"|left="398"|left="401"|left="407"|'
#ProjectExpensesPartA
ScrPosF05 = 'left="527"|left="531"|left="535"|left="540"|left="544"|left="548"|left="553"|'
#ProjectExpensesPartB
ScrPosF06 = 'left="639"|left="643"|left="648"|left="652"|left="656"|left="661"|'
#ERDFAmountApproved
ScrPosF07 = 'left="721"|left="725"|left="730"|left="734"|left="738"|left="744"' #Not for the last one

RelevantRecordColumn = 'left="279"'


ReceiverMinPos=84
ReceiverMaxPos=94
SubjectMinPos=279
SubjectMaxPos=279
#YearMinPos=
#YearMaxPos=
AmountApprovedMinPos=725
AmountApprovedMaxPos=744
#AmountPaidMinPos=
#AmountPaidMaxPos=
RelRecColPos=279
# ScrPosF08 = 

#ScraperPositions = 'left="51"|left="200"|left="279"|left="381"|left="384"|left="388"|left="527"|left="531"|left="535"|left="639"|left ="643"|left="652"|left="725"|left="730"|left="734"'
ScraperPositions = ScrPosF01 + ScrPosF02 + ScrPosF03 + ScrPosF04 + ScrPosF05 + ScrPosF06 + ScrPosF07




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

                    print 'PageNo & x-left/y-down  &  lxh : ', page.attrib.get('number') , str(int(v.attrib.get('left'))) + '/' + str(int(v.attrib.get('top'))) + ' - ' + str(int(v.attrib.get('width'))) + ' x ' + str(int(v.attrib.get('height')))


                    if (len(re.findall(ScraperPositions, lxml.etree.tostring(v)))) == 1:

                        if (((len(re.findall(RelevantRecordColumn,lxml.etree.tostring(v)))) == 1)): 

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

# results = scraperwiki.sqlite.select('a.PrId , a.sequencenumber as seqmin , a.bydn as seqmax, (select group_concat(UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and  ((i.x_leftPos = 16) or (i.x_leftPos = 18)) group by i.x_leftPos) as Receiver , (select group_concat(UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and ((i.x_leftPos >= 319) or (i.x_leftPos = 323)) group by i.x_leftPos) as Subject , (select group_concat(UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and ((i.x_leftPos = 811) or ((i.x_leftPos =  812))) group by i.x_leftPos) as Year , (select (UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and (i.x_leftPos >= 635 and i.x_leftPos <= 675) group by i.x_leftPos) as Amount , (select  (UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and (i.x_leftPos >= 718 and i.x_leftPos <= 758) group by i.x_leftPos) as AmountPaid, (select  (Inserttimestamp)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and (i.x_leftPos >= 279 and i.x_leftPos <= 279) group by i.x_leftPos) as DateAndTime, (select group_concat(sequencenumber)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and ((i.x_leftPos = 279)) group by i.x_leftPos) as SeqRespCol from TransformTestTable a where SeqRespCol not in ( select sequencenumber from ( select sequencenumber from  pdf_data_unstructured where ((x_leftPos >= 635) and (x_leftPos <= 675)) except select sequencenumber from  pdf_data_unstructured where ((x_leftPos = 279)) except select sequencenumber-1 from  pdf_data_unstructured where ((x_leftPos = 279)) except select sequencenumber+1 from  pdf_data_unstructured where ((x_leftPos = 279))))')



# SqlCommand2 = 'select a.PrId , a.sequencenumber as seqmin, a.bydn as seqmax , (select group_concat(UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and  ((i.x_leftPos >= ' + str(ReceiverMinPos) + ') or (i.x_leftPos <= ' + str(ReceiverMaxPos) + ')) group by i.x_leftPos) as Receiver, (select group_concat(UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and ((i.x_leftPos >= '+ str(SubjectMinPos) + ') or (i.x_leftPos <= ' + str(SubjectMinPos) + ')) group by i.x_leftPos) as Subject from TransformTestTable a'

# (select  (UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and (i.x_leftPos >= ' + str(AmountApprovedMinPos) + ' and i.x_leftPos <= ' + str(AmountApprovedMaxPos + ') group by i.x_leftPos) as AmountPaid 


SqlCommand2 = 'select a.PrId , a.sequencenumber as seqmin, a.bydn as seqmax , (select group_concat(UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and  ((i.x_leftPos >= ' + str(ReceiverMinPos) + ') or (i.x_leftPos <= ' + str(ReceiverMaxPos) + ')) group by i.x_leftPos) as Receiver, (select group_concat(UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and ((i.x_leftPos >= '+ str(SubjectMinPos) + ') or (i.x_leftPos <= ' + str(SubjectMinPos) + ')) group by i.x_leftPos) as Subject, (select  (Inserttimestamp)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and (i.x_leftPos >= ' + str(RelRecColPos) + ' and i.x_leftPos <= ' + str(RelRecColPos) + ') group by i.x_leftPos) as DateAndTime, (select group_concat(sequencenumber) from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and ((i.x_leftPos = ' + str(RelRecColPos) + ')) group by i.x_leftPos) as SeqRespCol, (select  (UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and (i.x_leftPos >= ' + str(AmountApprovedMinPos) + ' and i.x_leftPos <= ' + str(AmountApprovedMaxPos) + ') group by i.x_leftPos) as AmountPaid from TransformTestTable a'





# SqlCommand2 = 'select a.PrId , a.sequencenumber as seqmin , a.bydn as seqmax, (select group_concat(UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and  ((i.x_leftPos >= ' + str(ReceiverMinPos) + ') or (i.x_leftPos <= ' + str(ReceiverMaxPos) + ')) group by i.x_leftPos) as Receiver , (select group_concat(UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and ((i.x_leftPos >= '+ str(SubjectMinPos) + ') or (i.x_leftPos <= ' + str(SubjectMinPos) + ')) group by i.x_leftPos) as Subject, (select  (UniCodeString)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and (i.x_leftPos >= ' + str(AmountApprovedMinPos) + ' and i.x_leftPos <= ' + str(AmountApprovedMaxPos + ') group by i.x_leftPos) as AmountPaid, (select  (Inserttimestamp)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and (i.x_leftPos >= ' + str(RelRecColPos) + ' and i.x_leftPos <= ' + str(RelRecColPos) + ') group by i.x_leftPos) as DateAndTime, (select group_concat(sequencenumber)  from PDF_DATA_UNSTRUCTURED i where (i.Sequencenumber >= a.sequencenumber) and (i.Sequencenumber < a.bydn) and ((i.x_leftPos = ' + str(RelRecColPos) + ')) group by i.x_leftPos) as SeqRespCol from TransformTestTable a'

print  SqlCommand2


results = scraperwiki.sqlite.execute(SqlCommand2) 


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

results = scraperwiki.sqlite.select('"Italy" as Country, "Sicily" as State, a.PrId ,a.SeqRespCol ,a.seqmin ,a.seqmax  ,case when a.receiver is null then (select b.receiver from synthesis b where b.receiver is not null and b.prid < a.prid order by b.prid desc limit 1) else a.receiver end as Receiver ,a.Subject ,a.Amount ,a.AmountPaid, a.Year, DateAndTime from synthesis a ')


#results = scraperwiki.sqlite.select('a.prid ,a.SeqRespCol ,a.seqmin ,a.seqmax ,a.Subject ,a.Amount ,a.AmountPaid ,a.Year from synthesis a')

# scraperwiki.sqlite.save(unique_keys, data, table_name="swdata", verbose=2)
print results
scraperwiki.sqlite.save([], results, table_name="EFRE_EU_Italy_Sicily" , verbose=2)

# Line 5 - scraperwiki.datastore.save(unique_keys=['table_cell'], data) -- non-keyword arg after keyword arg SyntaxError('non-keyword arg after keyword arg', ('<string>', 5, None, None))
