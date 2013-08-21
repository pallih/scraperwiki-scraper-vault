import scraperwiki
from bs4 import BeautifulSoup
import urllib2
import time
import simplejson

candidates = ["obama","romney"]


for candidate in candidates:
    url = "http://transparencydata.com/api/1.0/contributions.json?apikey=aca140604ac8473ba552f8bdf50c66ac&recipient_ft=%s&cycle=2012" % (candidate)
    response = simplejson.loads(scraperwiki.scrape(url))
    time.sleep(2)
    for entry in response:
        output = {}
        #transaction_id,amount, date, recipient_name, contributer_name
        output['ID'] = entry['transaction_id']
        output['Amount'] = entry['amount']
        output['Date'] = entry['date']
        output['Recipient'] = candidate
        output['Contributor'] = entry['contributor_name']
        scraperwiki.sqlite.save(unique_keys=['ID'],data=output)

