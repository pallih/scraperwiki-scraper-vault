# In France there are all programs in the list, the ones called FEDER are the EFRE Programs
import scraperwiki
import urllib
import lxml.etree 
import re
import locale
from datetime import date

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8') # use German locale; name might vary with platform >>>
encoding = locale.nl_langinfo(locale.CODESET) #encode: how data comes in, decode: how data gets out
print 'Encoding: ', encoding # tells what codeset is used, dont remove, from time to time necessary to activate code


# Midi Pyrenees - as pdf - maybe its better to scrape the website directly
pdfurl = "http://cartobenef.asp-public.fr/cartobenef/liste_benef_pdf.php?nivgeo=reg&codgeo=73&evenement=&order=&deb=&fi=&page=&typeFonds=&thematique=&bornMin=&bornMax=&anneeProg=&motClef="

# To get it directly from the website
# http://cartobenef.asp-public.fr/cartobenef/liste_benef.php?nivgeo=reg&codgeo=73

pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)

RecNo = 0 

for page in root:

    assert page.tag == 'page'

    pagelines = {}
    if RecNo <= 1:   # is there a function page number ?, so its suppose, for the first page there is min 1 record
        TableContentStart = 135 # remove the lastdigit for Line number, the last digit is unknown, the 1st page is 288, other pages 119
    else:
        TableContentStart = 144 # remove the lastdigit for Line number, the last digit is unknown, the 1st page is 288, other pages 119
    NumberOfColumns = 4 # do we need this field/variable ? # PROBEM: DOES NOT WORK WHEN COLUMN IS PARTIALLY EMPTY Number of Columns where data has to be retrieved
    Initial = 0
    VertPosOld =0
    textOld = ''
#    RecordReady = 0

    ProjectAmount = ''
    Receiver = ''
    Subject = ''
    Year = ''
    EuFondsConcerned = ''
    ProjectPlace = ''
    AmountApproved = ''
    NameBeneficary = ''
    RegionCode = ''
    SpenderBudgetName = ''
    AmountPaid = '' 
    today = date.today()

    for v in page:
        if v.tag == 'text':
            VertPos = int(v.attrib.get('top')) #why is this field named 'top' ?
            if (VertPos >= TableContentStart): # first line of values in the table, below header and header line of table

#Receiver # Thats the structure of a field in a pdf which can have one or more lines.
                    if (len(re.findall('left="31"',lxml.etree.tostring(v)))) == 1:
                        if ((VertPosOld < VertPos) and (VertPosOld > 0)):
                            text = textOld + lxml.etree.tostring(v, encoding=unicode, method='text')
                        else:
                            text = lxml.etree.tostring(v, encoding=unicode, method='text')
                        Receiver = text              
                        textOld = text

# Subject
                    if (len(re.findall('left="105"',lxml.etree.tostring(v)))) == 1:
                        if ((VertPosOld < VertPos) and (VertPosOld > 0)):
                            text = textOld + lxml.etree.tostring(v, encoding=unicode, method='text')
                        else:
                            text = lxml.etree.tostring(v, encoding=unicode, method='text')
                        Subject = text
                        textOld = text

#Project Amount
                    if (len(re.findall('left="207"|left="203"|left="200"|left="197"|left="193"',lxml.etree.tostring(v)))) == 1:
                        text =  lxml.etree.tostring(v, encoding=unicode, method='text')
                        text = text.replace(' ', '')             
#                        print text
                        ProjectAmount = float(text)       

#AmountApproved
                    if (len(re.findall('left="252"|left="248"|left="246"|left="243"',lxml.etree.tostring(v)))) == 1:
                        text =  lxml.etree.tostring(v, encoding=unicode, method='text')
                        text = text.replace(' ', '')             
#                        print text
                        AmountApproved = float(text)       

# EU-Fonds Concerned
                    if (len(re.findall('left="266"',lxml.etree.tostring(v)))) == 1:
                        text = re.match('(?s)<.*?>(.*)</.*?>', lxml.etree.tostring(v)).group(1)
                        EuFondsConcerned = text                

# ProjectPlace
                    if (len(re.findall('left="295"',lxml.etree.tostring(v)))) == 1:
                        if ((VertPosOld < VertPos) and (VertPosOld > 0)):
                            text = textOld + lxml.etree.tostring(v, encoding=unicode, method='text')
                        else:
                            text = lxml.etree.tostring(v, encoding=unicode, method='text')
                        ProjectPlace = text
                        textOld = text

# NameBeneficary
                    if (len(re.findall('left="343"',lxml.etree.tostring(v)))) == 1:
                        if ((VertPosOld < VertPos) and (VertPosOld > 0)):
                            text = textOld + lxml.etree.tostring(v, encoding=unicode, method='text')
                        else:
                            text = lxml.etree.tostring(v, encoding=unicode, method='text')
                        NameBeneficary = text
                        textOld = text

# RegionCode
                    if (len(re.findall('left="388"',lxml.etree.tostring(v)))) == 1:
                        text = re.match('(?s)<.*?>(.*)</.*?>', lxml.etree.tostring(v)).group(1)
#                        print 'RecNo', RecNo # also on the wrong place, best would be at then end, but I am not sure is there min one line in the last field
                        RegionCode = text 



# SpenderBudgetName
                    if (len(re.findall('left="425"',lxml.etree.tostring(v)))) == 1:
                        if ((VertPosOld < VertPos) and (VertPosOld > 0)):
                            text = textOld + lxml.etree.tostring(v, encoding=unicode, method='text')
                        else:
                            text = lxml.etree.tostring(v, encoding=unicode, method='text')
                        SpenderBudgetName = text
                        textOld = text


# ProjectCategory
                    if (len(re.findall('left="482"',lxml.etree.tostring(v)))) == 1:
                        if ((VertPosOld < VertPos) and (VertPosOld > 0)):
                            text = textOld + lxml.etree.tostring(v, encoding=unicode, method='text')
                        else:
                            text = lxml.etree.tostring(v, encoding=unicode, method='text')
                        ProjectCategory = text
                        textOld = text


# Year # Thats the structure of a field which has one line - to be tested if the same logic as for multiple lines can be applied
                    if (len(re.findall('left="527"',lxml.etree.tostring(v)))) == 1:
                        text = re.match('(?s)<.*?>(.*)</.*?>', lxml.etree.tostring(v)).group(1)
                        Year = text                

                        RecNo += 1 # use a place where I know there is always exactly one line, can be improved somewhere else

                        if RecNo >= 1:
                            scraperwiki.sqlite.save(table_name="EFRE_EU_FRANCE_MIDIPYRENEES", unique_keys=[ 'RecNo' ], data={ 'RecNo' : RecNo , 'Receiver' : Receiver, 'Subject' : Subject, 'ProjectAmount' : ProjectAmount , 'Year' : Year  , 'AmountApproved' : AmountApproved , 'EuFondsConcerned' : EuFondsConcerned , 'ProjectPlace' : ProjectPlace , 'NameBeneficary' : NameBeneficary , 'RegionCode' : RegionCode , 'SpenderBudgetName' : SpenderBudgetName , 'ProjectCategory' : ProjectCategory , 'DateAndTime' : today.isoformat()})

                            print  'yRecNo: ' + str(RecNo) + ' Receiver: '+ Receiver + ' Subject: ' + Subject + 'ProjectAmount: ' + str(ProjectAmount) + ' Year: ' + str(Year) + ' AmountApproved: ' + str(AmountApproved) + 'EuFondsConcerned: ' + EuFondsConcerned + 'ProjectPlace: '+ ProjectPlace + ' NameBeneficary: ' + NameBeneficary + ' RegionCode: ' + RegionCode + ' SpenderBudgetName: ' + SpenderBudgetName + 'ProjectCategory: ' + ProjectCategory + ' DateAndTime: '+ str(today.isoformat())
                            textOld = ''
                    VertPosOld = VertPos
