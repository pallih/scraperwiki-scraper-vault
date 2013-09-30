import scraperwiki
import simplejson
import tarfile
import time
import StringIO
import os,cgi
from lxml.html import fromstring
from urllib2 import urlopen

html = fromstring(urlopen('https://views.scraperwiki.com/run/mix_scraper_spreadsheets/?date='+str(time.time())).read())
frompage = [href.split('/')[-2] for href in html.xpath('//td[position()=1]/a/@href')]
manual = [
    'geocode_all_mix_scrapers_final_for_south_africa',
    'mix_scraper_spreadsheets',
    'retrieve-mix-scrapers',
    'combine_mix_scraper_spreadsheets',
    'combine_mix_scraper_spreadsheets_1',
]

slugs = set(frompage + manual)

# Much of the following is based on Pall's script
mtime = time.time()
tarfilename= '/tmp/mix-scrapers.tar'
sendtarfilename = 'mix-scrapers.tar'
tar = tarfile.open(tarfilename, 'w') #write with no compression - for some reason compressed archives turn up damaged

for scraper_name in slugs:
    scraper = 'https://api.scraperwiki.com/api/1.0/scraper/getinfo?format=jsondict&name='+scraper_name+'&version=-1&quietfields=runevents%7Cdatasummary%7Cuserroles%7Chistory'
    scraper_json = simplejson.loads(scraperwiki.scrape(scraper))
    for scrapers in scraper_json:
        code = scrapers['code'].encode('utf-8')
        language = scrapers['language']
        if language == 'python':
            ending = '.py'
        elif language == 'php':
            ending = '.php'
        elif language == 'ruby':
            ending = '.rb'
        elif language == 'html':
            ending = '.html'
        else:
            ending = '.txt'
        tarinfo = tarfile.TarInfo(scraper_name+ending)
        tarinfo.size = len(code)
        tarinfo.mtime = mtime
        tar.addfile(tarinfo, StringIO.StringIO(str(code)))
tar.close()

scraperwiki.utils.httpresponseheader("Content-Type", "application/tar-x")
scraperwiki.utils.httpresponseheader("Content-Disposition", "attachment; filename="+sendtarfilename)

f = open(tarfilename,"r")
data = f.read()
print data
f.close

import scraperwiki
import simplejson
import tarfile
import time
import StringIO
import os,cgi
from lxml.html import fromstring
from urllib2 import urlopen

html = fromstring(urlopen('https://views.scraperwiki.com/run/mix_scraper_spreadsheets/?date='+str(time.time())).read())
frompage = [href.split('/')[-2] for href in html.xpath('//td[position()=1]/a/@href')]
manual = [
    'geocode_all_mix_scrapers_final_for_south_africa',
    'mix_scraper_spreadsheets',
    'retrieve-mix-scrapers',
    'combine_mix_scraper_spreadsheets',
    'combine_mix_scraper_spreadsheets_1',
]

slugs = set(frompage + manual)

# Much of the following is based on Pall's script
mtime = time.time()
tarfilename= '/tmp/mix-scrapers.tar'
sendtarfilename = 'mix-scrapers.tar'
tar = tarfile.open(tarfilename, 'w') #write with no compression - for some reason compressed archives turn up damaged

for scraper_name in slugs:
    scraper = 'https://api.scraperwiki.com/api/1.0/scraper/getinfo?format=jsondict&name='+scraper_name+'&version=-1&quietfields=runevents%7Cdatasummary%7Cuserroles%7Chistory'
    scraper_json = simplejson.loads(scraperwiki.scrape(scraper))
    for scrapers in scraper_json:
        code = scrapers['code'].encode('utf-8')
        language = scrapers['language']
        if language == 'python':
            ending = '.py'
        elif language == 'php':
            ending = '.php'
        elif language == 'ruby':
            ending = '.rb'
        elif language == 'html':
            ending = '.html'
        else:
            ending = '.txt'
        tarinfo = tarfile.TarInfo(scraper_name+ending)
        tarinfo.size = len(code)
        tarinfo.mtime = mtime
        tar.addfile(tarinfo, StringIO.StringIO(str(code)))
tar.close()

scraperwiki.utils.httpresponseheader("Content-Type", "application/tar-x")
scraperwiki.utils.httpresponseheader("Content-Disposition", "attachment; filename="+sendtarfilename)

f = open(tarfilename,"r")
data = f.read()
print data
f.close

