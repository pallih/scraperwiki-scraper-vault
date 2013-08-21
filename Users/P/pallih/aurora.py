import scraperwiki
import requests
import lxml.html
import yaml
import time
import datetime
import re
url = 'http://en.vedur.is/weather/forecasts/aurora/'

regex = re.compile(".*VI.data.aurora.idx = ([^if]+)")
response = requests.get(url)
root = lxml.html.fromstring(response.text)
script = root.xpath('//div[@class="pgextra1"]/div[@class="wrap"]/script')[0]

# /html/body/div/div[3]/div/script


r = regex.search(script.text)
#print script.text
#print r.groups()[0].replace('\n','')
#print script.text[155:-100]

#stuff = script.text[155:-100]

stuff = yaml.load(r.groups()[0].replace('\n',''))

#print stuff

today = datetime.date.today()

todaysdate = today.strftime('%y%m%d')
#print todaysdate

for item in stuff:
    record = {}
    print repr(str(item)), repr(todaysdate)
    #print type(item), type(int(todaysdate))
    record['year'] = '20' + str(item)[:2]
    record['month'] = str(item)[2:4]
    record['date'] = str(item)[4:]
    record['forecast'] = stuff[item]['act']
    if todaysdate == str(item):
        print 'this is today'
    print record
    #date_object = time.strptime(record['year']+record['month']+record['date'], "%Y%m%d") 
    #mytime = datetime.datetime.strptime(record['year']+record['month']+record['date'], "%Y%m%d").time()
    #mydatetime = datetime.datetime.combine(datetime.date.today(), mytime)
    #print mydatetime
    #print item, stuff[item]['act']
    #print record

exit()
for key, value in stuff.iteritems() :
    print key, value