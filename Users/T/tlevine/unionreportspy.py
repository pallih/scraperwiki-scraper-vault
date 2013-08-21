import scraperwiki
import urllib
import lxml.html
import datetime
import re
from time import sleep

COLNAMES = [
  'Employer Name', 'Format', 'Location', 'Union', 'Local',
  'NAICS', 'NumberWrkrs', 'Expiration Date', 'Number Pages', 'OLMS File Number'
]

STATES = [
  'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
  'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
  'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
  'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
  'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

def OnePage(url):
    try:
        f = urllib.urlopen(url)
    except:
        sleep(123)
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
    elif re.match('NumberWorkers', headers[6]):
        headers[6] = 'NumberWrkrs'
    elif re.match('Expiration\s*Date', headers[7]):
        headers[7] = 'Expiration Date'
    elif re.match('Number\s*Pages', headers[8]):
        headers[8] = 'Number Pages'

    #assert headers == ['Employer Name', 'Format', 'Location', 'Union', 'Local', 'NAICS', 'NumberWrkrs', 'Expiration Date', 'Number Pages', 'OLMS File Number'], headers
    
    ldata = [ ]
    for row in rows[1:]:
        d = [ z.text_content().strip()  for z in list(row) ]
        data = dict(zip(COLNAMES, d))

        try:
            data['NumberWrkrs'] = int(data['NumberWrkrs'])
        except:
            data['NumberWrkrs'] = None

        try:
            data['Expiration Date'] = datetime.datetime.strptime(data["Expiration Date"],"%m-%d-%y").date()
        except:
            data['Expiration Date'] = None

        data['state'] = data['Location'][:2]
        if data['Location'] == "National":
            data['state'] = ''
        elif data['state'] not in STATES:
            data["Location"] = 'unknown'
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
        sleep(4)
        
    #print lxml.html.tostring(a)

