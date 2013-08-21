import scraperwiki
import urllib
import lxml.etree 
import re
import locale
from datetime import date

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8') # use German locale; name might vary with platform >>>
encoding = locale.nl_langinfo(locale.CODESET) #encode: how data comes in, decode: how data gets out
print 'Encoding: ', encoding # tells what codeset is used, dont remove, from time to time necessary to activate code

#Baden-Wuerttemberg
pdfurl = "http://www.rwb-efre.baden-wuerttemberg.de/doks/Verzeichnis%20der%20Beguenstigten%20RWB-EFRE%20Stand%2031.12.2010.pdf"

#Bavaria
# pdfurl = "http://www.stmwivt.bayern.de/EFRE/_Downloads/Wettbewerbsfaehigkeit_Beschaeftigung/EU_Transparenzliste_V1-20062011.pdf"

# Hessen 
# pdfurl = "http://www.wirtschaft.hessen.de/irj/servlet/prt/portal/prtroot/slimp.CMReader/HMWVL_15/HMWVL_Internet/med/915/915503c6-cddd-0b11-53a1-6e91921321b2,22222222-2222-2222-2222-222222222222,true"

pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)

RecNo = 0 

for page in root:

    assert page.tag == 'page'

    pagelines = {}
    TableContentStart = 159 # this means line 16, the last digit is unknown
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
            if (VertPos >= TableContentStart): # first line of values in the table, below header and header line of table

#Receiver
# Thats the structure of a field in a pdf which can have one or more lines.
                    if (len(re.findall('left="44"',lxml.etree.tostring(v)))) == 1:
                        if ((VertPosOld < VertPos) and (VertPosOld > 0)):
                            text = textOld + lxml.etree.tostring(v, encoding=unicode, method='text')
                        else:
                            text = lxml.etree.tostring(v, encoding=unicode, method='text')
                        Receiver = text              
                        textOld = text

# Subject
                    if (len(re.findall('left="150"',lxml.etree.tostring(v)))) == 1:
                        if ((VertPosOld < VertPos) and (VertPosOld > 0)):
                            text = textOld + lxml.etree.tostring(v, encoding=unicode, method='text')
                        else:
                            text = lxml.etree.tostring(v, encoding=unicode, method='text')
                            RecordReady = 1
                        Subject = text
                        textOld = text

# Year
# Thats the structure of a field which has one line - to be tested if the same logic as for multiple lines can be applied
                    if (len(re.findall('left="385"',lxml.etree.tostring(v)))) == 1:
                        text = re.match('(?s)<.*?>(.*)</.*?>', lxml.etree.tostring(v)).group(1)
                        RecNo += 1 # use a place where I know there is always exactly one line, can be improved somewhere else
                        print 'RecNo', RecNo # also on the wrong place, best would be at then end, but I am not sure is there min one line in the last field
                        textOld = ''
                        Year = text                

#AmountApproved
                    if (len(re.findall('left="432"|left="433"|left="434"|left="435"|left="436"|left="437"|left="438"|left="439"|left="440"|left="441"|left="442"|left="443"|left="444"',lxml.etree.tostring(v)))) == 1:
                        text = re.match('(?s)<.*?>(.*)</.*?>', lxml.etree.tostring(v)).group(1)
                        textOld = ''
                        AmountApproved = float(text[0:(text).find(' ')].replace('.','').replace(',','.'))
                        if RecNo >= 1:
                            scraperwiki.sqlite.save(table_name="EFRE_EU_GERMANY_BADEN_WUERTTEMBERG", unique_keys=[ 'RecNo' ], data={ 'RecNo' : RecNo , 'Receiver' : Receiver, 'Subject' : Subject, 'Year' :
Year , 'AmountApproved' : AmountApproved, 'AmountPaid' : 0, 'DateAndTime' : today.isoformat()})
                            print  'xRecNo: ' + str(RecNo) + ' Receiver: '+ Receiver + ' Subject: ' + Subject + ' Year: ' + str(Year) + ' AmountApproved: ' + str(AmountApproved) + ' AmountPaid: 0' +  'DateAndTime: '+ str(today.isoformat())

#AmountPaid
                    if (len(re.findall('left="487"|left="488"|left="489"|left="490"|left="491"|left="492"|left="493"|left="494"|left="495"|left="496"|left="497"|left="498"|left="499"',lxml.etree.tostring(v)))) == 1:
                        text = re.match('(?s)<.*?>(.*)</.*?>', lxml.etree.tostring(v)).group(1)
                        textOld = ''
                        AmountPaid = float(text[0:(text).find(' ')].replace('.','').replace(',','.'))
                        if RecNo >= 1:
                            scraperwiki.sqlite.save(table_name="EFRE_EU_GERMANY_BADEN_WUERTTEMBERG", unique_keys=[ 'RecNo' ], data={ 'RecNo' : RecNo , 'Receiver' : Receiver, 'Subject' : Subject, 'Year' : Year , 'AmountApproved' : 0, 'AmountPaid' : AmountPaid , 'DateAndTime' : today.isoformat()})
                            print  'yRecNo: ' + str(RecNo) + ' Receiver: '+ Receiver + ' Subject: ' + Subject + ' Year: ' + str(Year) + ' AmountApproved: ' + str(AmountApproved) + ' AmountPaid: '+ str(AmountPaid) +  'DateAndTime: '+ str(today.isoformat())
                        RecordReady = 0
                    VertPosOld = VertPos


#Pagebreak Level - to be improved later
#    scraperwiki.sqlite.save(unique_keys=[ 'RecNo' ], data={ 'RecNo' : str(RecNo) , 'Receiver' : Receiver, 'Subject' : Subject, 'Year' : Year , 'AmountApproved' : AmountApproved, 'AmountPaid' : AmountPaid})


