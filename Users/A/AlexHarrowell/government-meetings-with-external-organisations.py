import scraperwiki
import urllib
import csv
import time
from hashlib import md5
import StringIO

urls = [('http://download.cabinetoffice.gov.uk/transparency/pm-meetings.csv', 'basic', '10 Downing St'), ('http://www.cabinetoffice.gov.uk/sites/default/files/resources/pm-meetings-aug-sept-2010_0.csv', 'basic', '10 Downing St'), ('http://www.cabinetoffice.gov.uk/sites/default/files/resources/pm-meetings-oct-dec-2010.csv', 'basic', '10 Downing St'), ('http://download.cabinetoffice.gov.uk/transparency/dpm-meetings.csv', 'basic', 'Deputy PM'), ('http://www.cabinetoffice.gov.uk/sites/default/files/resources/dpm-meetings-oct-dec-2010.csv', 'basic', 'Deputy PM'), ('http://download.cabinetoffice.gov.uk/transparency/co-ministers-meetings.csv', 'basic', 'Cabinet Office'), ('http://www.cabinetoffice.gov.uk/sites/default/files/resources/co-meetings-aug-sept-2010.csv', 'basic', 'Cabinet Office'), ('http://www.cabinetoffice.gov.uk/sites/default/files/resources/co-meetings-oct-dec-2010.csv', 'basic', 'Cabinet Office'), ('http://www.cabinetoffice.gov.uk/sites/default/files/resources/leaders-whips-meetings-aug-sept-2010.csv', 'basic', 'Whips'), ('http://download.cabinetoffice.gov.uk/transparency/leaders-whips-meetings.csv', 'basic', 'Whips'), ('http://www.cabinetoffice.gov.uk/sites/default/files/resources/leaders-whips-meetings-oct-dec-2010_0.csv', 'basic', 'Whips'), ('http://archive.defra.gov.uk/corporate/docs/data/hosp-bus-expen/disclosure-minister-meetings-oct2010.csv', 'basic', 'DEFRA'), ('http://archive.defra.gov.uk/corporate/docs/data/hosp-bus-expen/disclosure-minister-meetings-1011-q2.csv', 'dateofmeeting', 'DEFRA'), ('http://www.scotlandoffice.gov.uk/scotlandoffice/files/disclosure-ministerial-%20meetings-DA.csv', 'basic', 'Scotland Office'), ('http://www.scotlandoffice.gov.uk/scotlandoffice/files/disclosure-ministerial-%20meetings-DM.csv', 'basic', 'Scotland Office'), ('http://www.scotlandoffice.gov.uk/scotlandoffice/files/disclosure-ministerial-%20meetings-MM.csv', 'basic', 'Scotland Office'), ('http://www.scotlandoffice.gov.uk/scotlandoffice/files/disclosure-ministerial-external-meetings-October-December-2010-MM.csv', 'basic', 'Scotland Office'), ('http://www.scotlandoffice.gov.uk/scotlandoffice/files/disclosure-ministerial-external-meetings-October-December-2010-DM.csv', 'basic', 'Scotland Office'),('http://www.dwp.gov.uk/docs/dwp-ministerial-meetings-13-may-to-31-july-2010.csv', 'dateofmeeting', 'DWP'), ('http://www.transparency.culture.gov.uk/wp-content/uploads/2010/10/DCMS_dataset_ministerial_meetings_may_july_2010.csv', 'basic', 'DCMS'), ('http://www.transparency.culture.gov.uk/wp-content/uploads/2011/04/DCMStransparency_Oct_Dec_10_Ministerial_meetings_with_outside_gps.csv', 'basic', 'DCMS'), ('http://www.fco.gov.uk/resources/en/csv/publications/transparency/ministers-meetings-13may-to-31july2010.csv', 'basic', 'Foreign Office'), ('http://www.dft.gov.uk/datasets/disclosure-ministerial-external-meetings-dft-may-jul2010.csv', 'Transport', 'Transport'), ('http://www.communities.gov.uk/documents/corporate/xls/1752612.csv','dclgstyle', 'DCLG'), ('http://www.communities.gov.uk/documents/corporate/xls/17526121.csv', 'dclgstyle', 'DCLG'), ('http://www.bis.gov.uk/assets/biscore/corporate/docs/foi/foi-ministerial-meetings-may-july.csv', 'basic', 'BIS'), ('http://www.bis.gov.uk/assets/biscore/data/foi-ministerial-meetings-aug-sep.csv', 'basic', 'BIS'), ('http://media.education.gov.uk/assets/files/csv/disclosure%20of%20ministerial%20meetings%2013%20may%20to%2031%20july%202010.csv', 'deccstyle', 'Education'), ('http://media.education.gov.uk/assets/files/csv/disclosure%20of%20ministerial%20meetings%201%20august%20to%2030%20september%202010.csv', 'basic', 'Education'), ('http://www.mod.uk/NR/rdonlyres/05F250F2-E347-4575-806C-E78400F02E1C/0/meetingexternalorgs_augsept2010.csv', 'dateofmeeting', 'Defence'), ('http://www.mod.uk/NR/rdonlyres/7B1F23FD-EE2B-46FA-AB4F-1776001E61FD/0/ministersmeeting_externalorgs_oct_dec.csv', 'dateofmeeting', 'Defence'), ('http://www.mod.uk/NR/rdonlyres/33F201B7-5557-4FBA-A821-6BC97927D1DD/0/minister_meetings_external_org2011_jantomar.csv', 'dateofmeeting', 'Defence'), ('http://www.decc.gov.uk/assets/decc/accesstoinformation/820-huhne-external-meetings-may-july-2010.csv', 'deccstyle', 'DECC'), ('http://www.decc.gov.uk/assets/decc/accesstoinformation/807-barker-external-meetings-may-july-2010.csv', 'deccstyle', 'DECC'), ('http://www.decc.gov.uk/assets/decc/accesstoinformation/813-hendry-external-meetings-may-july-2010.csv', 'deccstyle', 'DECC'), ('http://www.decc.gov.uk/assets/decc/accesstoinformation/825-marland-external-meetings-may-july-2010.csv', 'deccstyle', 'DECC'), ('http://www.justice.gov.uk/publications/docs/ministerial-meetings-may-july-2010.csv', 'dateofmeeting', 'Justice'), ('http://www.cabinetoffice.gov.uk/sites/default/files/resources/dpm-meetings-aug-sept-2010.csv', 'dateofmeeting', 'Deputy PM'), ('http://www.hm-treasury.gov.uk/d/ministerial_meetings_may_to_july_2010.csv', 'basic', 'Treasury'), ('http://www.walesoffice.gov.uk/files/2010/08/SoS-meetings-with-external-organisations-Q2-20101.csv', 'wales', 'Welsh Office'), ('http://www.walesoffice.gov.uk/files/2010/08/Secretary-of-State-Meeting-with-External-Organisations-Q3-09-11-2010.csv', 'wales', 'Welsh Office'), ('http://www.walesoffice.gov.uk/files/2010/08/PUSS-meetings-with-External-Bodies-Q2-2010-1.csv', 'wales', 'Welsh Office'), ('http://www.walesoffice.gov.uk/files/2010/08/PUSS-Meetings-with-External-Organisations-Q3-09-11-2010.csv', 'wales', 'Welsh Office'), ('http://www.walesoffice.gov.uk/files/2010/08/SoS-Meetings-with-External-Organisations-Q4-2010.csv', 'wales', 'Welsh Office'), ('http://www.walesoffice.gov.uk/files/2010/08/PuSS-Meetings-with-External-Organisations-Q4-2010.csv', 'wales', 'Welsh Office'), ('http://www.attorneygeneral.gov.uk/GuidetoInformation/Listsandregisters/Documents/Ministerial-%20meetings_13%20May%202010%20-%2031%20July%202010.csv', 'Attorney General', 'Attorney General'), ('http://www.attorneygeneral.gov.uk/GuidetoInformation/Listsandregisters/Documents/Ministers%20meetings%20with%20outside%20organisations%201%20August%20-%2030%20September%202010.csv', 'Attorney General 1', 'Attorney General'), ('http://www.homeoffice.gov.uk/publications/about-us/corporate-publications/ministers-hospitality/ministers-hosp-dec2010.csv?view=Binary', 'Home Office', 'Home Office'), ('http://www.homeoffice.gov.uk/publications/about-us/corporate-publications/ministers-hospitality/ministers-hosp-sept10.csv?view=Binary', 'Home Office', 'Home Office'), ('http://www.homeoffice.gov.uk/publications/about-us/corporate-publications/ministers-hospitality/ministers-hospitality.csv?view=Binary', 'Home Office', 'Home Office'), ('http://www.homeoffice.gov.uk/publications/about-us/corporate-publications/ministers-gifts-jan-mar11.csv?view=Binary', 'Home Office', 'Home Office'),  ('https://www.dfid.gov.uk/Documents/datasets/sos-return-aug10.csv', 'DFID', 'DFID'), ('https://www.dfid.gov.uk/Documents/datasets/sos-return-oct-dec10.csv', 'DFID', 'DFID'), ('https://www.dfid.gov.uk/Documents/datasets/puss-qtr-info-1305-310710.csv', 'DFID', 'DFID'), ('https://www.dfid.gov.uk/Documents/datasets/puss-return-oct-dec10.csv', 'DFID', 'DFID')]

# this list is incomplete and DECC and Justice are special, apparently, having done a .csv but got it wrong
# todo: Health is a PDF. DECC doesn't provide dates and therefore they have a horses' birthday
# Clegg's disclosure for 2nd quarter is buggered -  ('http://www.cabinetoffice.gov.uk/sites/default/files/resources/dpm-meetings-aug-sept-2010.csv', 'basic', 'Deputy PM') 
# ('http://www.mod.uk/NR/rdonlyres/A4918CCA-39CE-4358-BEB6-634FD99E5361/0/meetingexternalorgs_mayjuly2010.csv', 'dateofmeeting', 'Defence')

horsesbirthday = '01/06/10'

class DataReader:

        """
        Reads raw data from csv files and combines them into complex data structures of
        primitive Python data types. Provides an alternate version of csv.DictReader that doesn't choke on anything that smells of Unicode.
        Stolen from http://mxm-mad-science.blogspot.com/2008/05/note-to-self-practical-csv-import.html - we thank you!
        """

        def __init__(self, fname, fieldnames=None, restval=None, encoding='windows-1252'):
            self.encoding = encoding
            self.fieldnames = fieldnames
            self.fname = fname
            self.restval = restval
            #self.csvfile = open(fname, 'r') #slight modification for use with stringIO
            self.csvfile = self.fname
            dialect = self.sniffDialect()
            self.dictreader = csv.DictReader(self.csvfile, fieldnames=self.fieldnames, restval=self.restval, dialect=dialect)

        def sniffDialect(self):
            for i in range(2):
                line2 = self.csvfile.readline()
            self.csvfile.seek(0)
            dialect = csv.Sniffer().sniff(line2)
            dialect.skipinitialspace = True
            return dialect

        def d2u(self, d):
            # dict to unicode
            e = self.encoding
            r = {}
            #if self.restkey in d:
                #d.pop(self.restkey)
            for key, val in d.items():
                if isinstance(val, str) : #bug - otherwise it chokes on anything with empty cells
                    r[key.decode(e)] = val.decode(e)
            return r

        def close(self):
            self.csvfile.close()

        def __iter__(self):
            return self

        def next(self):
            return self.d2u(self.dictreader.next())

def dumptodatastore(row):
    row.update(Date=ProcessDate(row['Date']))
    if row.has_key(''): #catch error in DEFRA June
        purp = row.pop('')
        purpose = 'Purpose of meeting'
        row.update((purpose)=purp)
    if row['Minister'] != '':   
        mini = (row.pop('Minister')).strip()
        row.update(Minister=mini)
        hasher = md5() # we've gotto have a unique key, but the data is such that it's not very unique
        hasher.update(str(row)) # we want to know if the same people are having multiple meetings, obviously
        row.update(uniqueid=(hasher.hexdigest())) # so we take an md5 hash of each row and use it as an unique identifier
        scraperwiki.sqlite.save(unique_keys=['uniqueid'], data=row)

def ProcessDate(rawdate):
    if rawdate != u'':
        #if '10' not in rawdate: # MOD didn't give a year. need to change this for 1Q2011!
            #rawdate = rawdate.strip() + ', 2010'
        rd = rawdate.encode('utf-8')
        date = rd.rstrip()
        print date
        try:
            d = time.strptime(date, '%b-%Y')
        except ValueError:
            try:    
                d = time.strptime(date, '%B-%Y')
            except ValueError:
                try:
                    d = time.strptime(date, '%B %Y')
                except ValueError:
                    try:
                        d = time.strptime(date, '%d/%m/%y',)
                    except ValueError:
                        try:
                            d = time.strptime(date, '%d/&m/%Y')
                        except ValueError:
                            try:
                                d = time.strptime(date, '%B-%y')
                            except ValueError:
                                try:
                                    d = time.strptime(date, '%b-%y')
                                except ValueError:
                                    try:
                                        d = time.strptime(date, '%B, %Y')
                                    except ValueError:
                                        try:
                                            d = time.strptime(date, '%b, %Y')
                                        except ValueError:
                                            print date
                                            pattern = '%b \'y'
                                            d = time.strptime(date, pattern)
                                            
    else:
        d = 'Blank'

    if d != 'Blank':
        date = time.strftime('%B %Y', d)
        return date
    else:
        return d

def BasicParser(f, department):
    reader = DataReader(f) #read into dicts
    for row in reader:
        if department == 'DEFRA':
            print row
        if row['Minister'] == 'Note': 
            break
        if 'Does not normally' in row['Minister']:
            break # DIE DIE DIE DEFRA! and DCLG!
        if row['Date'] == 'nil return':
            break
        if 'Name of Organisation' in row:
            org = row.pop('Name of Organisation')
            row.update({'Name of External Organisation': org})
        if row['Name of External Organisation'] != '':
            row.update(department=department) #probably useful to keep track by department, so add this
            if row['Minister'] != '':
                currentminister = row['Minister']
            else:
                if row['Minister'] == '':
                    row.update(Minister=currentminister)
            dumptodatastore(row)
    f.close()

def TransportParser(f, department):
    reader = DataReader(f) #read into dicts
    for row in reader:
        if row['Minister'] == 'Note:': 
            break
        if row['Name of External Organisation'] != '':
            row.update(department=department) #probably useful to keep track by department, so add this
            if row['Minister'] != '':
                currentminister = row['Minister']
            else:
                if row['Minister'] == '':
                    row.update(Minister=currentminister)
            
            dumptodatastore(row)
    f.close()

def DWPParser(f, department):
    if department == 'Attorney General':
        fields = ['Date', 'Minister', 'Name of External Organisation', 'Purpose of meeting']
    else:
        fields = ['Minister', 'Date', 'Name of External Organisation', 'Purpose of meeting']
    reader = DataReader(f, fields) #read into dicts
    for row in reader:
        if row['Minister'] is 'Note':
            break
        if 'Does not normally' in row['Minister']:
            break
        if row['Minister'] == 'Minister' or 'MEETINGS' in row['Minister']:
            continue
        if row['Minister'] == 'Minister   ': #clegg
            continue
        if row['Name of External Organisation'] != '':
            row.update(department=department) #probably useful to keep track by department, so add this
            if row['Minister'] != '':
                currentminister = row['Minister']
            else:
                row.update(Minister=currentminister)
            dumptodatastore(row)
    f.close()

def EducationParser(f, department):
    fields = ['Date', 'Name of External Organisation', 'Purpose of meeting']
    reader = DataReader(f, fieldnames=fields, restval='*') #read into dicts
    for row in reader:
        if row['Date'] != '*':
            if 'Minister' in row['Date'] or 'Secretary' in row['Date']:
                currentminister = row['Date']
            if '/' in row['Date']:
                currentdate = row['Date']
        
        if row['Name of External Organisation'] != '*':
            if row['Name of External Organisation'] != 'Name of External Organisation':
                if 'Does not normally' not in row['Name of External Organisation']:
                    row.update(Minister=currentminister, department=dept, Date=currentdate)
                    dumptodatastore(row) 
                else:
                    break
    f.close()       
    
def DECCSecretaryParser(f, department):
    fields = ['Date', 'Name of External Organisation', 'Purpose of meeting']
    currentminister = None
    reader = DataReader(f, fieldnames=fields, restval='*') #read into dicts
    for row in reader:
        if row['Name of External Organisation'] != '*':
            if row['Name of External Organisation'] != 'Name of External Organisation':
                if 'Does not normally' not in row['Date']:
                    if 'Minister' in row['Date'] or 'Secretary' in row['Date']:
                        currentminister = row['Date']
                    if row['Name of External Organisation'] != u'': #skip blank lines
                        row.update(Minister=currentminister, department=department, Date=horsesbirthday) #set dummy date for decc
                        dumptodatastore(row)
                else:
                    break
    f.close()

def DCLGParser(f, department):
    fields = ['Minister', 'Date', 'Name of External Organisation', 'Purpose of meeting']
    reader = DataReader(f, fields) #read into dicts
    for row in reader:
        if str(row['Minister']) == 'Minister':
            continue
        if '*Does not normally' in row['Minister']:
            break
        if u'Nil Return' in row.values():
            break
        else:
            row.update(department=department) #probably useful to keep track by department, so add this
            if row['Minister'] != '':
                currentminister = row['Minister']
            row.update(Minister=currentminister)
            dumptodatastore(row)
    f.close()

def WalesParser(f, department):
    fields = ['Date', 'Name of External Organisation', 'Purpose of meeting']
    reader = csv.DictReader(f, fieldnames=fields)
    for row in reader:
        if row['Date'] != '':
            if '**Does not normally' not in row['Date']:
                if 'Secretary' in row['Date'] or 'Minister' in row['Date']:
                    currentminister = row['Date']
                else:
                    if row['Date'] != 'DATE OF MEETING':
                        row.update(Minister=currentminister)
                        row.update(department=department)
                        dumptodatastore(row)
                
    f.close()


def AGParser(f, department):
    reader = csv.DictReader(f) #like BasicParser, but funny encoding doesn't work with unicode capable parser
    for row in reader:
        if row['Minister'] == 'Note': 
            break
        if 'Does not normally' in row['Minister']:
            break
        if row['Date'] == 'nil return':
            break
        if row['Name of External Organisation'] != '':
            row.update(department=department)
            if row['Minister'] != '':
                currentminister = row['Minister']
            else:
                if row['Minister'] == '':
                    row.update(Minister=currentminister)
            dumptodatastore(row)
    f.close()

def AGParser1(f, department):
    fields = ['Date', 'Minister', 'Name of External Organisation', 'Purpose of meeting']
    reader = csv.DictReader(f, fieldnames=fields)
    for row in reader:
        if row['Date'] != 'Date of meeting':
            row.update(department=department)
            dumptodatastore(row)

def HomeOfficeParser(f, department):
    fields = ['Date', 'Name of External Organisation', 'Purpose of meeting']
    reader = DataReader(f, fieldnames=fields, restval='*')
    meetings = False
    for row in reader:
        if row['Date'] == '' or 'Date of meeting' in row['Date']:
            continue
        if '[1] Does not include' in row['Date']:
            break
        if 'MEETINGS' in row['Date']:
            meetings = True
            continue
        if meetings == True:
            if 'Secretary' in row['Date'] or 'Minister' in row['Date']:
                    currentminister = row['Date']
            else:
                row.update(Minister=currentminister, department=department)
                dumptodatastore(row)

def DFIDParser(f, department):    
    fields = ['Date', 'Name of External Organisation', 'Purpose of meeting']
    reader = DataReader(f, fieldnames=fields, restval='*')
    meetings = False
    for row in reader:
        if 'Date of meeting' in row['Date']:
            meetings = True
            continue
        if 'Does not normally' in row['Date']:
            break
        if meetings == True:
            if 'Secretary' in row['Date'] or 'Minister' in row['Date']:
                currentminister = row['Date']
            elif '/' in row['Date']:
                currentdate = row['Date']
            else:
                outrow = {'Date': currentdate, 'Name of External Organisation': row['Name of External Organisation'], 'Purpose of meeting': row['Purpose of meeting'], 'Minister': currentminister}
                dumptodatastore(outrow)
                

for url in urls:
    if scraperwiki.sqlite.get_var(url[0]) == None or url[2] == 'DFID':
        input = urllib.urlopen(url[0]) #get file
        f = StringIO.StringIO(input.read())
        if url[1] == 'basic':
            BasicParser(f, url[2])
        elif url[1] == 'deccstyle':
            DECCSecretaryParser(f, url[2])
        elif url[1] == 'education':
            EducationParser(f, url[2])
        elif url[1] == 'dateofmeeting':
            DWPParser(f, url[2])
        elif url[1] == 'Transport':
            TransportParser(f, url[2])
        elif url[1] == 'dclgstyle':
            DCLGParser(f, url[2])
        elif url[1] == 'wales':
            WalesParser(f, url[2])
        elif url[1] == 'Attorney General':
            AGParser(f, url[2])
        elif url[1] == 'Attorney General 1':
            AGParser1(f, url[2])
        elif url[1] == 'Home Office':
            HomeOfficeParser(f, url[2])
        elif url[1] == 'DFID':
            DFIDParser(f, url[2])
        scraperwiki.sqlite.save_var(url[0], 'scraped')
