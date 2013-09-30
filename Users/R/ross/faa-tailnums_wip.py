#!/usr/bin/env python

import scraperwiki
import zipfile
import os
import tempfile
import sys
import subprocess
import requests

#import re

zipurl = "https://media.scraperwiki.com/custom/AR102011.zip"             
zipfname = None

#print subprocess.check_output(["echo", "-n", "Hello World!"])
#print "bar"

with tempfile.NamedTemporaryFile(suffix='.zip',mode='wb',delete=False,) as zipout:
    zipfname = zipout.name
    zipout.write(scraperwiki.scrape(zipurl))
    #zipout.write(requests.get(zipurl,headers={"x-cache":""}))
    zipout.flush()

print "foo"

print subprocess.check_output(["stat",zipfname])
print subprocess.check_output(["ls", "-lk", zipfname])
print subprocess.check_output(["sha1sum",zipfname])

zipfl = zipfile.ZipFile(zipfname, 'r')
zipfl.printdir()
print zipfl.infolist()
print zipfl.namelist()
#!/usr/bin/env python

import scraperwiki
import zipfile
import os
import tempfile
import sys
import subprocess
import requests

#import re

zipurl = "https://media.scraperwiki.com/custom/AR102011.zip"             
zipfname = None

#print subprocess.check_output(["echo", "-n", "Hello World!"])
#print "bar"

with tempfile.NamedTemporaryFile(suffix='.zip',mode='wb',delete=False,) as zipout:
    zipfname = zipout.name
    zipout.write(scraperwiki.scrape(zipurl))
    #zipout.write(requests.get(zipurl,headers={"x-cache":""}))
    zipout.flush()

print "foo"

print subprocess.check_output(["stat",zipfname])
print subprocess.check_output(["ls", "-lk", zipfname])
print subprocess.check_output(["sha1sum",zipfname])

zipfl = zipfile.ZipFile(zipfname, 'r')
zipfl.printdir()
print zipfl.infolist()
print zipfl.namelist()
#!/usr/bin/env python

import scraperwiki
import zipfile
import os
import tempfile
import sys
import subprocess
import requests

#import re

zipurl = "https://media.scraperwiki.com/custom/AR102011.zip"             
zipfname = None

#print subprocess.check_output(["echo", "-n", "Hello World!"])
#print "bar"

with tempfile.NamedTemporaryFile(suffix='.zip',mode='wb',delete=False,) as zipout:
    zipfname = zipout.name
    zipout.write(scraperwiki.scrape(zipurl))
    #zipout.write(requests.get(zipurl,headers={"x-cache":""}))
    zipout.flush()

print "foo"

print subprocess.check_output(["stat",zipfname])
print subprocess.check_output(["ls", "-lk", zipfname])
print subprocess.check_output(["sha1sum",zipfname])

zipfl = zipfile.ZipFile(zipfname, 'r')
zipfl.printdir()
print zipfl.infolist()
print zipfl.namelist()
#!/usr/bin/env python

import scraperwiki
import zipfile
import os
import tempfile
import sys
import subprocess
import requests

#import re

zipurl = "https://media.scraperwiki.com/custom/AR102011.zip"             
zipfname = None

#print subprocess.check_output(["echo", "-n", "Hello World!"])
#print "bar"

with tempfile.NamedTemporaryFile(suffix='.zip',mode='wb',delete=False,) as zipout:
    zipfname = zipout.name
    zipout.write(scraperwiki.scrape(zipurl))
    #zipout.write(requests.get(zipurl,headers={"x-cache":""}))
    zipout.flush()

print "foo"

print subprocess.check_output(["stat",zipfname])
print subprocess.check_output(["ls", "-lk", zipfname])
print subprocess.check_output(["sha1sum",zipfname])

zipfl = zipfile.ZipFile(zipfname, 'r')
zipfl.printdir()
print zipfl.infolist()
print zipfl.namelist()
