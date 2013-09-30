import scraperwiki
from BeautifulSoup import BeautifulSoup
from re import sub
from urllib2 import Request, urlopen
# Blank Python
dept = 1
stop = False
while not stop:
    url = "http://www.galichon.com/codesgeo/insee.php?dept=%02d&dep=1" % dept
    response = urlopen(url)
    data = BeautifulSoup(response.read())
    table = data.find('table',{'valign':'top'})
    trs = table.findAll('tr')
    record = {}
    for tr in trs:
        tds = tr.findAll('td')
        if len(tds) == 3:
            if tds[0].getText() == "Commune":
                continue
            else:
                record['City'] = tds[0].getText()
                record['Zip Code'] = tds[1].getText()
                insee_code = tds[2].getText()
                record['INSEE Code'] = sub(' &nbsp;', '', insee_code)
    #            print "--%s--" % record['City']
                scraperwiki.sqlite.save(["INSEE Code"], record)
    dept = dept + 1
    if dept == 95:
        stop = True
import scraperwiki
from BeautifulSoup import BeautifulSoup
from re import sub
from urllib2 import Request, urlopen
# Blank Python
dept = 1
stop = False
while not stop:
    url = "http://www.galichon.com/codesgeo/insee.php?dept=%02d&dep=1" % dept
    response = urlopen(url)
    data = BeautifulSoup(response.read())
    table = data.find('table',{'valign':'top'})
    trs = table.findAll('tr')
    record = {}
    for tr in trs:
        tds = tr.findAll('td')
        if len(tds) == 3:
            if tds[0].getText() == "Commune":
                continue
            else:
                record['City'] = tds[0].getText()
                record['Zip Code'] = tds[1].getText()
                insee_code = tds[2].getText()
                record['INSEE Code'] = sub(' &nbsp;', '', insee_code)
    #            print "--%s--" % record['City']
                scraperwiki.sqlite.save(["INSEE Code"], record)
    dept = dept + 1
    if dept == 95:
        stop = True
