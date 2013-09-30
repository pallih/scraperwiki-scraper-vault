import scraperwiki
from lxml import html
from urllib2 import urlopen, Request
import re
import string

URL = "http://www.entwicklung.at/foerderungen-und-ausschreibungen/projektliste/?tx_sysfirecdlist_pi1[pointer]=%s"

def cleandata(data):
    if data:
        newdata = string.strip(data)
    else:
        newdata=''
    return newdata

def cleanamount(data):
    newdata = cleandata(data)
    newdata = re.sub('EUR ', '', newdata)
    newdata = re.sub('\.', '', newdata)
    newdata = re.sub(',', '.', newdata)
    return newdata

for page in range(0,16):
    req = Request(URL % (page))
    doc = html.parse(urlopen(req))
    count = 0
    for tr in doc.findall('//tr'):
        cells = list(tr.findall('''td[@class='cdcontent']/div'''))
        if not len(cells):
            continue
        amount = cells[3].text
        print cleanamount(amount)
        data = {
            'number' : cleandata(cells[0].text),
            'title' : cleandata(cells[1].find('a').text),
            'country' : cleandata(cells[2].text),
            'amount' : cleanamount(amount),
            'implementer' : cleandata(cells[4].text)
        }       
        scraperwiki.sqlite.save(unique_keys=["number"],
            data=data)import scraperwiki
from lxml import html
from urllib2 import urlopen, Request
import re
import string

URL = "http://www.entwicklung.at/foerderungen-und-ausschreibungen/projektliste/?tx_sysfirecdlist_pi1[pointer]=%s"

def cleandata(data):
    if data:
        newdata = string.strip(data)
    else:
        newdata=''
    return newdata

def cleanamount(data):
    newdata = cleandata(data)
    newdata = re.sub('EUR ', '', newdata)
    newdata = re.sub('\.', '', newdata)
    newdata = re.sub(',', '.', newdata)
    return newdata

for page in range(0,16):
    req = Request(URL % (page))
    doc = html.parse(urlopen(req))
    count = 0
    for tr in doc.findall('//tr'):
        cells = list(tr.findall('''td[@class='cdcontent']/div'''))
        if not len(cells):
            continue
        amount = cells[3].text
        print cleanamount(amount)
        data = {
            'number' : cleandata(cells[0].text),
            'title' : cleandata(cells[1].find('a').text),
            'country' : cleandata(cells[2].text),
            'amount' : cleanamount(amount),
            'implementer' : cleandata(cells[4].text)
        }       
        scraperwiki.sqlite.save(unique_keys=["number"],
            data=data)