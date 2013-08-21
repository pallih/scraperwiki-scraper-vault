import simplejson
import string
import scraperwiki
import tarfile
import time
import StringIO
import os,cgi
from datetime import datetime

date = 'Date: '+datetime.now().strftime('%d-%m-%Y') + '\n'
spacestring = '    '

qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

if not qsenv:
    print 'Please add a username to the url in this format:<br>'
    print 'user=USERNAME<br>'
    print 'Example: https://views.scraperwiki.com/run/retrieve-scrapers-markdown-calepin_1/?user=pallih'
    print '<br>'
    print 'You will be given a .tar file with all the scrapers belonging to given user. The files will be ready for import into <a href="http://calepin.co">calepin.co</a>'
    print '<br>'
    print 'If you want plain text files of the scrapers go <a href="https://scraperwiki.com/views/retrieve-scrapers/">here</a>'
    exit()

mtime = time.time()
tarfilename= '/tmp/'+qsenv['user']+'-scrapers-md.tar'
sendtarfilename = qsenv['user']+'-scrapers-md.tar'
tar = tarfile.open(tarfilename, 'w') #write with no compression - for some reason compressed archives turn up damaged

json_url = 'https://api.scraperwiki.com/api/1.0/scraper/getuserinfo?format=jsondict&username=' + qsenv['user']
json = simplejson.loads(scraperwiki.scrape(json_url))
for d in json:
    for scraper_name in d['coderoles']['owner']:
        scraper = 'https://api.scraperwiki.com/api/1.0/scraper/getinfo?format=jsondict&name='+scraper_name+'&version=-1&quietfields=runevents%7Cdatasummary%7Cuserroles%7Chistory'
        scraper_json = simplejson.loads(scraperwiki.scrape(scraper))
        for scrapers in scraper_json:
            code = scrapers['code'].encode('utf-8')
            language = scrapers['language']
            title = 'Title: '+ scraper_name
            if language == 'python':
                ending = '.py.md'
                codestring = '    ::::python\n'
            elif language == 'php':
                ending = '.php.md'
                codestring = '    ::::php\n'
            elif language == 'ruby':
                ending = '.rb.md'
                codestring = '    ::::ruby\n'
            elif language == 'html':
                ending = '.html.md'
                codestring = '    ::::html\n'
            else:
                ending = '.txt'
            #add the language info and spaces for markdown
            codesplit = string.split(code, '\n')
            newcode = []
            for line in codesplit:
                line = spacestring + line
                newcode.append(line)
            newcode.insert(0, codestring) #insert codestring
            newcode.insert(0,'Category:scrapers\n')
            newcode.insert(0, date)
            newcode.insert(0, title) 
            newlist = ''
            for n in newcode:
                newlist = newlist + n + '\n'
            code = newlist
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



    
    
