import scraperwiki
import urllib2
import json
import csv
import nltk
import sys
from datetime import datetime

output = csv.DictWriter(open('guardian.csv','wb'), ['headline', 'webUrl', 'body', 'date'])
output.writeheader()

page = 96

for j in range(10,page):

    guardian_data = urllib2.urlopen('http://content.guardianapis.com/search?q=protesters&section=world&from-date=2012-01-01&to-date=2012-04-14&format=json&show-fields=all&show-factboxes=all&show-references=all&api-key=jk9rzgdu38j9n57g6yna7s5v').read()

    guardian_search = json.loads(guardian_data)

    for i in range(0,50):
        guardian = {}
        guardian['headline'] = nltk.clean_html(guardian_search['response']['results'][i]['fields']['headline']).encode(sys.stdout.encoding,'replace').replace(',', ' ') 
        guardian['webUrl'] = nltk.clean_html(guardian_search['response']['results'][i]['webUrl']).encode(sys.stdout.encoding,'replace').replace(',', ' ') 
        try:
            guardian['body'] = nltk.clean_html(guardian_search['response']['results'][i]['fields']['body']).encode(sys.stdout.encoding,'replace').replace(',', ' ')
        except Exception:
            guardian['body'] = ""
        format = datetime.strptime(guardian_search['response']['results'][i]['webPublicationDate'], '%Y-%m-%dT%H:%M:%SZ')
        guardian['date'] = format.strftime('%m/%d/%Y')
    
        print i
        print guardian

        output.writerow(guardian)

import scraperwiki
import urllib2
import json
import csv
import nltk
import sys
from datetime import datetime

output = csv.DictWriter(open('guardian.csv','wb'), ['headline', 'webUrl', 'body', 'date'])
output.writeheader()

page = 96

for j in range(10,page):

    guardian_data = urllib2.urlopen('http://content.guardianapis.com/search?q=protesters&section=world&from-date=2012-01-01&to-date=2012-04-14&format=json&show-fields=all&show-factboxes=all&show-references=all&api-key=jk9rzgdu38j9n57g6yna7s5v').read()

    guardian_search = json.loads(guardian_data)

    for i in range(0,50):
        guardian = {}
        guardian['headline'] = nltk.clean_html(guardian_search['response']['results'][i]['fields']['headline']).encode(sys.stdout.encoding,'replace').replace(',', ' ') 
        guardian['webUrl'] = nltk.clean_html(guardian_search['response']['results'][i]['webUrl']).encode(sys.stdout.encoding,'replace').replace(',', ' ') 
        try:
            guardian['body'] = nltk.clean_html(guardian_search['response']['results'][i]['fields']['body']).encode(sys.stdout.encoding,'replace').replace(',', ' ')
        except Exception:
            guardian['body'] = ""
        format = datetime.strptime(guardian_search['response']['results'][i]['webPublicationDate'], '%Y-%m-%dT%H:%M:%SZ')
        guardian['date'] = format.strftime('%m/%d/%Y')
    
        print i
        print guardian

        output.writerow(guardian)

