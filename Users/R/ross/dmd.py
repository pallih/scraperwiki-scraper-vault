import scraperwiki
import os, cgi, gc
import mechanize
import re
import cookielib
import urlparse
import urllib
import zipfile
from lxml.html import fromstring
from lxml import etree
from cStringIO import StringIO
import datetime

env = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
username = env['USERNAME']
password = env['PASSWORD']

supplier_re = re.compile('.*\((.*?)\).*')

br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Login
r = br.open('https://www.uktcregistration.nss.cfh.nhs.uk/trud3/user/authenticated/group/0/pack/6/subpack/24/releases')
html = r.read()
br.select_form(nr=1)
br.form['j_username'] = username
br.form['j_password'] = password
br.submit()


page = fromstring(br.response().read())
del br

latest = page.cssselect('.download-release')
url = urlparse.urljoin('https://www.uktcregistration.nss.cfh.nhs.uk', latest[0].get('href'))

# download url to /tmp and unzip it.
urllib.urlretrieve (url, "dmd.zip")
zfile = zipfile.ZipFile("dmd.zip")
for name in zfile.namelist():
    (dirname, filename) = os.path.split(name)
    print "Decompressing " + filename + " on " + dirname
    if dirname and not os.path.exists(dirname):
        os.mkdir(dirname)
    fd = open(name,"w")
    fd.write(zfile.read(name))
    fd.close()
del zfile

source = None
for f in os.listdir("."):
    if f.startswith("f_amp2_"):
        source = f

gc.collect()

now = datetime.datetime.now().isoformat()
print "Loading from ", source

items = []
data = {"_when": now, "_source": source}
for event, elem in etree.iterparse(source):
    if elem.tag == "AMP":
        if 'APID' in data:
            items.append(data.copy())
            data = {"_when": now, "_source": source}        
            if len(items) == 100:
                scraperwiki.sqlite.save(['APID'], items)
                items = []
        else:
            print 'No APID in %s and event was %s' %(data,event)
    if elem.text:
        data[elem.tag] = elem.text
    if elem.tag == "DESC":
        m = supplier_re.match(elem.text)
        if m:
            data['SUPPLIER'] = m.groups()[0]
        else:
            data['SUPPLIER'] = "Unknown"
        

if items:
    scraperwiki.sqlite.save(['APID'], items)import scraperwiki
import os, cgi, gc
import mechanize
import re
import cookielib
import urlparse
import urllib
import zipfile
from lxml.html import fromstring
from lxml import etree
from cStringIO import StringIO
import datetime

env = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
username = env['USERNAME']
password = env['PASSWORD']

supplier_re = re.compile('.*\((.*?)\).*')

br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Login
r = br.open('https://www.uktcregistration.nss.cfh.nhs.uk/trud3/user/authenticated/group/0/pack/6/subpack/24/releases')
html = r.read()
br.select_form(nr=1)
br.form['j_username'] = username
br.form['j_password'] = password
br.submit()


page = fromstring(br.response().read())
del br

latest = page.cssselect('.download-release')
url = urlparse.urljoin('https://www.uktcregistration.nss.cfh.nhs.uk', latest[0].get('href'))

# download url to /tmp and unzip it.
urllib.urlretrieve (url, "dmd.zip")
zfile = zipfile.ZipFile("dmd.zip")
for name in zfile.namelist():
    (dirname, filename) = os.path.split(name)
    print "Decompressing " + filename + " on " + dirname
    if dirname and not os.path.exists(dirname):
        os.mkdir(dirname)
    fd = open(name,"w")
    fd.write(zfile.read(name))
    fd.close()
del zfile

source = None
for f in os.listdir("."):
    if f.startswith("f_amp2_"):
        source = f

gc.collect()

now = datetime.datetime.now().isoformat()
print "Loading from ", source

items = []
data = {"_when": now, "_source": source}
for event, elem in etree.iterparse(source):
    if elem.tag == "AMP":
        if 'APID' in data:
            items.append(data.copy())
            data = {"_when": now, "_source": source}        
            if len(items) == 100:
                scraperwiki.sqlite.save(['APID'], items)
                items = []
        else:
            print 'No APID in %s and event was %s' %(data,event)
    if elem.text:
        data[elem.tag] = elem.text
    if elem.tag == "DESC":
        m = supplier_re.match(elem.text)
        if m:
            data['SUPPLIER'] = m.groups()[0]
        else:
            data['SUPPLIER'] = "Unknown"
        

if items:
    scraperwiki.sqlite.save(['APID'], items)import scraperwiki
import os, cgi, gc
import mechanize
import re
import cookielib
import urlparse
import urllib
import zipfile
from lxml.html import fromstring
from lxml import etree
from cStringIO import StringIO
import datetime

env = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
username = env['USERNAME']
password = env['PASSWORD']

supplier_re = re.compile('.*\((.*?)\).*')

br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Login
r = br.open('https://www.uktcregistration.nss.cfh.nhs.uk/trud3/user/authenticated/group/0/pack/6/subpack/24/releases')
html = r.read()
br.select_form(nr=1)
br.form['j_username'] = username
br.form['j_password'] = password
br.submit()


page = fromstring(br.response().read())
del br

latest = page.cssselect('.download-release')
url = urlparse.urljoin('https://www.uktcregistration.nss.cfh.nhs.uk', latest[0].get('href'))

# download url to /tmp and unzip it.
urllib.urlretrieve (url, "dmd.zip")
zfile = zipfile.ZipFile("dmd.zip")
for name in zfile.namelist():
    (dirname, filename) = os.path.split(name)
    print "Decompressing " + filename + " on " + dirname
    if dirname and not os.path.exists(dirname):
        os.mkdir(dirname)
    fd = open(name,"w")
    fd.write(zfile.read(name))
    fd.close()
del zfile

source = None
for f in os.listdir("."):
    if f.startswith("f_amp2_"):
        source = f

gc.collect()

now = datetime.datetime.now().isoformat()
print "Loading from ", source

items = []
data = {"_when": now, "_source": source}
for event, elem in etree.iterparse(source):
    if elem.tag == "AMP":
        if 'APID' in data:
            items.append(data.copy())
            data = {"_when": now, "_source": source}        
            if len(items) == 100:
                scraperwiki.sqlite.save(['APID'], items)
                items = []
        else:
            print 'No APID in %s and event was %s' %(data,event)
    if elem.text:
        data[elem.tag] = elem.text
    if elem.tag == "DESC":
        m = supplier_re.match(elem.text)
        if m:
            data['SUPPLIER'] = m.groups()[0]
        else:
            data['SUPPLIER'] = "Unknown"
        

if items:
    scraperwiki.sqlite.save(['APID'], items)