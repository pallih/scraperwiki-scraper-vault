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

     URL = row[0]+'&tab=d'
     html = scraperwiki.scrape(URL)
     #print html
     Demo = 'j_id349'
     TD = html.split(Demo)
     try:
      i1 = TD[1].split('<script')
      Code = i1[0]
     except:
      Code = ''
     data = [{'URL':URL,'Code':Code} ]

     scraperwiki.sqlite.save(unique_keys=["URL"], data=data)

