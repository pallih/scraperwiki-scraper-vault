import scraperwiki
import urllib2, urllib
import sqlite3
import contextlib
from bs4 import *
import contextlib
import re

scraperwiki.sqlite.execute('DROP TABLE IF EXISTS dist_profiles;')
scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS dist_profiles (`district` VARCHAR, `title` VARCHAR, `pdf_link` VARCHAR PRIMARY KEY);')

baseUrl = "http://www.ecoi.net/index.php?y=0&ExtendedSearchFormTab=adv&ES_before=&js=true&ES_after=&ES_query=%22Region+District+Profiles%22&ES_countrychooser_country=188769%3A%3AAfghanistan%3A%3AAF%3A%3AAF%3A%3A188772%3A%3A311452%3A%3Aafghanistan%3A%3A341753&x=0&StartAt="
endUrl = "&ES_source=10&source=10&ES_sort_by=1&ES_documenttype=&ES_query_hidden=district+AND+profile&ES_origlanguage=&countrychooser_country=188769%3A%3AAfghanistan%3A%3AAF%3A%3AAF%3A%3A188772%3A%3A311452%3A%3Aafghanistan&shortcut=afghanistan&ES_usethesaurus=on"

startIndex = 0
pageNum = 1
while startIndex <= 240:
    url = baseUrl + str(startIndex) + endUrl
    request = urllib2.Request(url)
    opener = urllib2.build_opener()
    request.add_header('User-Agent', 'OpenAnything/1.0 +http://diveintopython.org/')
    x = opener.open(request).read()
    soup = BeautifulSoup(x)
    results = soup.body.find_all('div',attrs={'class':'countrydoc'})[1:-1]
    for ix in range(len(results)):
        result = results[ix]
        record = {}
        pdf_link = result.find('table',attrs={'class':'doxxx'}).tr.td.find('a',attrs={'class': 'pdf_en'})['href']
        pattern = re.compile('file_upload')
        if pattern.search(pdf_link) != None:
            record['pdf_link'] = 'http://www.ecoi.net/' + pdf_link
        
            record['title'] = re.sub('\n','', result.find_all('p', attrs={'class':'black'})[0].get_text())
            record['district'] = re.split('\[',re.sub('UNHCR.*District Profiles: District ','', record['title']))[0]
            try:
                scraperwiki.sqlite.execute("INSERT OR IGNORE into dist_profiles values( ?, ?, ?)",(record["district"], record["title"], record["pdf_link"]))
                scraperwiki.sqlite.commit()
            except:
                print("fail")
    startIndex += 10import scraperwiki
import urllib2, urllib
import sqlite3
import contextlib
from bs4 import *
import contextlib
import re

scraperwiki.sqlite.execute('DROP TABLE IF EXISTS dist_profiles;')
scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS dist_profiles (`district` VARCHAR, `title` VARCHAR, `pdf_link` VARCHAR PRIMARY KEY);')

baseUrl = "http://www.ecoi.net/index.php?y=0&ExtendedSearchFormTab=adv&ES_before=&js=true&ES_after=&ES_query=%22Region+District+Profiles%22&ES_countrychooser_country=188769%3A%3AAfghanistan%3A%3AAF%3A%3AAF%3A%3A188772%3A%3A311452%3A%3Aafghanistan%3A%3A341753&x=0&StartAt="
endUrl = "&ES_source=10&source=10&ES_sort_by=1&ES_documenttype=&ES_query_hidden=district+AND+profile&ES_origlanguage=&countrychooser_country=188769%3A%3AAfghanistan%3A%3AAF%3A%3AAF%3A%3A188772%3A%3A311452%3A%3Aafghanistan&shortcut=afghanistan&ES_usethesaurus=on"

startIndex = 0
pageNum = 1
while startIndex <= 240:
    url = baseUrl + str(startIndex) + endUrl
    request = urllib2.Request(url)
    opener = urllib2.build_opener()
    request.add_header('User-Agent', 'OpenAnything/1.0 +http://diveintopython.org/')
    x = opener.open(request).read()
    soup = BeautifulSoup(x)
    results = soup.body.find_all('div',attrs={'class':'countrydoc'})[1:-1]
    for ix in range(len(results)):
        result = results[ix]
        record = {}
        pdf_link = result.find('table',attrs={'class':'doxxx'}).tr.td.find('a',attrs={'class': 'pdf_en'})['href']
        pattern = re.compile('file_upload')
        if pattern.search(pdf_link) != None:
            record['pdf_link'] = 'http://www.ecoi.net/' + pdf_link
        
            record['title'] = re.sub('\n','', result.find_all('p', attrs={'class':'black'})[0].get_text())
            record['district'] = re.split('\[',re.sub('UNHCR.*District Profiles: District ','', record['title']))[0]
            try:
                scraperwiki.sqlite.execute("INSERT OR IGNORE into dist_profiles values( ?, ?, ?)",(record["district"], record["title"], record["pdf_link"]))
                scraperwiki.sqlite.commit()
            except:
                print("fail")
    startIndex += 10