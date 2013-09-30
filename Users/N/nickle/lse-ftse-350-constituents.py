import scraperwiki
import BeautifulSoup

index_url    = 'http://www.lse.co.uk/index-constituents.asp?index=idx:nmx&indexname=' 
interim_url = 'http://www.lse.co.uk/SharePrice.asp?shareprice='
fundamentals_url = 'http://www.lse.co.uk/share-fundamentals.asp?shareprice=%s&share=%s'

import scraperwiki
from datetime import date 
import re

interim_pat = re.compile ('"share-fundamentals.asp\?shareprice=(.*?)&amp;share=(.*?)"')

    
def get_epics ():
    epics = {}
    try:
        for data in scraperwiki.sqlite.select("* from swdata"):
            epics[data['Epic']] = data
    except:
        pass
    return epics

def get_ncodes ():
    ncodes = {}
    try:
        for data in scraperwiki.sqlite.select("* from swdata"):
            if data ['Ncode'] != '':
                ncodes [data['Ncode']] = data
    except:
        pass
    return ncodes

def get_northcote_epic (url):
    html = scraperwiki.scrape (url)
    soup = BeautifulSoup.BeautifulSoup(html)
    ref = soup('form')[1]['action'] 
    parts = ref.split('&')
    ncode = parts[1].split('=')[1].encode("utf8","ignore")
    epic  = parts[2].split('=')[1].encode("utf8","ignore")
    return ncode, epic

def search_northcode (epic):
    url = "http://www.northcote.co.uk/company_links/search.asp?SCN=&SEC=%s&SAS=&SPC=&normal=Go" % epic
    html = scraperwiki.scrape (url)
    soup = BeautifulSoup.BeautifulSoup(html)
    hrefs = []
    for link in soup.findAll ('a'):
        if link.get('class') == "companylink":
            href = link.get("href")
            ncode, repic = get_northcote_epic ("http://www.northcote.co.uk" + href.replace (" ", "%20"))
            if repic == epic:
                return ncode
    return ''

def get_last_open_bracket (t):
    pos = -1
    for i,c in enumerate(t):
        if c == '(': 
            pos = i
    return pos

def get_name (t):
    res = t[0:get_last_open_bracket (t)]
    res = res.strip()
    res = res.replace ("&amp;", "&")
    return res

def get_ticker (t):
    return t[get_last_open_bracket (t)+1:-1]

def get_interim (ticker, name):
    print ticker, name
    try:
        url = interim_url + ticker
        html = scraperwiki.scrape (url)
        res = interim_pat .search (html)
        ticker2 = res.group(1)
        id    = res.group(2)
        url = fundamentals_url % (ticker, id)
        html = scraperwiki.scrape (url)
        soup = BeautifulSoup.BeautifulSoup(html)
        data = {}
        data['Ticker'] = ticker
        data ['Epic'] = ticker
        data ['Name'] = name
        data ['Source'] = 'LSE'  
        data ['Ncode'] = ''  
        try:
            t =soup.findAll("table")[2]
            for row in t.findAll ('tr'):
                label = row.find ("th").text
                value = row.find ("td").text
                if label == 'ISIN':
                    data [label] = value
                if label == 'TIDM':
                    data [label] = value
                if label == 'Currency':
                    if value == 'GBX':
                        value = 'GBP'
                    data [label] = value
        except:
            data['ISIN'] = ''
            data['TIDM'] = ''
            data['Currency'] = 'GBP'
        return data
    except:
        print "Failed to save ", ticker
    return None

def get_lse_index(index):
    epics = get_epics()
    ncodes = get_ncodes ()
    
    url = index_url + index
    html = scraperwiki.scrape (url)
    
    soup = BeautifulSoup.BeautifulSoup(html)
    
    t =soup.findAll("table")[0]
    first = True
    for row in t.findAll ('tr'):
        tds = [td.text.encode("utf8","ignore") for td in row.findAll ('td')]
        if first:
            first = False
        else:
            epic = get_ticker (tds[0])
            name = get_name   (tds[0])
            if epic in epics:
                data = epics[epic]
            else:
                data = get_interim (epic, name)
            try:
                if data['Ncode'] in [None, '']:
                    data['Ncode'] = search_northcode (epic)
            except:
                data['Ncode'] = search_northcode (epic)
            scraperwiki.sqlite.save (unique_keys=["Ticker"], data=data)

    
get_lse_index ('ftse_350')

# href for data http://www.northcote.co.uk/company_links/by_Index.asp?SDL=NI02375

#print search_northcode ('III') import scraperwiki
import BeautifulSoup

index_url    = 'http://www.lse.co.uk/index-constituents.asp?index=idx:nmx&indexname=' 
interim_url = 'http://www.lse.co.uk/SharePrice.asp?shareprice='
fundamentals_url = 'http://www.lse.co.uk/share-fundamentals.asp?shareprice=%s&share=%s'

import scraperwiki
from datetime import date 
import re

interim_pat = re.compile ('"share-fundamentals.asp\?shareprice=(.*?)&amp;share=(.*?)"')

    
def get_epics ():
    epics = {}
    try:
        for data in scraperwiki.sqlite.select("* from swdata"):
            epics[data['Epic']] = data
    except:
        pass
    return epics

def get_ncodes ():
    ncodes = {}
    try:
        for data in scraperwiki.sqlite.select("* from swdata"):
            if data ['Ncode'] != '':
                ncodes [data['Ncode']] = data
    except:
        pass
    return ncodes

def get_northcote_epic (url):
    html = scraperwiki.scrape (url)
    soup = BeautifulSoup.BeautifulSoup(html)
    ref = soup('form')[1]['action'] 
    parts = ref.split('&')
    ncode = parts[1].split('=')[1].encode("utf8","ignore")
    epic  = parts[2].split('=')[1].encode("utf8","ignore")
    return ncode, epic

def search_northcode (epic):
    url = "http://www.northcote.co.uk/company_links/search.asp?SCN=&SEC=%s&SAS=&SPC=&normal=Go" % epic
    html = scraperwiki.scrape (url)
    soup = BeautifulSoup.BeautifulSoup(html)
    hrefs = []
    for link in soup.findAll ('a'):
        if link.get('class') == "companylink":
            href = link.get("href")
            ncode, repic = get_northcote_epic ("http://www.northcote.co.uk" + href.replace (" ", "%20"))
            if repic == epic:
                return ncode
    return ''

def get_last_open_bracket (t):
    pos = -1
    for i,c in enumerate(t):
        if c == '(': 
            pos = i
    return pos

def get_name (t):
    res = t[0:get_last_open_bracket (t)]
    res = res.strip()
    res = res.replace ("&amp;", "&")
    return res

def get_ticker (t):
    return t[get_last_open_bracket (t)+1:-1]

def get_interim (ticker, name):
    print ticker, name
    try:
        url = interim_url + ticker
        html = scraperwiki.scrape (url)
        res = interim_pat .search (html)
        ticker2 = res.group(1)
        id    = res.group(2)
        url = fundamentals_url % (ticker, id)
        html = scraperwiki.scrape (url)
        soup = BeautifulSoup.BeautifulSoup(html)
        data = {}
        data['Ticker'] = ticker
        data ['Epic'] = ticker
        data ['Name'] = name
        data ['Source'] = 'LSE'  
        data ['Ncode'] = ''  
        try:
            t =soup.findAll("table")[2]
            for row in t.findAll ('tr'):
                label = row.find ("th").text
                value = row.find ("td").text
                if label == 'ISIN':
                    data [label] = value
                if label == 'TIDM':
                    data [label] = value
                if label == 'Currency':
                    if value == 'GBX':
                        value = 'GBP'
                    data [label] = value
        except:
            data['ISIN'] = ''
            data['TIDM'] = ''
            data['Currency'] = 'GBP'
        return data
    except:
        print "Failed to save ", ticker
    return None

def get_lse_index(index):
    epics = get_epics()
    ncodes = get_ncodes ()
    
    url = index_url + index
    html = scraperwiki.scrape (url)
    
    soup = BeautifulSoup.BeautifulSoup(html)
    
    t =soup.findAll("table")[0]
    first = True
    for row in t.findAll ('tr'):
        tds = [td.text.encode("utf8","ignore") for td in row.findAll ('td')]
        if first:
            first = False
        else:
            epic = get_ticker (tds[0])
            name = get_name   (tds[0])
            if epic in epics:
                data = epics[epic]
            else:
                data = get_interim (epic, name)
            try:
                if data['Ncode'] in [None, '']:
                    data['Ncode'] = search_northcode (epic)
            except:
                data['Ncode'] = search_northcode (epic)
            scraperwiki.sqlite.save (unique_keys=["Ticker"], data=data)

    
get_lse_index ('ftse_350')

# href for data http://www.northcote.co.uk/company_links/by_Index.asp?SDL=NI02375

#print search_northcode ('III') 