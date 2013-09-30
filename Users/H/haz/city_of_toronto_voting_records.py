import csv
import scraperwiki
from bs4 import BeautifulSoup
from twill.commands import *

# Need to make the hidden download field writeable
config('readonly_controls_writeable', '+')

# The function that fetches a csv given a member id
def fetch_data(id, member):
    # Grab the voting form
    go("http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberVoteReport")
    
    # Fill out the form with the id, and set it to download
    fv("2", "memberId", id)
    fv("2", "download", "Y")
    submit()
    raw_data = show().decode("utf-8", errors="replace").split("\n")[:-1]
    revised_data = ['"Member",' + raw_data[0]] + ['"' + member + '",' + line for line in raw_data[1:]]
    return revised_data


# Grab the list of members
soup = BeautifulSoup(scraperwiki.scrape('http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberVoteReport'))
form = soup.find_all("form")[1]
select = form.find_all("select")[2]

# Go through each member, and download their data
DATA = []
for opt in select.find_all("option")[1:]:# <-- Uncomment this line for the full version
#for opt in select.find_all("option")[1:3]:# <-- Used for testing
    memberVal = opt.get('value')
    memberName = opt.get_text()
    print "Fetching data for %s (%s)" % (memberName, memberVal)
    DATA.append(fetch_data(memberVal, memberName))

# Aggregate and save the entire data
ALL_DATA = [DATA[0][0]]
for d in DATA:
    ALL_DATA.extend(d[1:])

headers = list(csv.reader([ALL_DATA[0]], delimiter=',', quotechar='"'))[0]
csv_data = list(csv.reader([line.encode(errors='replace') for line in ALL_DATA[1:]], delimiter=',', quotechar='"'))
#print len(csv_data)
#print len(csv_data[0])
#print csv_data[0]
#print csv_data[-1]
#print ALL_DATA[0]
#print headers
#assert False

# The headers need to be simple text
headers[2] = 'Date and Time'
headers[3] = 'Agenda Item Num'

# We need a unique key for each entry
key = 1
all_data = []
for line in csv_data:
    data = {'key': str(key)}
    key += 1
    for i in range(len(headers)):
        data[headers[i]] = line[i]
    all_data.append(data)

# Save them all at once
scraperwiki.sqlite.save(unique_keys=['key'], data=all_data)

import csv
import scraperwiki
from bs4 import BeautifulSoup
from twill.commands import *

# Need to make the hidden download field writeable
config('readonly_controls_writeable', '+')

# The function that fetches a csv given a member id
def fetch_data(id, member):
    # Grab the voting form
    go("http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberVoteReport")
    
    # Fill out the form with the id, and set it to download
    fv("2", "memberId", id)
    fv("2", "download", "Y")
    submit()
    raw_data = show().decode("utf-8", errors="replace").split("\n")[:-1]
    revised_data = ['"Member",' + raw_data[0]] + ['"' + member + '",' + line for line in raw_data[1:]]
    return revised_data


# Grab the list of members
soup = BeautifulSoup(scraperwiki.scrape('http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberVoteReport'))
form = soup.find_all("form")[1]
select = form.find_all("select")[2]

# Go through each member, and download their data
DATA = []
for opt in select.find_all("option")[1:]:# <-- Uncomment this line for the full version
#for opt in select.find_all("option")[1:3]:# <-- Used for testing
    memberVal = opt.get('value')
    memberName = opt.get_text()
    print "Fetching data for %s (%s)" % (memberName, memberVal)
    DATA.append(fetch_data(memberVal, memberName))

# Aggregate and save the entire data
ALL_DATA = [DATA[0][0]]
for d in DATA:
    ALL_DATA.extend(d[1:])

headers = list(csv.reader([ALL_DATA[0]], delimiter=',', quotechar='"'))[0]
csv_data = list(csv.reader([line.encode(errors='replace') for line in ALL_DATA[1:]], delimiter=',', quotechar='"'))
#print len(csv_data)
#print len(csv_data[0])
#print csv_data[0]
#print csv_data[-1]
#print ALL_DATA[0]
#print headers
#assert False

# The headers need to be simple text
headers[2] = 'Date and Time'
headers[3] = 'Agenda Item Num'

# We need a unique key for each entry
key = 1
all_data = []
for line in csv_data:
    data = {'key': str(key)}
    key += 1
    for i in range(len(headers)):
        data[headers[i]] = line[i]
    all_data.append(data)

# Save them all at once
scraperwiki.sqlite.save(unique_keys=['key'], data=all_data)

