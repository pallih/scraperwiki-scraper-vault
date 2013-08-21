import scraperwiki
import simplejson
import tarfile
import time
import StringIO
import os,cgi,glob
import mechanize
from BeautifulSoup import BeautifulSoup
import sys

verbose = True

import logging
#log = logging.getLogger("DropBoxClass")
logger = logging.getLogger("mechanize")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

import mechanize
from getpass import getpass
import sys
from os import environ
import cookielib
from urllib2 import HTTPError

class UploadError(Exception): pass

def upload_files(local_files, remote_dir, email, password):
    """ Upload a local file to Dropbox """

    # Fire up a browser using mechanize
    br = mechanize.Browser()

    br.set_handle_equiv(True)
#    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
#    br.set_handle_robots(False)

#    br.set_debug_http(True)
#    br.set_debug_responses(True)
#    br.set_debug_redirects(True)

    br.addheaders = [('User-agent', ' Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1018.0 Safari/535.19')]

    if verbose: print 'Opening login page...'
    # Browse to the login page
    r = br.open('https://www.dropbox.com/login')
    # just in case you need the html
    # html = r.read()
    # this shows a lot of info

    print r.info()

    if verbose: print br.title(), br.geturl()

    # Enter the username and password into the login form
    isLoginForm = lambda l: l.action == "https://www.dropbox.com/login" and l.method == "POST"

    try:
        if verbose: print 'selecting form...'
        br.select_form(predicate=isLoginForm)
    except:
        print("Unable to find login form.");
        exit(1);

    br['login_email'] = email
    br['login_password'] = password

    # Send the form
    if verbose: print 'submitting login form...'
    response = br.submit()

    # Add our file upload to the upload form once logged in
    isUploadForm = lambda u: u.action == "https://dl-web.dropbox.com/upload" and u.method == "POST"

    for local_file in local_files:
        try:
            br.select_form(predicate=isUploadForm)
        except:
            print("Unable to find upload form.");
            print("Make sure that your login information is correct.");
            exit(1);
            
        br.form.find_control("dest").readonly = False
        br.form.set_value(remote_dir, "dest")

        remote_file = os.path.basename(local_file)
        #if (os.path.isfile(local_file)):
        br.form.add_file(open(local_files, "rb"))
            # Submit the form with the file
        if verbose: print 'Uploading %s... to <<Dropbox>>:/%s/%s' % (local_files, remote_dir, remote_file),
        br.submit()
        
        if verbose: print 'Ok'
                
    print 'All completed Ok!'

qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

user = str(qsenv['user'])
email = str(qsenv['email'])
password = str(qsenv['password'])
mtime = time.time()
filename = str(qsenv['user']+'-scrapers.tar')
tarfilename= str('/tmp/'+qsenv['user']+'-scrapers.tar')

#upload_file(email,password,tarfilename,'/')
#exit()


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
print 'Tar file created'
print 'Uploading to dropbox.com'
upload_files(tarfilename,'Geymsla',email,password,)

#scraperwiki.utils.httpresponseheader("Content-Type", "application/tar-x")
#scraperwiki.utils.httpresponseheader("Content-Disposition", "attachment; filename="+sendtarfilename)

#f = open(tarfilename,"r")
#data = f.read()
#print data
#f.close

