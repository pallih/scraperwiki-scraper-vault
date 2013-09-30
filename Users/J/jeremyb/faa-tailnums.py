#!/usr/bin/env python

import scraperwiki
import zipfile
import os
import tempfile
import sys
import subprocess
import requests

#import re

# I've copied that file down to our local server, so it should get served to 
# you across the VLAN fairly quickly.  Unfortunately we don't yet have support
# for a local persistent file store, but we're discussing it.
#
# Obviously this won't be much use if the .zip is updated regularly :(
#zipurl = "https://media.scraperwiki.com/custom/AR102011.zip" 
 
           
zipurl = "http://registry.faa.gov/database/AR102011.zip"             
zipfname = None

print subprocess.check_output(["echo", "-n", "Hello World!"])
print "bar"

with tempfile.NamedTemporaryFile(suffix='.zip',mode='wb',delete=False,) as zipout:
    zipfname = zipout.name

    # scraperwiki.scrape() will cache when you're running the code from the editor, but it
    # shouldn't cache too heavily if running as a scheduled task
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

# I've copied that file down to our local server, so it should get served to 
# you across the VLAN fairly quickly.  Unfortunately we don't yet have support
# for a local persistent file store, but we're discussing it.
#
# Obviously this won't be much use if the .zip is updated regularly :(
#zipurl = "https://media.scraperwiki.com/custom/AR102011.zip" 
 
           
zipurl = "http://registry.faa.gov/database/AR102011.zip"             
zipfname = None

print subprocess.check_output(["echo", "-n", "Hello World!"])
print "bar"

with tempfile.NamedTemporaryFile(suffix='.zip',mode='wb',delete=False,) as zipout:
    zipfname = zipout.name

    # scraperwiki.scrape() will cache when you're running the code from the editor, but it
    # shouldn't cache too heavily if running as a scheduled task
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
