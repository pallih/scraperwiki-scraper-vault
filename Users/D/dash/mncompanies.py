# -*- coding: utf-8 -*-
"""
Proof-of-concept for a montenegro scraper
"""
import scraperwiki
import urllib
import urllib2
import datetime
from bs4 import BeautifulSoup
import traceback

simple_keys = {'Registarski broj : ': 'Registration Number',
'Matični broj : ': 'Establishment number',
'Broj promjene    : ': 'Number of changes',
'Puni naziv : ' : 'Full Name',
'Šifra djelatnosti : ': 'Code of Activity',
'Naziv djelatnosti : ': 'Name of Activity',
'Adresa sjedišta : ': 'Address of Headquarters',
'Mjesto sjedišta : ': 'Town of Headquarters',
'Datum registracije : ': 'Date Registered',
'Datum promjene : ': 'Date Changed',
'Datum brisanja : ': 'Date Dissolved',
'Status : ': 'Status',
}

person_keys = {
'Ime : ': 'First Name',
'Prezime : ': 'Last Name',
'Broj pasoša :': 'Passport Number',
}

UNKNOWN = 'UNKNOWN' # what do you say when you can't find anything?

def detail_from_soup(soup, label):
    match = soup.find(text = label)
    if match:
        return match.findNext(text = True) or UNKNOWN
    return UNKNOWN

def extract_details(soup):
    results = {}
    #soup = BeautifulSoup(html)
    for (label, english) in simple_keys.items():
        results[english] = detail_from_soup(soup, label)
    return results

def extract_person(table55):
    details = {}
    details['ime'] =  table55.findAll('td')[-1].text
    details['title'] = table55.findPrevious('b').text
    details['prezime'] = table55.findNext('table').findAll('td')[-1].text
    return details

def extract_people(soup):
    people = []
    faces = soup.findAll('table', {'id': 'table55'})
    for face in faces:
        people.append(extract_person(face))
    return people

def info_from_record(html, system_record_id):
    results = {
     'system_record_id': system_record_id,
     'date_scraped': datetime.datetime.now().date(),
    }
    soup = BeautifulSoup(html)
    results['people'] = extract_people(soup)
    results.update(extract_details(soup))
    return results

def download_by_id(recordid = "177585"):
    # <input id="prikazidrustvo_0" class="bezslike" type="submit" style="cursor: pointer" value="Prikaži podatke">
    # input id="prikazidrustvo_idDosijea" type="hidden" value="177585" name="idDosijea"# 
    url = 'http://www.crps.me/CRPSPublic/prikazidrustvo.action'
    data = {'prikazidrustvo_0': 'Prikaži podatke',
            'prikazidrustvo_idDosijea': '177585',
            }
    data = {'idDosijea': recordid}
    localfile = open('/tmp/mnsample.html', 'w')
    req = urllib2.Request(url, urllib.urlencode(data))
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page

def sample_record(recordid = "177585"):
    the_page = download_by_id(recordid)
    info = info_from_record(the_page, recordid)
    save_to_sqlite(info)
    return(info)

def record_by_url(url):
    the_page = urllib2.urlopen(url).read()
    recordid = url.split('=')[-1]
    info = info_from_record(the_page, recordid)
    info['url'] = url
    save_to_sqlite(info)
    return(info)

def save_to_sqlite(info):
    #unique_keys = (info['system_record_id'], info['date_scraped'])
    scraperwiki.sqlite.save(unique_keys=['system_record_id', 'date_scraped'], data=info)

def trial():
    scraperwiki.sqlite.attach("me_cmp_list")           
    print scraperwiki.sqlite.select("link from me_cmp_list.swdata limit 2")
    #print(sample_record())

def scrape_sequential():
    count = 10
    offset = scraperwiki.sqlite.get_var('offset', 0)                     
    for link in scraperwiki.sqlite.select("link from me_cmp_list.swdata limit ? offset ?", (count, offset)):
        record_by_url(link['link'])
    scraperwiki.sqlite.save_var('offset', offset + count)


#trial()  
scraperwiki.sqlite.attach("me_cmp_list")
for i in range(10):
    try:    
        scrape_sequential()
    except Exception:
        traceback.print_exc()
        print('aborting')