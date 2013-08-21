######################################################################################
# Scraping the Information Asset Register (also demonstrates scraping ASPX)
# There's a guide to the meaning of each record field at http://www.opsi.gov.uk/iar/index.htm
######################################################################################
import cgi
import htmllib
import scraperwiki
import urllib, urllib2
import urlparse
from BeautifulSoup import BeautifulSoup
from datetime import date

start_url = 'http://www.opsi.gov.uk/iar/search.aspx'
base_url = 'http://search.opsi.gov.uk/'
date = date.today()

# python doesn't have built-in HTML unescaping, so use this
def unescape(s):
    p = htmllib.HTMLParser(None)
    p.save_bgn()
    p.feed(s)
    return p.save_end()
    
# follow links to individual records & save into scraperwiki data store
def get_record_info(soup, department_name):
        record_cells = soup.findAll('dt')
        for record in record_cells: 
            data = {}
            record = record.find('a')
            data['Title'] = unescape(record.contents[0])
            data['URL'] = record['href']
            data['OPSI ID'] = str(cgi.parse_qs(urlparse.urlparse(record['href'])[4])['ID'][0]) # extract internal ID from URL
            data['Department'] = department_name
            record_html = scraperwiki.scrape(record['href'])
            record_soup = BeautifulSoup(record_html)
            iar_div = record_soup.find('div', attrs={'id' : 'iar'})
            iar_titles = iar_div.findAll('dt')
            iar_recordfields = iar_div.findAll('dd')
            for i, title in enumerate(iar_titles): 
                if title.find('acronym'): 
                    title = title.find('acronym')
                data[title.contents[0].replace(':', '')] = iar_recordfields[i].contents[0]
            scraperwiki.datastore.save(["OPSI ID"], data=data, date=date)

# get records from page 1 (which we had to call using an ASPX viewstate request)
# and check for a 'next page' link, then call self recursively
def get_records_and_check_for_next(soup, department_name):
    get_record_info(soup, department_name)
    next_link = soup.find(title="Go to next page")
    if next_link: 
        next_link = base_url + next_link['href']
        next_html = scraperwiki.scrape(next_link)
        next_soup = BeautifulSoup(next_html)
        get_records_and_check_for_next(next_soup, department_name) 

# given a department name, do a search (with fake ASPX POST data)
def get_records_for_department(department_name):
    print ('Getting records for department: ' + department_name)
    headers = {
    'HTTP_USER_AGENT': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3',
    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    formFields = (
        (r'__VIEWSTATE',    r'/wEPDwUKMTAwMzIwNTU2Ng9kFgJmD2QWAgIED2QWAgIBD2QWAgIJDxBkDxYTZgIBAgICAwIEAgUCBgIHAggCCQIKAgsCDAINAg4CDwIQAhECEhYTEAUNLS0tLS1BbnktLS0tLQUBMGcQBRpDZW50cmFsIFNjaWVuY2UgTGFib3JhdG9yeQUaQ2VudHJhbCBTY2llbmNlIExhYm9yYXRvcnlnEAUgQ29tbXVuaXRpZXMgYW5kIExvY2FsIEdvdmVybm1lbnQFIENvbW11bml0aWVzIGFuZCBMb2NhbCBHb3Zlcm5tZW50ZxAFD0NvbXBhbmllcyBIb3VzZQUPQ29tcGFuaWVzIEhvdXNlZxAFLURlcGFydG1lbnQgZm9yIENoaWxkcmVuLCBTY2hvb2xzIGFuZCBGYW1pbGllcwUtRGVwYXJ0bWVudCBmb3IgQ2hpbGRyZW4sIFNjaG9vbHMgYW5kIEZhbWlsaWVzZxAFMkRlcGFydG1lbnQgZm9yIEVudmlyb25tZW50LCBGb29kIGFuZCBSdXJhbCBBZmZhaXJzBTJEZXBhcnRtZW50IGZvciBFbnZpcm9ubWVudCwgRm9vZCBhbmQgUnVyYWwgQWZmYWlyc2cQBRREZXBhcnRtZW50IG9mIEhlYWx0aAUURGVwYXJ0bWVudCBvZiBIZWFsdGhnEAUYRHJpdmluZyBTdGFuZGFyZHMgQWdlbmN5BRhEcml2aW5nIFN0YW5kYXJkcyBBZ2VuY3lnEAUVRm9vZCBTdGFuZGFyZHMgQWdlbmN5BRVGb29kIFN0YW5kYXJkcyBBZ2VuY3lnEAUER0NIUQUER0NIUWcQBRlMZWdhbCBTZXJ2aWNlcyBDb21taXNzaW9uBRlMZWdhbCBTZXJ2aWNlcyBDb21taXNzaW9uZxAFE01pbmlzdHJ5IG9mIEp1c3RpY2UFE01pbmlzdHJ5IG9mIEp1c3RpY2VnEAURTmF0aW9uYWwgQXJjaGl2ZXMFEU5hdGlvbmFsIEFyY2hpdmVzZxAFD09yZG5hbmNlIFN1cnZleQUPT3JkbmFuY2UgU3VydmV5ZxAFFVBsYW5uaW5nIEluc3BlY3RvcmF0ZQUVUGxhbm5pbmcgSW5zcGVjdG9yYXRlZxAFFVJlZ2lzdGVycyBvZiBTY290bGFuZAUVUmVnaXN0ZXJzIG9mIFNjb3RsYW5kZxAFRFJveWFsIENvbW1pc3Npb24gb24gdGhlIEFuY2llbnQgYW5kIEhpc3RvcmljYWwgTW9udW1lbnRzIG9mIFNjb3RsYW5kBURSb3lhbCBDb21taXNzaW9uIG9uIHRoZSBBbmNpZW50IGFuZCBIaXN0b3JpY2FsIE1vbnVtZW50cyBvZiBTY290bGFuZGcQBStUcmFpbmluZyBhbmQgRGV2ZWxvcG1lbnQgQWdlbmN5IGZvciBTY2hvb2xzBStUcmFpbmluZyBhbmQgRGV2ZWxvcG1lbnQgQWdlbmN5IGZvciBTY2hvb2xzZxAFF1ZhbHVhdGlvbiBPZmZpY2UgQWdlbmN5BRdWYWx1YXRpb24gT2ZmaWNlIEFnZW5jeWdkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAQUhY3RsMDAkbWFpbkNvbnRlbnRzJGRlcGFydG1lbnRsaXN0O41q3etQuwjbgzlcNkIV2TCjwCk='),
        (r'__EVENTVALIDATION', r'/wEWGQK1/vtGAu60z58OAsbcgP8OAuCY+aIKAtL8zs4EAretoZAPApnfm/QNAu/tif0PAs/XwPYHAtaLneoMApzhs7sKApn0hpQPAsSU3rsOAoaf8XsCjMam7w4Cz9HFgAUC79qQpA0CzuKV8QEC2/TolAwCj/HgtQoC58y/5A8CzcqPsQoC3Z7TvAIC/5uljgMCjMH8bv4ftDRu6liDV4EODT1fqQ20dONs'),
        (r'ctl00$mainContents$as_epq', ''), 
        (r'ctl00$mainContents$as_eq', ''), 
        (r'ctl00$mainContents$as_oq', ''),
        (r'ctl00$mainContents$as_q', ''),
        (r'ctl00$mainContents$departmentlist', department_name),  
        (r'ctl00$mainContents$searchsubmit', 'Search'), 
    )
    encodedFields = urllib.urlencode(formFields)
    req = urllib2.Request(start_url, encodedFields, headers)
    doc = urllib2.urlopen(req)
    soup = BeautifulSoup(doc)
    if soup is not None: 
        get_records_and_check_for_next(soup, department_name)
                                                                     
# first, get the list of departments off the IAR homepage
start_html = scraperwiki.scrape(start_url)
start_soup = BeautifulSoup(start_html)
department_list = start_soup.find(id='ctl00_mainContents_departmentlist').findAll('option')
for i, department in enumerate(department_list): 
    if i == 0:
        continue
    get_records_for_department(department.string)
