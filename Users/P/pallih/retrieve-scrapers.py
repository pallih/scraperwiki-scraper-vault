import scraperwiki
import simplejson
import tarfile
import time
import StringIO
import os,cgi
import random
import string

chars = string.letters + string.digits
randomstring =  ''.join([random.choice(chars) for i in xrange(4)]) # create a random string for url appending to avoid cache

qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

if not qsenv:
    print 'Please add a username to the url in this format:<br>'
    print 'user=USERNAME<br>'
    print 'Example: https://views.scraperwiki.com/run/retrieve-scrapers/?user=pallih'
    
    exit()

mtime = time.time()
tarfilename= '/tmp/'+qsenv['user']+'_'+randomstring+'-scrapers.tar'
sendtarfilename = qsenv['user']+'-scrapers.tar'
tar = tarfile.open(tarfilename, 'w') #write with no compression - for some reason compressed archives turn up damaged

json_url = 'https://api.scraperwiki.com/api/1.0/scraper/getuserinfo?format=jsondict&username=' + qsenv['user']
json = simplejson.loads(scraperwiki.scrape(json_url))
scrapers = []
for d in json:
    for scraper_name in d['coderoles']['owner']:
        scrapers.append(scraper_name)

for scraper_name in scrapers[60:]:
    
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

