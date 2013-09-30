###############################################################################
# Swale Borough Council - Democratic Services Meeting Calendar
# Scraped by permission on ScraperWiki.
# matthew@refute.me.uk 
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
from hashlib import md5
from datetime import datetime
import re

# retrieve a page
starting_url = 'http://www2.swale.gov.uk/dso/meeting_diary.asp'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# all the info is in trs
trs = soup.findAll('tr')

# ignore any recursive trs
trs = [tr for tr in trs if not tr.findChildren('tr')]

# all the res we'll need :D!
cntrd = re.compile('text-align:center')
aagenda = re.compile('\./viewagenda.*')
amins = re.compile('\./viewminutes.*')
avenue = re.compile('displayvenue.*')
acommit = re.compile('committee_details.*')

#record the index too so we can try to pick out agenda links later
trH = [tr for tr in trs if tr.findChildren(style=cntrd)] 

meetings = []

for tr in trH:
    kids = tr.findChildren()
    date = kids[0].contents[0]
    date = re.sub("&nbsp;", "", date)
    time = kids[1].contents[0] 

    agendaTr = tr.findNextSibling()

    record = {
        "date": date,
        "time": time,
        "committee": tr.findChildren('a', href=acommit),
        "venue": tr.findChildren('a', href=avenue),
        "agenda": agendaTr.findChildren('a', href=aagenda),
        "minutes": agendaTr.findChildren('a', href=amins),
        "datetime": datetime.now(),
    }

    unique = md5()
    unique.update( "%s%s" % ( date, time) )

    for item in ['venue', 'committee', 'agenda', 'minutes']:
        try: 
            linkstr = str(record[ item ][0].extract())    
            linkstr = re.sub('href="\./|href="', 'href="http://www2.swale.gov.uk/dso/', linkstr)
            record[item] = linkstr
            unique.update( linkstr )
        except IndexError, e:
            record[item] = "None"

    record['unique'] = unique.hexdigest()


    # save records to the datastore
    scraperwiki.datastore.save(["unique"], record)
###############################################################################
# Swale Borough Council - Democratic Services Meeting Calendar
# Scraped by permission on ScraperWiki.
# matthew@refute.me.uk 
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
from hashlib import md5
from datetime import datetime
import re

# retrieve a page
starting_url = 'http://www2.swale.gov.uk/dso/meeting_diary.asp'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# all the info is in trs
trs = soup.findAll('tr')

# ignore any recursive trs
trs = [tr for tr in trs if not tr.findChildren('tr')]

# all the res we'll need :D!
cntrd = re.compile('text-align:center')
aagenda = re.compile('\./viewagenda.*')
amins = re.compile('\./viewminutes.*')
avenue = re.compile('displayvenue.*')
acommit = re.compile('committee_details.*')

#record the index too so we can try to pick out agenda links later
trH = [tr for tr in trs if tr.findChildren(style=cntrd)] 

meetings = []

for tr in trH:
    kids = tr.findChildren()
    date = kids[0].contents[0]
    date = re.sub("&nbsp;", "", date)
    time = kids[1].contents[0] 

    agendaTr = tr.findNextSibling()

    record = {
        "date": date,
        "time": time,
        "committee": tr.findChildren('a', href=acommit),
        "venue": tr.findChildren('a', href=avenue),
        "agenda": agendaTr.findChildren('a', href=aagenda),
        "minutes": agendaTr.findChildren('a', href=amins),
        "datetime": datetime.now(),
    }

    unique = md5()
    unique.update( "%s%s" % ( date, time) )

    for item in ['venue', 'committee', 'agenda', 'minutes']:
        try: 
            linkstr = str(record[ item ][0].extract())    
            linkstr = re.sub('href="\./|href="', 'href="http://www2.swale.gov.uk/dso/', linkstr)
            record[item] = linkstr
            unique.update( linkstr )
        except IndexError, e:
            record[item] = "None"

    record['unique'] = unique.hexdigest()


    # save records to the datastore
    scraperwiki.datastore.save(["unique"], record)
