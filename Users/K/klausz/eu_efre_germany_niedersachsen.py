# open tbd
import scraperwiki
import urllib
import lxml.etree 
import re
import locale
from datetime import date

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8') # use German locale; name might vary with platform >>>
encoding = locale.nl_langinfo(locale.CODESET) #encode: how data comes in, decode: how data gets out
print 'Encoding: ', encoding # tells what codeset is used, dont remove, from time to time necessary to activate code



# Niedersachsen - have a look, there are several Programs - http://www.mw.niedersachsen.de/live/live.php?navigation_id=5679&article_id=15575&_psmand=18
pdfurl = "http://www.mw.niedersachsen.de/download/59986"

pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)

RecNo = 0 

for page in root:

    assert page.tag == 'page'

    pagelines = {}
    if RecNo <= 1:   # is there a function page number ?, so its suppose, for the first page there is min 1 record
        TableContentStart = 145 # remove the lastdigit for Line number, the last digit is unknown, the 1st page is 288, other pages 119
    else:
        TableContentStart = 47 # remove the lastdigit for Line number, the last digit is unknown, the 1st page is 288, other pages 119
    NumberOfColumns = 4 # PROBEM: DOES NOT WORK WHEN COLUMN IS PARTIALLY EMPTY Number of Columns where data has to be retrieved
    Initial = 0
    VertPosOld =0
    textOld = ''
    RecordReady = 0

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

#Receiver # Thats the structure of a field in a pdf which can have one or more lines.
                    if (len(re.findall('left="59"',lxml.etree.tostring(v)))) == 1:
                        if ((VertPosOld < VertPos) and (VertPosOld > 0)):
                            text = textOld + lxml.etree.tostring(v, encoding=unicode, method='text')
                        else:
                            text = lxml.etree.tostring(v, encoding=unicode, method='text')
                        Receiver = text              
                        textOld = text

# Subject
                    if (len(re.findall('left="281"',lxml.etree.tostring(v)))) == 1:
                        if ((VertPosOld < VertPos) and (VertPosOld > 0)):
                            text = textOld + lxml.etree.tostring(v, encoding=unicode, method='text')
                        else:
                            text = lxml.etree.tostring(v, encoding=unicode, method='text')
                            RecordReady = 1
                        Subject = text
                        textOld = text

# Year # Thats the structure of a field which has one line - to be tested if the same logic as for multiple lines can be applied
                    if (len(re.findall('left="486"',lxml.etree.tostring(v)))) == 1:
                        text = re.match('(?s)<.*?>(.*)</.*?>', lxml.etree.tostring(v)).group(1)
                        RecNo += 1 # use a place where I know there is always exactly one line, can be improved somewhere else
#                        print 'RecNo', RecNo # also on the wrong place, best would be at then end, but I am not sure is there min one line in the last field
                        textOld = ''
                        Year = text                


# Year # The year of the payment
                    if (len(re.findall('left="557"',lxml.etree.tostring(v)))) == 1:
                        text = re.match('(?s)<.*?>(.*)</.*?>', lxml.etree.tostring(v)).group(1)
                        textOld = ''
                        YearPayment = text                

#AmountApproved
#                    if (len(re.findall('left="621"|left="626"|left="632"|left="637"|left="641"',lxml.etree.tostring(v)))) == 1:
                    if (((len(re.findall('left="621"|left="626"|left="632"|left="637"|left="641"',lxml.etree.tostring(v)))) == 1) and ((len(re.findall('left="696"|left="700"|left="707"|left="711"|left="715"',lxml.etree.tostring(v)))) <> 1)):
                        text = re.match('(?s)<.*?>(.*)</.*?>', lxml.etree.tostring(v)).group(1)
                        textOld = ''
                        AmountApproved = float(text[0:(text).find(' ')].replace('.','').replace(',','.')) 
                        if RecNo >= 1:
                            scraperwiki.sqlite.save(unique_keys=[ 'RecNo' ], data={ 'RecNo' : RecNo , 'Receiver' : Receiver, 'Subject' : Subject, 'Year' :
Year , 'AmountApproved' : AmountApproved, 'AmountPaid' : 0, 'DateAndTime' : today.isoformat()})
                            print  'xRecNo: ' + str(RecNo) + ' Receiver: '+ Receiver + ' Subject: ' + Subject + ' Year: ' + str(Year) + ' AmountApproved: ' + str(AmountApproved) + ' AmountPaid: 0'+  'DateAndTime: '+ str(today.isoformat())

#AmountPaid
#                    if (len(re.findall('left="696"|left="700"|left="707"|left="711"|left="715"',lxml.etree.tostring(v)))) == 1: 
                    if (((len(re.findall('left="621"|left="626"|left="632"|left="637"|left="641"',lxml.etree.tostring(v)))) == 1) and ((len(re.findall('left="696"|left="700"|left="707"|left="711"|left="715"',lxml.etree.tostring(v)))) == 1)):
                        text = re.match('(?s)<.*?>(.*)</.*?>', lxml.etree.tostring(v)).group(1)
                        textOld = ''
                        AmountPaid = float(text[0:(text).find(' ')].replace('.','').replace(',','.')) 
#                        print 'AmountPaid: ', AmountPaid

                        if RecNo >= 1:
                            scraperwiki.sqlite.save(unique_keys=[ 'RecNo' ], data={ 'RecNo' : RecNo , 'Receiver' : Receiver, 'Subject' : Subject, 'Year' : Year , 'AmountApproved' : 0, 'AmountPaid' : AmountPaid , 'DateAndTime' : today.isoformat()})
                            print  'yRecNo: ' + str(RecNo) + ' Receiver: '+ Receiver + ' Subject: ' + Subject + ' Year: ' + str(Year) + ' AmountApproved: ' + str(AmountApproved) + ' AmountPaid: '+ str(AmountPaid) +  'DateAndTime: '+ str(today.isoformat())
                        RecordReady = 0
                    VertPosOld = VertPos


#Pagebreak Level - to be improved later
#    scraperwiki.sqlite.save(unique_keys=[ 'RecNo' ], data={ 'RecNo' : str(RecNo) , 'Receiver' : Receiver, 'Subject' : Subject, 'Year' : Year , 'AmountApproved' : AmountApproved, 'AmountPaid' : AmountPaid})# open tbd
import scraperwiki
import urllib
import lxml.etree 
import re
import locale
from datetime import date

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8') # use German locale; name might vary with platform >>>
encoding = locale.nl_langinfo(locale.CODESET) #encode: how data comes in, decode: how data gets out
print 'Encoding: ', encoding # tells what codeset is used, dont remove, from time to time necessary to activate code



# Niedersachsen - have a look, there are several Programs - http://www.mw.niedersachsen.de/live/live.php?navigation_id=5679&article_id=15575&_psmand=18
pdfurl = "http://www.mw.niedersachsen.de/download/59986"

pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)

RecNo = 0 

for page in root:

    assert page.tag == 'page'

    pagelines = {}
    if RecNo <= 1:   # is there a function page number ?, so its suppose, for the first page there is min 1 record
        TableContentStart = 145 # remove the lastdigit for Line number, the last digit is unknown, the 1st page is 288, other pages 119
    else:
        TableContentStart = 47 # remove the lastdigit for Line number, the last digit is unknown, the 1st page is 288, other pages 119
    NumberOfColumns = 4 # PROBEM: DOES NOT WORK WHEN COLUMN IS PARTIALLY EMPTY Number of Columns where data has to be retrieved
    Initial = 0
    VertPosOld =0
    textOld = ''
    RecordReady = 0

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

#Receiver # Thats the structure of a field in a pdf which can have one or more lines.
                    if (len(re.findall('left="59"',lxml.etree.tostring(v)))) == 1:
                        if ((VertPosOld < VertPos) and (VertPosOld > 0)):
                            text = textOld + lxml.etree.tostring(v, encoding=unicode, method='text')
                        else:
                            text = lxml.etree.tostring(v, encoding=unicode, method='text')
                        Receiver = text              
                        textOld = text

# Subject
                    if (len(re.findall('left="281"',lxml.etree.tostring(v)))) == 1:
                        if ((VertPosOld < VertPos) and (VertPosOld > 0)):
                            text = textOld + lxml.etree.tostring(v, encoding=unicode, method='text')
                        else:
                            text = lxml.etree.tostring(v, encoding=unicode, method='text')
                            RecordReady = 1
                        Subject = text
                        textOld = text

# Year # Thats the structure of a field which has one line - to be tested if the same logic as for multiple lines can be applied
                    if (len(re.findall('left="486"',lxml.etree.tostring(v)))) == 1:
                        text = re.match('(?s)<.*?>(.*)</.*?>', lxml.etree.tostring(v)).group(1)
                        RecNo += 1 # use a place where I know there is always exactly one line, can be improved somewhere else
#                        print 'RecNo', RecNo # also on the wrong place, best would be at then end, but I am not sure is there min one line in the last field
                        textOld = ''
                        Year = text                


# Year # The year of the payment
                    if (len(re.findall('left="557"',lxml.etree.tostring(v)))) == 1:
                        text = re.match('(?s)<.*?>(.*)</.*?>', lxml.etree.tostring(v)).group(1)
                        textOld = ''
                        YearPayment = text                

#AmountApproved
#                    if (len(re.findall('left="621"|left="626"|left="632"|left="637"|left="641"',lxml.etree.tostring(v)))) == 1:
                    if (((len(re.findall('left="621"|left="626"|left="632"|left="637"|left="641"',lxml.etree.tostring(v)))) == 1) and ((len(re.findall('left="696"|left="700"|left="707"|left="711"|left="715"',lxml.etree.tostring(v)))) <> 1)):
                        text = re.match('(?s)<.*?>(.*)</.*?>', lxml.etree.tostring(v)).group(1)
                        textOld = ''
                        AmountApproved = float(text[0:(text).find(' ')].replace('.','').replace(',','.')) 
                        if RecNo >= 1:
                            scraperwiki.sqlite.save(unique_keys=[ 'RecNo' ], data={ 'RecNo' : RecNo , 'Receiver' : Receiver, 'Subject' : Subject, 'Year' :
Year , 'AmountApproved' : AmountApproved, 'AmountPaid' : 0, 'DateAndTime' : today.isoformat()})
                            print  'xRecNo: ' + str(RecNo) + ' Receiver: '+ Receiver + ' Subject: ' + Subject + ' Year: ' + str(Year) + ' AmountApproved: ' + str(AmountApproved) + ' AmountPaid: 0'+  'DateAndTime: '+ str(today.isoformat())

#AmountPaid
#                    if (len(re.findall('left="696"|left="700"|left="707"|left="711"|left="715"',lxml.etree.tostring(v)))) == 1: 
                    if (((len(re.findall('left="621"|left="626"|left="632"|left="637"|left="641"',lxml.etree.tostring(v)))) == 1) and ((len(re.findall('left="696"|left="700"|left="707"|left="711"|left="715"',lxml.etree.tostring(v)))) == 1)):
                        text = re.match('(?s)<.*?>(.*)</.*?>', lxml.etree.tostring(v)).group(1)
                        textOld = ''
                        AmountPaid = float(text[0:(text).find(' ')].replace('.','').replace(',','.')) 
#                        print 'AmountPaid: ', AmountPaid

                        if RecNo >= 1:
                            scraperwiki.sqlite.save(unique_keys=[ 'RecNo' ], data={ 'RecNo' : RecNo , 'Receiver' : Receiver, 'Subject' : Subject, 'Year' : Year , 'AmountApproved' : 0, 'AmountPaid' : AmountPaid , 'DateAndTime' : today.isoformat()})
                            print  'yRecNo: ' + str(RecNo) + ' Receiver: '+ Receiver + ' Subject: ' + Subject + ' Year: ' + str(Year) + ' AmountApproved: ' + str(AmountApproved) + ' AmountPaid: '+ str(AmountPaid) +  'DateAndTime: '+ str(today.isoformat())
                        RecordReady = 0
                    VertPosOld = VertPos


#Pagebreak Level - to be improved later
#    scraperwiki.sqlite.save(unique_keys=[ 'RecNo' ], data={ 'RecNo' : str(RecNo) , 'Receiver' : Receiver, 'Subject' : Subject, 'Year' : Year , 'AmountApproved' : AmountApproved, 'AmountPaid' : AmountPaid})