import scraperwiki
import BeautifulSoup
from datetime import date 
import re
from mechanize import Browser

def convert_date (t):
    if t == '-':
        return None
    parts = t.split ('/')
    return date (int (parts[2]), int (parts[1]), int(parts[0]))

def tickers ():
    scraperwiki.sqlite.attach('lse-ftse-350-constituents', 'constituents')
    results = [r['Epic'].encode("utf8","ignore") for r in scraperwiki.sqlite.select("* from constituents.swdata")]
    results.sort()
    return results


edd_url = 'http://www.exdividenddate.co.uk/'

edd_pat = "javascript:__doPostBack\('(.*?)','(.*?)'\)"

def process_ex_dividend_data (html):
    soup = BeautifulSoup.BeautifulSoup(html)
    t = soup.find ("table", {"class":"exdividendtable"})
    alldata = []
    for row in t.findAll ('tr'):
        tds = [td.text.encode("utf8","ignore") for td in row.findAll ('td')]
        if len(tds) == 0:
            continue
            
        data = \
            {
            'Source':'ExDividendData',
            'Ticker':tds[0],
            'Type' : '',
            'Currency': '',
            'DeclarationDate': None,
            'ExDivDate':convert_date (tds[2]),
            'RecordDate':None,
            'PayDate':None,
            'Amount':float(tds[3]),
            'Url':edd_url
            }
        alldata.append (data)
    scraperwiki.sqlite.save (unique_keys=["Source", "Ticker", "ExDivDate", "Type"], data=alldata)


def get_data ():

    html = scraperwiki.scrape (edd_url)
    process_ex_dividend_data  (html)
    
    br = Browser()
    br.set_handle_robots (False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.open (edd_url)    
    
    links = {}
    for link in br.links():
        if link.text in ['2', '3', '4']:
            links [link.text] = link.url
    for k, link in links.items():
        m = re.search (edd_pat, link)

        br = Browser()
        br.set_handle_robots (False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        br.open (edd_url)    
        br.select_form(nr=0)
        br.set_all_readonly(False)
        br["__EVENTTARGET"] = m.group(1)
        br["__EVENTARGUMENT"] = ''
        for c in br.controls:
            if c.type == 'submit':
                c.disabled = True
        response = br.submit()
        process_ex_dividend_data (response.read())

get_data ()
import scraperwiki
import BeautifulSoup
from datetime import date 
import re
from mechanize import Browser

def convert_date (t):
    if t == '-':
        return None
    parts = t.split ('/')
    return date (int (parts[2]), int (parts[1]), int(parts[0]))

def tickers ():
    scraperwiki.sqlite.attach('lse-ftse-350-constituents', 'constituents')
    results = [r['Epic'].encode("utf8","ignore") for r in scraperwiki.sqlite.select("* from constituents.swdata")]
    results.sort()
    return results


edd_url = 'http://www.exdividenddate.co.uk/'

edd_pat = "javascript:__doPostBack\('(.*?)','(.*?)'\)"

def process_ex_dividend_data (html):
    soup = BeautifulSoup.BeautifulSoup(html)
    t = soup.find ("table", {"class":"exdividendtable"})
    alldata = []
    for row in t.findAll ('tr'):
        tds = [td.text.encode("utf8","ignore") for td in row.findAll ('td')]
        if len(tds) == 0:
            continue
            
        data = \
            {
            'Source':'ExDividendData',
            'Ticker':tds[0],
            'Type' : '',
            'Currency': '',
            'DeclarationDate': None,
            'ExDivDate':convert_date (tds[2]),
            'RecordDate':None,
            'PayDate':None,
            'Amount':float(tds[3]),
            'Url':edd_url
            }
        alldata.append (data)
    scraperwiki.sqlite.save (unique_keys=["Source", "Ticker", "ExDivDate", "Type"], data=alldata)


def get_data ():

    html = scraperwiki.scrape (edd_url)
    process_ex_dividend_data  (html)
    
    br = Browser()
    br.set_handle_robots (False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.open (edd_url)    
    
    links = {}
    for link in br.links():
        if link.text in ['2', '3', '4']:
            links [link.text] = link.url
    for k, link in links.items():
        m = re.search (edd_pat, link)

        br = Browser()
        br.set_handle_robots (False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        br.open (edd_url)    
        br.select_form(nr=0)
        br.set_all_readonly(False)
        br["__EVENTTARGET"] = m.group(1)
        br["__EVENTARGUMENT"] = ''
        for c in br.controls:
            if c.type == 'submit':
                c.disabled = True
        response = br.submit()
        process_ex_dividend_data (response.read())

get_data ()
