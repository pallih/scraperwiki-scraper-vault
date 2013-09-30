###       FCC Application Filter           ###
###       Author: Stephen Finney           ###
###                                        ###
###       File name legend (.dat)          ###
###       AD = Application Data            ###
###       MK = Market Data                 ###
###       EN = Entity                      ###
###       HD = Application License/Header  ###
###       LO = Location                    ###

import scraperwiki
import dateutil.parser
import zipfile
import urllib
import csv
import re
from time import time
from operator import itemgetter


print "Creating tables..."
scraperwiki.sqlite.execute("PRAGMA synchronous=OFF")
scraperwiki.sqlite.execute("PRAGMA journal_mode=MEMORY")
scraperwiki.sqlite.execute("BEGIN TRANSACTION")
scraperwiki.sqlite.execute("drop table 'Application Info'") 
scraperwiki.sqlite.execute("drop table 'Last Updated'") 
scraperwiki.sqlite.execute("create table 'Application Info'(" + 
      "'File Number' text, 'Call Sign' str, 'Applicant Name' str," + 
      "'FRN' str, 'Purpose' str, 'Receipt Date' date," + 
      "'Status' str, 'Channel Block' char, 'Market' str, 'Location' str, 'System ID' str)")
scraperwiki.sqlite.execute("create table 'Last Updated'(Date datetime)")


### Download of data from FCC website ###
download = time()
url = 'http://wireless.fcc.gov/uls/data/complete/a_cell.zip'
print "Downloading data..."
urllib.urlretrieve(url, "data.zip")
after_download = time()
diff_download = after_download - download


### Extracting relevant files ###
print "Extracting files..."
z = zipfile.ZipFile("data.zip")
files = ['AD.dat', 'MK.dat', 'EN.dat', 'HD.dat', 'LO.dat', 'counts']
for name in z.namelist():
    if name in files:
        with open(name, "wb") as code:
            code.write(z.read(name))


### Reading and recording data from files ###
### Store date of last modification to data from COUNTS file ###
print "Recording date of most recent data update..."
with open("counts") as f:                    
    counts = f.read()
    entry = {}
    date = dateutil.parser.parse( counts[counts.find('File Creation Date:')+20:counts.find("\r\n")].replace(" EST","") )
    entry['Date'] = date.date().strftime("%A %B %d, %Y")
    scraperwiki.sqlite.save(unique_keys=['Date'], data=entry, table_name="Last Updated")


### Store data from Application License/Header file ###
print "Recording header data..."
with open("HD.dat") as f:
    call_signs = []
    reader = csv.reader(f, delimiter='|')
    for row in reader:
        call_signs.append(row[4])


### Store data from Application Data file ###
print "Recording application data..."
with open("AD.dat") as f:
    records = []      # The records for the table
    purpose_defs = {'MD':'MD - Modification', 'NE':'NE - New', 'AU':'AU - Administrative Update', 
                    'NT':'NT - Required Notification', 'AM':'AM - Amendment', 'AA':'AA - Assignment of Authorization',
                    'CA':'CA - Cancelation of License', 'CB':'CB - C Block Election', 'DC':'DC - Data Correction',
                    'DU':'DU - Duplication of License', 'EX':'EX - Extension Request', 'LL':'LL - Spectrum Leasing',
                    'RL':'RL - Register Link/Location', 'RM':'RM - Renewal/Modification', 'RO':'RO - Renewal Only',
                    'TC':'TC - Transfer of Control', 'WD':'WD - Withdrawal of Application'}     

    status_defs = {'1':'1 - Pending Level 1', '2':'2 - Pending Level 2', 'A':'A - A Granted', 'C':'C - Consented To', 'D':'D - Dismissed',
                   'G':'G - Granted', 'H':'H - History Only', 'I':'I - Inactive', 'K':'K - Killed', 'M':'M - Consummated',
                   'N':'N - Granted in Part', 'P':'P - Pending Pack Filing', 'Q':'Q - Accepted', 'R':'R - Returned', 'S':'S - Saved',
                   'T':'T - Terminated','U':'U - Unprocessable', 'W':'W - Withdrawn', 'X':'X - N/A', 'Y':'Y - Problems with Application'}         

    reader = csv.reader(f, delimiter='|')
    for row in reader:
        entry = {}    # A single entry to be given to 'records'
        entry['System ID'] = row[1]
        if "CL" in row[2]:
            entry['File Number'] = row[2]
        else:
            entry['File Number'] = row[2].zfill(10)
        entry['Purpose'] = purpose_defs[row[4]]
        entry['Status'] = status_defs[row[5]]
        if row[10] != "":
            entry['Receipt Date'] = dateutil.parser.parse(row[10]).date().strftime("%Y-%m-%d")
        else:
            entry['Receipt Date'] = " N/A"
        records.append(entry)


### Store data from Entity file ###
print "Recording entity data..."
with open("EN.dat") as f:
    reader = csv.reader(f, delimiter='|')
    index = 0
    for row in reader:
        if index < len(records):
            entry = {}
            entry = records[index]
            entry['Call Sign'] = call_signs[index]
            entry['Applicant Name'] = re.sub('[^a-zA-Z0-9\.\,\-\#\(\)\&" "]', '', row[7])
            entry['FRN'] = row[22]
            index += 1
        else:
            break


### Store data from Market Data file ###
print "Recording market data..."
with open("MK.dat") as f:
    reader = csv.reader(f, delimiter='|')
    name_indexer = dict((p['System ID'], i) for i, p in enumerate(records))
    for row in reader:
        if name_indexer.get(str(row[1]), -1) >= 0:
            records[name_indexer.get(str(row[1]), -1)]['Market'] = str(row[5] + " - " + row[8])
            records[name_indexer.get(str(row[1]), -1)]['Channel Block'] = row[6]
        else:
            print "System ID " + str(row[1]) + " not found in other files."


### Store data from Location file ###
print "Recording location data..."
with open("LO.dat") as f:
    reader = csv.reader(f, delimiter='|')
    for row in reader:
        if name_indexer.get(str(row[1]), -1) >= 0:
            records[name_indexer.get(str(row[1]), -1)]['Location'] = str(row[19] + " " + row[20] + " " + row[21] + " " + row[22] + " " + 
                                                                         row[23] + " " + row[24] + " " + row[25] + " " + row[26])
        else:
            print "System ID " + str(row[1]) + " not found in other files."


### Saving data ###
save = time()
print "Saving " + str(len(records)) + " records..."
temp = []
for entry in records:
    if len(temp) >= 20000:
        scraperwiki.sqlite.save(unique_keys=['System ID'], data=temp, table_name="Application Info")
        temp[:] = []
    temp.append(entry)

scraperwiki.sqlite.save(unique_keys=['System ID'], data=temp, table_name="Application Info")
after_save = time()
diff_save = after_save - save

print "Download time: " + str(diff_download) + " sec"
print "Save time: " + str(diff_save) + " sec"
print "Mission Accomplished"

###       FCC Application Filter           ###
###       Author: Stephen Finney           ###
###                                        ###
###       File name legend (.dat)          ###
###       AD = Application Data            ###
###       MK = Market Data                 ###
###       EN = Entity                      ###
###       HD = Application License/Header  ###
###       LO = Location                    ###

import scraperwiki
import dateutil.parser
import zipfile
import urllib
import csv
import re
from time import time
from operator import itemgetter


print "Creating tables..."
scraperwiki.sqlite.execute("PRAGMA synchronous=OFF")
scraperwiki.sqlite.execute("PRAGMA journal_mode=MEMORY")
scraperwiki.sqlite.execute("BEGIN TRANSACTION")
scraperwiki.sqlite.execute("drop table 'Application Info'") 
scraperwiki.sqlite.execute("drop table 'Last Updated'") 
scraperwiki.sqlite.execute("create table 'Application Info'(" + 
      "'File Number' text, 'Call Sign' str, 'Applicant Name' str," + 
      "'FRN' str, 'Purpose' str, 'Receipt Date' date," + 
      "'Status' str, 'Channel Block' char, 'Market' str, 'Location' str, 'System ID' str)")
scraperwiki.sqlite.execute("create table 'Last Updated'(Date datetime)")


### Download of data from FCC website ###
download = time()
url = 'http://wireless.fcc.gov/uls/data/complete/a_cell.zip'
print "Downloading data..."
urllib.urlretrieve(url, "data.zip")
after_download = time()
diff_download = after_download - download


### Extracting relevant files ###
print "Extracting files..."
z = zipfile.ZipFile("data.zip")
files = ['AD.dat', 'MK.dat', 'EN.dat', 'HD.dat', 'LO.dat', 'counts']
for name in z.namelist():
    if name in files:
        with open(name, "wb") as code:
            code.write(z.read(name))


### Reading and recording data from files ###
### Store date of last modification to data from COUNTS file ###
print "Recording date of most recent data update..."
with open("counts") as f:                    
    counts = f.read()
    entry = {}
    date = dateutil.parser.parse( counts[counts.find('File Creation Date:')+20:counts.find("\r\n")].replace(" EST","") )
    entry['Date'] = date.date().strftime("%A %B %d, %Y")
    scraperwiki.sqlite.save(unique_keys=['Date'], data=entry, table_name="Last Updated")


### Store data from Application License/Header file ###
print "Recording header data..."
with open("HD.dat") as f:
    call_signs = []
    reader = csv.reader(f, delimiter='|')
    for row in reader:
        call_signs.append(row[4])


### Store data from Application Data file ###
print "Recording application data..."
with open("AD.dat") as f:
    records = []      # The records for the table
    purpose_defs = {'MD':'MD - Modification', 'NE':'NE - New', 'AU':'AU - Administrative Update', 
                    'NT':'NT - Required Notification', 'AM':'AM - Amendment', 'AA':'AA - Assignment of Authorization',
                    'CA':'CA - Cancelation of License', 'CB':'CB - C Block Election', 'DC':'DC - Data Correction',
                    'DU':'DU - Duplication of License', 'EX':'EX - Extension Request', 'LL':'LL - Spectrum Leasing',
                    'RL':'RL - Register Link/Location', 'RM':'RM - Renewal/Modification', 'RO':'RO - Renewal Only',
                    'TC':'TC - Transfer of Control', 'WD':'WD - Withdrawal of Application'}     

    status_defs = {'1':'1 - Pending Level 1', '2':'2 - Pending Level 2', 'A':'A - A Granted', 'C':'C - Consented To', 'D':'D - Dismissed',
                   'G':'G - Granted', 'H':'H - History Only', 'I':'I - Inactive', 'K':'K - Killed', 'M':'M - Consummated',
                   'N':'N - Granted in Part', 'P':'P - Pending Pack Filing', 'Q':'Q - Accepted', 'R':'R - Returned', 'S':'S - Saved',
                   'T':'T - Terminated','U':'U - Unprocessable', 'W':'W - Withdrawn', 'X':'X - N/A', 'Y':'Y - Problems with Application'}         

    reader = csv.reader(f, delimiter='|')
    for row in reader:
        entry = {}    # A single entry to be given to 'records'
        entry['System ID'] = row[1]
        if "CL" in row[2]:
            entry['File Number'] = row[2]
        else:
            entry['File Number'] = row[2].zfill(10)
        entry['Purpose'] = purpose_defs[row[4]]
        entry['Status'] = status_defs[row[5]]
        if row[10] != "":
            entry['Receipt Date'] = dateutil.parser.parse(row[10]).date().strftime("%Y-%m-%d")
        else:
            entry['Receipt Date'] = " N/A"
        records.append(entry)


### Store data from Entity file ###
print "Recording entity data..."
with open("EN.dat") as f:
    reader = csv.reader(f, delimiter='|')
    index = 0
    for row in reader:
        if index < len(records):
            entry = {}
            entry = records[index]
            entry['Call Sign'] = call_signs[index]
            entry['Applicant Name'] = re.sub('[^a-zA-Z0-9\.\,\-\#\(\)\&" "]', '', row[7])
            entry['FRN'] = row[22]
            index += 1
        else:
            break


### Store data from Market Data file ###
print "Recording market data..."
with open("MK.dat") as f:
    reader = csv.reader(f, delimiter='|')
    name_indexer = dict((p['System ID'], i) for i, p in enumerate(records))
    for row in reader:
        if name_indexer.get(str(row[1]), -1) >= 0:
            records[name_indexer.get(str(row[1]), -1)]['Market'] = str(row[5] + " - " + row[8])
            records[name_indexer.get(str(row[1]), -1)]['Channel Block'] = row[6]
        else:
            print "System ID " + str(row[1]) + " not found in other files."


### Store data from Location file ###
print "Recording location data..."
with open("LO.dat") as f:
    reader = csv.reader(f, delimiter='|')
    for row in reader:
        if name_indexer.get(str(row[1]), -1) >= 0:
            records[name_indexer.get(str(row[1]), -1)]['Location'] = str(row[19] + " " + row[20] + " " + row[21] + " " + row[22] + " " + 
                                                                         row[23] + " " + row[24] + " " + row[25] + " " + row[26])
        else:
            print "System ID " + str(row[1]) + " not found in other files."


### Saving data ###
save = time()
print "Saving " + str(len(records)) + " records..."
temp = []
for entry in records:
    if len(temp) >= 20000:
        scraperwiki.sqlite.save(unique_keys=['System ID'], data=temp, table_name="Application Info")
        temp[:] = []
    temp.append(entry)

scraperwiki.sqlite.save(unique_keys=['System ID'], data=temp, table_name="Application Info")
after_save = time()
diff_save = after_save - save

print "Download time: " + str(diff_download) + " sec"
print "Save time: " + str(diff_save) + " sec"
print "Mission Accomplished"

