import scraperwiki
import csv       

# Map of Orgs, Venues and Events?
Organisations = []
Organisations.append('Bluecoat')
Organisations.append('FACT')
Organisations.append('St Georges Hall')
Organisations.append('Tate')
Organisations.append('Walker')
Organisations.append('Phil')


BiennialOrgMap = {}
BiennialOrgMap['Biennial'] = 'N/A'
BiennialOrgMap['Bluecoat'] = 'Bluecoat'
BiennialOrgMap['Coach Shed'] = 'N/A'
BiennialOrgMap['Dock area'] = 'N/A'
BiennialOrgMap['FACT'] = 'FACT'
BiennialOrgMap['Fusebox'] = 'N/A'
BiennialOrgMap['Greenland Street'] = 'N/A'
BiennialOrgMap['Open Eye'] = 'N/A'
BiennialOrgMap['St Georges Hall'] = 'St Georges Hall'
BiennialOrgMap['St Lukes'] = 'N/A'
BiennialOrgMap['Tate'] = 'Tate'
BiennialOrgMap['Town centre'] = 'N/A'
BiennialOrgMap['Walker'] = 'Walker'

# LARC Engagment Data

# Collection of Data from Various Orgs
sample = {}

sample['DataSource'] = ''

# Where is the data from
sample['Organisation'] = ''
sample['Venue'] = ''
sample['Event'] = ''

# What type of data
sample['Type'] = '' # Engagment or Attendence or Feedback

# About the data collected
sample['Age'] = ''
sample['AgeGroup'] = ''
sample['Gender'] = ''

# When was the data collected
sample['Date'] = ''
sample['Year'] = ''
sample['Month'] = ''
sample['Quater'] = ''

# Location for this data sample
sample['PostCode'] = ''
sample['FirstPartOfPostCode'] = ''
sample['City'] = ''
sample['County'] = ''
sample['Country'] = ''

# We can cache this for later if we wanted to:
sample['Lat'] = ''
sample['Long'] = ''

# Might have more then one person in a single record
sample['count'] = 1

# Dataset 1: Everyman_Playhouse_Schools_data.csv

myID = 0;

data = scraperwiki.scrape("http://mojo-projects.com/hack4culture/Engagment/Everyman_Playhouse_Schools_data.csv")
    
reader = csv.reader(data.splitlines())

for row in reader:
    if myID:
        insert = {}
        insert['myID'] = myID;
        insert['DataSource'] = 'http://mojo-projects.com/hack4culture/Engagment/Everyman_Playhouse_Schools_data.csv'
        insert['Organisation'] = 'EveryManAndPlayHouse'
        insert['Type'] = 'Engagment'

        #splitAddress = row[3].split(',')

        #insert['PostCode'] = splitAddress[-1]
    
        insert['PostCode'] = row[6]
        splitPostCode = insert['PostCode'].split(' ')
        
        insert['FirstPartOfPostCode'] = splitPostCode[0]
        scraperwiki.sqlite.save(unique_keys=['myID'], data=insert)

    myID = myID + 1

# FACT_Engagement_data.csv
data = scraperwiki.scrape("http://mojo-projects.com/hack4culture/Engagment/FACT_Engagement_data.csv")
    
reader = csv.reader(data.splitlines())

for row in reader:
    if myID:
        insert = {}
        insert['myID'] = myID;
        insert['DataSource'] = 'http://mojo-projects.com/hack4culture/Engagment/FACT_Engagement_data.csv'
        insert['Organisation'] = 'EveryManAndPlayHouse'
        insert['Type'] = 'Engagment'

    
        insert['PostCode'] = row[0]
        splitPostCode = insert['PostCode'].split(' ')
        
        insert['FirstPartOfPostCode'] = splitPostCode[0]
        scraperwiki.sqlite.save(unique_keys=['myID'], data=insert)

    myID = myID + 1
# Liverpool_Philharmonic_Engagement.csv
data = scraperwiki.scrape("http://mojo-projects.com/hack4culture/Engagment/Liverpool_Philharmonic_Engagement.csv")
    
reader = csv.reader(data.splitlines())
philRow = 0
for row in reader:
    if philRow:
        insert = {}
        insert['myID'] = myID;
        insert['DataSource'] = 'http://mojo-projects.com/hack4culture/Engagment/Liverpool_Philharmonic_Engagement.csv'
        insert['Organisation'] = 'Phil'
        insert['Type'] = 'Engagment'

        #splitAddress = row[3].split(',')

        #insert['PostCode'] = splitAddress[-1]
    
        insert['PostCode'] = row[5]
        splitPostCode = insert['PostCode'].split(' ')
        
        insert['FirstPartOfPostCode'] = splitPostCode[0]
        scraperwiki.sqlite.save(unique_keys=['myID'], data=insert)

    philRow = philRow + 1
    myID = myID + 1

# monitoring_tracking_young_dada_projects_2011_without_namesv2.csv
import scraperwiki
import csv       

# Map of Orgs, Venues and Events?
Organisations = []
Organisations.append('Bluecoat')
Organisations.append('FACT')
Organisations.append('St Georges Hall')
Organisations.append('Tate')
Organisations.append('Walker')
Organisations.append('Phil')


BiennialOrgMap = {}
BiennialOrgMap['Biennial'] = 'N/A'
BiennialOrgMap['Bluecoat'] = 'Bluecoat'
BiennialOrgMap['Coach Shed'] = 'N/A'
BiennialOrgMap['Dock area'] = 'N/A'
BiennialOrgMap['FACT'] = 'FACT'
BiennialOrgMap['Fusebox'] = 'N/A'
BiennialOrgMap['Greenland Street'] = 'N/A'
BiennialOrgMap['Open Eye'] = 'N/A'
BiennialOrgMap['St Georges Hall'] = 'St Georges Hall'
BiennialOrgMap['St Lukes'] = 'N/A'
BiennialOrgMap['Tate'] = 'Tate'
BiennialOrgMap['Town centre'] = 'N/A'
BiennialOrgMap['Walker'] = 'Walker'

# LARC Engagment Data

# Collection of Data from Various Orgs
sample = {}

sample['DataSource'] = ''

# Where is the data from
sample['Organisation'] = ''
sample['Venue'] = ''
sample['Event'] = ''

# What type of data
sample['Type'] = '' # Engagment or Attendence or Feedback

# About the data collected
sample['Age'] = ''
sample['AgeGroup'] = ''
sample['Gender'] = ''

# When was the data collected
sample['Date'] = ''
sample['Year'] = ''
sample['Month'] = ''
sample['Quater'] = ''

# Location for this data sample
sample['PostCode'] = ''
sample['FirstPartOfPostCode'] = ''
sample['City'] = ''
sample['County'] = ''
sample['Country'] = ''

# We can cache this for later if we wanted to:
sample['Lat'] = ''
sample['Long'] = ''

# Might have more then one person in a single record
sample['count'] = 1

# Dataset 1: Everyman_Playhouse_Schools_data.csv

myID = 0;

data = scraperwiki.scrape("http://mojo-projects.com/hack4culture/Engagment/Everyman_Playhouse_Schools_data.csv")
    
reader = csv.reader(data.splitlines())

for row in reader:
    if myID:
        insert = {}
        insert['myID'] = myID;
        insert['DataSource'] = 'http://mojo-projects.com/hack4culture/Engagment/Everyman_Playhouse_Schools_data.csv'
        insert['Organisation'] = 'EveryManAndPlayHouse'
        insert['Type'] = 'Engagment'

        #splitAddress = row[3].split(',')

        #insert['PostCode'] = splitAddress[-1]
    
        insert['PostCode'] = row[6]
        splitPostCode = insert['PostCode'].split(' ')
        
        insert['FirstPartOfPostCode'] = splitPostCode[0]
        scraperwiki.sqlite.save(unique_keys=['myID'], data=insert)

    myID = myID + 1

# FACT_Engagement_data.csv
data = scraperwiki.scrape("http://mojo-projects.com/hack4culture/Engagment/FACT_Engagement_data.csv")
    
reader = csv.reader(data.splitlines())

for row in reader:
    if myID:
        insert = {}
        insert['myID'] = myID;
        insert['DataSource'] = 'http://mojo-projects.com/hack4culture/Engagment/FACT_Engagement_data.csv'
        insert['Organisation'] = 'EveryManAndPlayHouse'
        insert['Type'] = 'Engagment'

    
        insert['PostCode'] = row[0]
        splitPostCode = insert['PostCode'].split(' ')
        
        insert['FirstPartOfPostCode'] = splitPostCode[0]
        scraperwiki.sqlite.save(unique_keys=['myID'], data=insert)

    myID = myID + 1
# Liverpool_Philharmonic_Engagement.csv
data = scraperwiki.scrape("http://mojo-projects.com/hack4culture/Engagment/Liverpool_Philharmonic_Engagement.csv")
    
reader = csv.reader(data.splitlines())
philRow = 0
for row in reader:
    if philRow:
        insert = {}
        insert['myID'] = myID;
        insert['DataSource'] = 'http://mojo-projects.com/hack4culture/Engagment/Liverpool_Philharmonic_Engagement.csv'
        insert['Organisation'] = 'Phil'
        insert['Type'] = 'Engagment'

        #splitAddress = row[3].split(',')

        #insert['PostCode'] = splitAddress[-1]
    
        insert['PostCode'] = row[5]
        splitPostCode = insert['PostCode'].split(' ')
        
        insert['FirstPartOfPostCode'] = splitPostCode[0]
        scraperwiki.sqlite.save(unique_keys=['myID'], data=insert)

    philRow = philRow + 1
    myID = myID + 1

# monitoring_tracking_young_dada_projects_2011_without_namesv2.csv
