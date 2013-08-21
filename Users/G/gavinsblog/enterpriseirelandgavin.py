import scraperwiki
import BeautifulSoup
import urllib2
import urllib
import cookielib

from scraperwiki import datastore

failed_count = 0


def get_name(str_name):


    urlopen = urllib2.urlopen
    Request = urllib2.Request
    cj = cookielib.LWPCookieJar()

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)


    url = "http://www.enterprise-ireland.com/peoplefinder/clientsearch.aspx"
    reqdata = {}
    reqdata = urllib.urlencode(reqdata)
    req = Request(url, reqdata)
    handle = urlopen(req)


    soup = BeautifulSoup.BeautifulSoup(handle.read())
    viewstate = soup.find('input', {'id' : '__VIEWSTATE'})['value']
    ev = soup.find('input', {'id' : '__EVENTVALIDATION'})['value']
    
    reqdata = {
        'ClientName' : str_name,
        '__EVENTTARGET' : 'btnClientSearch',
        '__VIEWSTATE' : viewstate, 
        '__EVENTVALIDATION' : ev, 
        }
    reqdata = urllib.urlencode(reqdata)
    req = Request(url, reqdata)
    handle = urlopen(req)


    soup = BeautifulSoup.BeautifulSoup(handle.read())
    try:
        name = soup.find('div', {'id' : 'stdartev'}).find(text='Development Adviser:').parent.findNext('dd').string
    except Exception, e:
        name = None
    return name


import csv

url = 'http://www.gavinsblog.com/eisheet.csv'

data=scraperwiki.scrape(url)

new_data = data.splitlines()[1:]


csv_reader=csv.reader(new_data)

for line in csv_reader:
    if len(line) > 3:
        companyname=line[3]
        if not companyname.strip(): continue
    else:
        continue
        
    contact = get_name(companyname)

    if contact:
        data = {'company' : companyname,
            'development_advisor': contact,}
        datastore.save(unique_keys=['company'], data=data)
    else:
        print "SEARCH FAILED WITH: %s" % companyname
        failed_count += 1
print "TOTAL FAILED: %s" % failed_count
