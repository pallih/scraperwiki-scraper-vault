import scraperwiki
import urllib, urllib2
from bs4 import *
import csv
import json
import contextlib

url = "https://www.dmr.nd.gov/oilgas/findwellsvw.asp"
userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:18.0) Gecko/20100101 Firefox/18.0"
contentType = "application/x-www-form-urlencoded"
for y in range(1,37):
    data = urllib.urlencode({'VTI-GROUP':'0', 'ddmOperator':'', 'ddmField':'', 'ddmSection': y, 'ddmTownship':'0', 'ddmRange':'0', 'B1':'Submit'})
    req = urllib2.Request(url=url,data=data)
    req.add_header('ASPSESSIONIDQUTQDRRD','KNFIBKMCOLPFPBBHFENOAAEF')
    with contextlib.closing(urllib2.urlopen(req)) as x:
        html = x.read()
    soup = BeautifulSoup(html)
    table = soup.find('table',attrs={'summary':'Well Log search results table'})
    for row in table.findAll('tr')[1:-1]:
        record = {}
        columns = row.find_all('td')
        record["file_no"] = columns[0].get_text()
        record["ctb_no"] = columns[1].get_text()
        record["api_no"] = columns[2].get_text()
        record["well_type"] = columns[3].get_text()
        record["well_status"] = columns[4].get_text()
        record["status_date"] = columns[5].get_text()
        record["dtd"] = columns[6].get_text()
        record["location"] = columns[7].get_text()
        record["operator"] = columns[8].get_text()
        record["well_name"] = columns[9].get_text()
        record["field"] = columns[10].get_text()
        print record
        scraperwiki.sqlite.save(unique_keys=['api_no'], data=record)
    scraperwiki.sqlite.commit()


import scraperwiki
import urllib, urllib2
from bs4 import *
import csv
import json
import contextlib

url = "https://www.dmr.nd.gov/oilgas/findwellsvw.asp"
userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:18.0) Gecko/20100101 Firefox/18.0"
contentType = "application/x-www-form-urlencoded"
for y in range(1,37):
    data = urllib.urlencode({'VTI-GROUP':'0', 'ddmOperator':'', 'ddmField':'', 'ddmSection': y, 'ddmTownship':'0', 'ddmRange':'0', 'B1':'Submit'})
    req = urllib2.Request(url=url,data=data)
    req.add_header('ASPSESSIONIDQUTQDRRD','KNFIBKMCOLPFPBBHFENOAAEF')
    with contextlib.closing(urllib2.urlopen(req)) as x:
        html = x.read()
    soup = BeautifulSoup(html)
    table = soup.find('table',attrs={'summary':'Well Log search results table'})
    for row in table.findAll('tr')[1:-1]:
        record = {}
        columns = row.find_all('td')
        record["file_no"] = columns[0].get_text()
        record["ctb_no"] = columns[1].get_text()
        record["api_no"] = columns[2].get_text()
        record["well_type"] = columns[3].get_text()
        record["well_status"] = columns[4].get_text()
        record["status_date"] = columns[5].get_text()
        record["dtd"] = columns[6].get_text()
        record["location"] = columns[7].get_text()
        record["operator"] = columns[8].get_text()
        record["well_name"] = columns[9].get_text()
        record["field"] = columns[10].get_text()
        print record
        scraperwiki.sqlite.save(unique_keys=['api_no'], data=record)
    scraperwiki.sqlite.commit()


