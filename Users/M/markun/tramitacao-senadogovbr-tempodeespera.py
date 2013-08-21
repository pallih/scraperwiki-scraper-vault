import urllib
import simplejson
import re
import datetime

today = datetime.datetime.today()

url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&name=tramitacao-senadogovbr"
results = simplejson.load(urllib.urlopen(url))

for result in results:
    if (re.search(re.compile("Recebido nest*."), result['action'])) :
        milestone = datetime.datetime.strptime(result['date'],'%d/%m/%Y')
        timeago = today-milestone        
        print "Parado na " + result['where'] + " durante " + str(timeago.days) + " dias"
        break