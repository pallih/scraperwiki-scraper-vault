import scraperwiki
import urllib
import lxml.html
import datetime
import re

def OnePage(url):
    f = urllib.urlopen(url)
    x = f.read()
    r = lxml.html.fromstring(x)
    tables = r.cssselect("table")
    datatable = tables[2]
    rows = datatable.cssselect("tr")
    zlist = rows[0].cssselect("th")
    headers = [ z.text_content().strip().replace("#", "Number").replace("*", "")  for z in zlist ]
    if re.match('Employer\s*Name', headers[0]):
        headers[0] = 'Employer Name'
    if re.match('NumberWorkers', headers[6]):
        headers[6] = 'NumberWrkrs'
    if re.match('Expiration\s*Date', headers[7]):
        headers[7] = 'Expiration Date'
    if re.match('Number\s*Pages', headers[8]):
        headers[8] = 'Number Pages'
    assert headers == ['Employer Name', 'Format', 'Location', 'Union', 'Local', 'NAICS', 'NumberWrkrs', 'Expiration Date', 'Number Pages', 'OLMS File Number'], headers

    states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    
    ldata = [ ]
    for row in rows[1:]:
        d = [ z.text_content().strip()  for z in list(row) ]
        data = dict(zip(headers, d))
        #print data
        try:
            data['NumberWrkrs'] = int(data['NumberWrkrs'])
            dt = data['Expiration Date'].split('-')
            data['Expiration Date'] = datetime.date(int(dt[2])+2000, int(dt[0]), int(dt[1]))
        except (ValueError, IndexError):
            print "Bad", data
        data['state'] = data['Location'][:2]
        if data['Location'] == "National":
            data['state'] = ''
        elif data['state'] not in states:
            print data["Location"]
        else:
            ldata.append(data)
    scraperwiki.sqlite.save(["OLMS File Number"], ldata)
    


url = "http://www.dol.gov/olms/regs/compliance/cba/"
fin = urllib.urlopen(url)
r = lxml.html.fromstring(fin.read())
for a in r.cssselect("div#content a"):
    ah = a.attrib.get("href")
    if ah != None and ah[-3:] == "htm":
        print ah
        OnePage("http://www.dol.gov/olms/regs/compliance/cba/"+ah)
        
    #print lxml.html.tostring(a)

import scraperwiki
import urllib
import lxml.html
import datetime
import re

def OnePage(url):
    f = urllib.urlopen(url)
    x = f.read()
    r = lxml.html.fromstring(x)
    tables = r.cssselect("table")
    datatable = tables[2]
    rows = datatable.cssselect("tr")
    zlist = rows[0].cssselect("th")
    headers = [ z.text_content().strip().replace("#", "Number").replace("*", "")  for z in zlist ]
    if re.match('Employer\s*Name', headers[0]):
        headers[0] = 'Employer Name'
    if re.match('NumberWorkers', headers[6]):
        headers[6] = 'NumberWrkrs'
    if re.match('Expiration\s*Date', headers[7]):
        headers[7] = 'Expiration Date'
    if re.match('Number\s*Pages', headers[8]):
        headers[8] = 'Number Pages'
    assert headers == ['Employer Name', 'Format', 'Location', 'Union', 'Local', 'NAICS', 'NumberWrkrs', 'Expiration Date', 'Number Pages', 'OLMS File Number'], headers

    states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    
    ldata = [ ]
    for row in rows[1:]:
        d = [ z.text_content().strip()  for z in list(row) ]
        data = dict(zip(headers, d))
        #print data
        try:
            data['NumberWrkrs'] = int(data['NumberWrkrs'])
            dt = data['Expiration Date'].split('-')
            data['Expiration Date'] = datetime.date(int(dt[2])+2000, int(dt[0]), int(dt[1]))
        except (ValueError, IndexError):
            print "Bad", data
        data['state'] = data['Location'][:2]
        if data['Location'] == "National":
            data['state'] = ''
        elif data['state'] not in states:
            print data["Location"]
        else:
            ldata.append(data)
    scraperwiki.sqlite.save(["OLMS File Number"], ldata)
    


url = "http://www.dol.gov/olms/regs/compliance/cba/"
fin = urllib.urlopen(url)
r = lxml.html.fromstring(fin.read())
for a in r.cssselect("div#content a"):
    ah = a.attrib.get("href")
    if ah != None and ah[-3:] == "htm":
        print ah
        OnePage("http://www.dol.gov/olms/regs/compliance/cba/"+ah)
        
    #print lxml.html.tostring(a)

