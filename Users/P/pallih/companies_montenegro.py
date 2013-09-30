#opencorporates montenegro

import scraperwiki
import re
import urllib2
import lxml.html
import time

starturl = 'http://www.crps.me/CRPSPublic/rezultatpretrageregistra.action?od='
urlend='&privrednaDjelatnost=0&naziv=&sjediste=&lice=&djelatnostId=&sortiranje=1&regBr=&prikazati=0'

#next page gif
regex = re.compile("desno.gif")

def process(html):
    root = lxml.html.fromstring(html)
    for td in root.xpath('//tr[@class="podaci"]/.'):
        record = {}
        record['registration_number'] = td[0].text.strip()
        record['identification_number'] = td[1].text.strip()
        record['business_activity'] = td[2].text.strip()
        record['name'] = td[3].text.strip()
        record['activity'] = td[4].text.strip()
        record['place'] = td[5].text.strip()
        record['status'] = td[6].text.strip()
        record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())
        record['url'] = 'http://www.crps.me/CRPSPublic/prikazidrustvo.action?idDosijea='+td[7][0][0].get('value')
        scraperwiki.sqlite.save(['registration_number'], data=record, table_name='montenegro-companies')

def get(number):
    url = starturl + str(number) + urlend
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    html = response.read()
    process(html)
    next_page= regex.findall(html)
    if next_page:
        number = int(number)+15
        print 'There is a next page (starting with record number ',number,')'
        update_statement= 'update runtime_info SET lastnumber='+ '"' +str(number)+ '"'
        scraperwiki.sqlite.execute(update_statement)
        scraperwiki.sqlite.commit()
        get(number)
    else:
        print 'No more results! Start again on next run!'
        record = {}
        record ['lastnumber'] = '1'
        scraperwiki.sqlite.execute("drop table if exists runtime_info")
        scraperwiki.sqlite.save(['lastnumber'], data=record, table_name='runtime_info')

#Runtime info setup:
#record = {}
#record ['lastnumber'] = '1'
#scraperwiki.sqlite.save(['lastnumber'], data=record, table_name='runtime_info')

selection_statement = '* from runtime_info'
search_string = scraperwiki.sqlite.select(selection_statement)
last_done = search_string[0]

print 'Last result page done was ', int(last_done['lastnumber'])+14 / 15

get(last_done['lastnumber'])







#opencorporates montenegro

import scraperwiki
import re
import urllib2
import lxml.html
import time

starturl = 'http://www.crps.me/CRPSPublic/rezultatpretrageregistra.action?od='
urlend='&privrednaDjelatnost=0&naziv=&sjediste=&lice=&djelatnostId=&sortiranje=1&regBr=&prikazati=0'

#next page gif
regex = re.compile("desno.gif")

def process(html):
    root = lxml.html.fromstring(html)
    for td in root.xpath('//tr[@class="podaci"]/.'):
        record = {}
        record['registration_number'] = td[0].text.strip()
        record['identification_number'] = td[1].text.strip()
        record['business_activity'] = td[2].text.strip()
        record['name'] = td[3].text.strip()
        record['activity'] = td[4].text.strip()
        record['place'] = td[5].text.strip()
        record['status'] = td[6].text.strip()
        record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())
        record['url'] = 'http://www.crps.me/CRPSPublic/prikazidrustvo.action?idDosijea='+td[7][0][0].get('value')
        scraperwiki.sqlite.save(['registration_number'], data=record, table_name='montenegro-companies')

def get(number):
    url = starturl + str(number) + urlend
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    html = response.read()
    process(html)
    next_page= regex.findall(html)
    if next_page:
        number = int(number)+15
        print 'There is a next page (starting with record number ',number,')'
        update_statement= 'update runtime_info SET lastnumber='+ '"' +str(number)+ '"'
        scraperwiki.sqlite.execute(update_statement)
        scraperwiki.sqlite.commit()
        get(number)
    else:
        print 'No more results! Start again on next run!'
        record = {}
        record ['lastnumber'] = '1'
        scraperwiki.sqlite.execute("drop table if exists runtime_info")
        scraperwiki.sqlite.save(['lastnumber'], data=record, table_name='runtime_info')

#Runtime info setup:
#record = {}
#record ['lastnumber'] = '1'
#scraperwiki.sqlite.save(['lastnumber'], data=record, table_name='runtime_info')

selection_statement = '* from runtime_info'
search_string = scraperwiki.sqlite.select(selection_statement)
last_done = search_string[0]

print 'Last result page done was ', int(last_done['lastnumber'])+14 / 15

get(last_done['lastnumber'])







