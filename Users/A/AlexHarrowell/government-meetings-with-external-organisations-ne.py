# Reprocessing the government meetings data into an edge-oriented format for network analysers

import urllib2
import csv
import scraperwiki
import re
from hashlib import md5
import json

ls = None
lobbyregex = re.compile(r'\s*[^\w\s]+\s*')
def datawriter(minister, date, department, name_of_external_organisation, subject, meeting):
     link = {}
     link.update(minister=minister, date=date, department=department, name_of_external_organisation=name_of_external_organisation, subject=subject, meeting=meeting)
     hasher = md5()
     hasher.update(str(link))
     link.update(link_id=(hasher.hexdigest()))
     scraperwiki.datastore.save(unique_keys=['link_id'], data=link)

def process_row(row):
    print row
    minister = row['Minister']
    date = row['Date']
    orgs = row['Name of External Organisation']
    department = row['department']
    subject = row['Purpose of meeting']
    meeting = row['uniqueid']
    if orgs != '':
        names = re.split(lobbyregex,  orgs)
        for org in names:
            datawriter(minister, date, department, org, subject, meeting)

def savedate(d):
    mostrecent = d['date_scraped']
    scraperwiki.sqlite.save_var('lastscrape', mostrecent)

try:
    ls = scraperwiki.sqlite.get_var('lastscrape')
except NameError:
    pass

if ls:
    query_uri = 'http://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=government-meetings-with-external-organisations&query=select%20*%20from%20swdata%20where%20time(date_scraped)%20>%20time(' + ''' + ls + ''' +')' 
    
else:
    query_uri = 'http://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=government-meetings-with-external-organisations&query=select%20*%20from%20swdata'

input = urllib2.urlopen(query_uri)
data = json.load(input, object_hook=process_row)

mr = urllib2.urlopen('http://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=government-meetings-with-external-organisations&query=select%20date_scraped%20from%20swdata%20order%20by%20date_scraped%20desc%20limit%201')
print mr
date = json.load(mr, object_hook=savedate)
# Reprocessing the government meetings data into an edge-oriented format for network analysers

import urllib2
import csv
import scraperwiki
import re
from hashlib import md5
import json

ls = None
lobbyregex = re.compile(r'\s*[^\w\s]+\s*')
def datawriter(minister, date, department, name_of_external_organisation, subject, meeting):
     link = {}
     link.update(minister=minister, date=date, department=department, name_of_external_organisation=name_of_external_organisation, subject=subject, meeting=meeting)
     hasher = md5()
     hasher.update(str(link))
     link.update(link_id=(hasher.hexdigest()))
     scraperwiki.datastore.save(unique_keys=['link_id'], data=link)

def process_row(row):
    print row
    minister = row['Minister']
    date = row['Date']
    orgs = row['Name of External Organisation']
    department = row['department']
    subject = row['Purpose of meeting']
    meeting = row['uniqueid']
    if orgs != '':
        names = re.split(lobbyregex,  orgs)
        for org in names:
            datawriter(minister, date, department, org, subject, meeting)

def savedate(d):
    mostrecent = d['date_scraped']
    scraperwiki.sqlite.save_var('lastscrape', mostrecent)

try:
    ls = scraperwiki.sqlite.get_var('lastscrape')
except NameError:
    pass

if ls:
    query_uri = 'http://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=government-meetings-with-external-organisations&query=select%20*%20from%20swdata%20where%20time(date_scraped)%20>%20time(' + ''' + ls + ''' +')' 
    
else:
    query_uri = 'http://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=government-meetings-with-external-organisations&query=select%20*%20from%20swdata'

input = urllib2.urlopen(query_uri)
data = json.load(input, object_hook=process_row)

mr = urllib2.urlopen('http://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=government-meetings-with-external-organisations&query=select%20date_scraped%20from%20swdata%20order%20by%20date_scraped%20desc%20limit%201')
print mr
date = json.load(mr, object_hook=savedate)
