# not ready

import scraperwiki
import urllib
import lxml.etree 
import re
import locale
from datetime import date

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8') # use German locale; name might vary with platform >>>
encoding = locale.nl_langinfo(locale.CODESET) #encode: how data comes in, decode: how data gets out
print 'Encoding: ', encoding # tells what codeset is used, dont remove, from time to time necessary to activate code

# Hamburg
pdfurl = "http://www.hamburg.de/contentblob/1624550/data/efre-beguenstigte.pdf"

pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)

RecNo = 0 

for page in root:

    assert page.tag == 'page'

    pagelines = {}
    if RecNo <= 1:   # is there a function page number ?, so its suppose, for the first page there is min 1 record
        TableContentStart = 372 # remove the lastdigit for Line number, the last digit is unknown, the 1st page is 288, other pages 119
    else:
        TableContentStart = 122 # remove the lastdigit for Line number, the last digit is unknown, the 1st page is 288, other pages 119
    NumberOfColumns = 4 # PROBEM: DOES NOT WORK WHEN COLUMN IS PARTIALLY EMPTY Number of Columns where data has to be retrieved
    Initial = 0
    VertPosOld =0
    textOld = ''
    RecordReady = 0
    StoreNext = 0
    Receiver = ''
    Subject = ''
    Year = ''
    AmountApproved = ''
    AmountPaid = '' 
    today = date.today()

    for v in page:
        if v.tag == 'text':
            VertPos = int(v.attrib.get('top')) #why is this field named 'top' ?
#            print '== VertPosOld x VertPos x VertPosOld < VertPos  x textOld:', VertPosOld, VertPos, VertPosOld < VertPos, textOld
            if (VertPos >= TableContentStart): # first line of values in the table, below header and header line of table
#                    print '== VertPosOld x VertPos x ((VertPosOld < VertPos) and (VertPosOld >0))  x textOld:', VertPosOld, VertPos, (VertPosOld < VertPos) and (VertPosOld > 0), textOld

#Receiver
# Thats the structure of a field in a pdf which can have one or more lines.
                    if (len(re.findall('left="53"',lxml.etree.tostring(v)))) == 1:
                        if ((VertPosOld < VertPos) and (VertPosOld > 0)):
##                            text = textOld + re.match('(?s)<.*?>(.*)</.*?>', lxml.etree.tostring(v)).group(1)
                            text = textOld + lxml.etree.tostring(v, encoding=unicode, method='text')
                        else:
##                            text = re.match('(?s)<.*?>(.*)</.*?>', lxml.etree.tostring(v)).group(1)
                            text = lxml.etree.tostring(v, encoding=unicode, method='text')
#                            text = re.match('(?s)<.*?>(.*)</.*?>', lxml.etree.tostring(v)).group(1)) #, encoding=unicode)
#                        print 'Receiver: ', text  
                        Receiver = text              
                        textOld = text

# Subject
                    if (len(re.findall('left="204"',lxml.etree.tostring(v)))) == 1:
                        if ((VertPosOld < VertPos) and (VertPosOld > 0)):
#                            text = textOld + re.match('(?s)<.*?>(.*)</.*?>', lxml.etree.tostring(v)).group(1)
                            text = textOld + lxml.etree.tostring(v, encoding=unicode, method='text')
                        else:
#                            text = re.match('(?s)<.*?>(.*)</.*?>', lxml.etree.tostring(v)).group(1)
                            text = lxml.etree.tostring(v, encoding=unicode, method='text')
                            RecordReady = 1
#                        print 'Subject: ', (text) 
                        Subject = text
                        textOld = text

# Year
# Thats the structure of a field which has one line - to be tested if the same logic as for multiple lines can be applied
                    if (len(re.findall('left="497"',lxml.etree.tostring(v)))) == 1:
                        text = re.match('(?s)<.*?>(.*)</.*?>', lxml.etree.tostring(v)).group(1)
                        RecNo += 1 # use a place where I know there is always exactly one line, can be improved somewhere else
                        print 'RecNo', RecNo # also on the wrong place, best would be at then end, but I am not sure is there min one line in the last field
                        textOld = ''
#                        print 'Year : ', (text)
                        Year = text                

#AmountApproved
                    if (len(re.findall('left="556"|left="560"|left="567"|left="570"',lxml.etree.tostring(v)))) == 1:
                        text =  lxml.etree.tostring(v, encoding=unicode, method='text')
                        textOld = ''
                        AmountApproved = float(re.match('[0-9.,]*', text).group(0).replace('.','').replace(',','.'))
                        RecordReady = 2

#                     print 'in Schleife - check if there is a value in paid column: ' , len(re.findall('left="663"|left="669"|left="680"|left="683"',lxml.etree.tostring(v)))


                    if (len(re.findall('left="663"|left="669"|left="680"|left="683"',lxml.etree.tostring(v)))) == 1:
                       text =  lxml.etree.tostring(v, encoding=unicode, method='text')
                       textOld = ''
                       AmountPaid = float(re.match('[0-9.,]*', text).group(0).replace('.','').replace(',','.'))
                       print AmountPaid
                       if RecNo >= 1:
                           scraperwiki.sqlite.save(unique_keys=[ 'RecNo' ], data={ 'RecNo' : RecNo , 'Receiver' : Receiver, 'Subject' : Subject, 'Year' : Year , 'AmountApproved' : AmountApproved, 'AmountPaid' : AmountPaid , 'DateAndTime' : today.isoformat()})
                           print  'paidRecNo: ' + str(RecNo) + ' Receiver: '+ Receiver + ' Subject: ' + Subject + ' Year: ' + str(Year) + ' AmountApproved: ' + str(AmountApproved) + ' AmountPaid: ' +  str(AmountPaid) +  'DateAndTime: '+ str(today.isoformat())
                           if AmountPaid > 0 :
                               StoreNext = 1
                           AmountPaid = 0


#                       print 'RecordReady-if: ' , RecordReady

                    else: 
                       if ((RecordReady == 2) and ((len(re.findall('left="663"|left="669"|left="680"|left="683"',lxml.etree.tostring(v)))) <> 1) and StoreNext == 1 ):
                           RecNo += 1
                           print  'nonpaidRecNo: ' + str(RecNo) + ' Receiver: '+ Receiver + ' Subject: ' + Subject + ' Year: ' + str(Year) + ' AmountApproved: ' + str(AmountApproved) + ' AmountPaid: ' +  str(AmountPaid) +  'DateAndTime: '+ str(today.isoformat())
                           StoreNext = 0


                       RecordReady = 0
                    VertPosOld = VertPos
