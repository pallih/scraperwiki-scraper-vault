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
 try:
     URL = row[0]+'&tab=r'
     html = scraperwiki.scrape(URL)
     temp = html.split(':postedBy')
     html = temp[1]

    
     data = [{'URL': URL, 'Raw':html}]
    
     scraperwiki.sqlite.save(unique_keys=["URL"], data=data)
 except:
    URL = '' 
    print 'Excwption'
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
 try:
     URL = row[0]+'&tab=r'
     html = scraperwiki.scrape(URL)
     temp = html.split(':postedBy')
     html = temp[1]

    
     data = [{'URL': URL, 'Raw':html}]
    
     scraperwiki.sqlite.save(unique_keys=["URL"], data=data)
 except:
    URL = '' 
    print 'Excwption'
