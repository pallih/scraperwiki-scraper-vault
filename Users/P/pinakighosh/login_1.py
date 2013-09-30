import scraperwiki
import mechanize
import re
import lxml.html
import sys
import requests
from bs4 import BeautifulSoup

url="http://en.wikipedia.org/wiki/List_of_districts_of_India"
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)
VAR1 = response.read()
#nr=0 if form has no name        
br.select_form(nr=0)
br.set_all_readonly(False)
d=dict()
# get the names of the control fields
for control in br.form.controls:
    print control.name
    #d[control.name]=br[control.name]
#for i in d:
 #   print i+':'+str(d[i])            
br["Username"]='ghosh.pinaki@tcs.com'
br["Password"]='Mufc@2013'
response = br.submit()
var=response.read()
print var
import scraperwiki
import mechanize
import re
import lxml.html
import sys
import requests
from bs4 import BeautifulSoup

url="http://en.wikipedia.org/wiki/List_of_districts_of_India"
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)
VAR1 = response.read()
#nr=0 if form has no name        
br.select_form(nr=0)
br.set_all_readonly(False)
d=dict()
# get the names of the control fields
for control in br.form.controls:
    print control.name
    #d[control.name]=br[control.name]
#for i in d:
 #   print i+':'+str(d[i])            
br["Username"]='ghosh.pinaki@tcs.com'
br["Password"]='Mufc@2013'
response = br.submit()
var=response.read()
print var
