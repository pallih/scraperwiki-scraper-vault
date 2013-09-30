import scraperwiki
import string
from scrapemark import scrape
import scraperwiki
data = scraperwiki.scrape("https://dl.dropboxusercontent.com/u/87106626/Apps.csv")
line = 0
import csv
reader = csv.reader(data.splitlines())
headerline = reader.next()
for row in reader:

     URL = row[0]
     html = scraperwiki.scrape(URL)
     #print html
     Demo = 'Watch a Demo'
     TestDrive = 'Take a Test Drive'
     try:
      i1 = string.index(html, Demo)
     except:
      i1='0'
     try:
      i2 = string.index(html, TestDrive)
     except:
      i2='0'
     #print i1
     #print i2
     data = [{'URL':URL,'Demo':i1,'TestDrive':i2 } ]

     scraperwiki.sqlite.save(unique_keys=["URL"], data=data)

import scraperwiki
import string
from scrapemark import scrape
import scraperwiki
data = scraperwiki.scrape("https://dl.dropboxusercontent.com/u/87106626/Apps.csv")
line = 0
import csv
reader = csv.reader(data.splitlines())
headerline = reader.next()
for row in reader:

     URL = row[0]
     html = scraperwiki.scrape(URL)
     #print html
     Demo = 'Watch a Demo'
     TestDrive = 'Take a Test Drive'
     try:
      i1 = string.index(html, Demo)
     except:
      i1='0'
     try:
      i2 = string.index(html, TestDrive)
     except:
      i2='0'
     #print i1
     #print i2
     data = [{'URL':URL,'Demo':i1,'TestDrive':i2 } ]

     scraperwiki.sqlite.save(unique_keys=["URL"], data=data)

