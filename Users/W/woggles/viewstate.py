import scraperwiki
from BeautifulSoup import BeautifulSoup
import mechanize
import cookielib
import time
from mechanize import ParseResponse
import urllib
import urllib2
import lxml.html
import re

# Browser
br = mechanize.Browser(factory=mechanize.RobustFactory())
#print "ok mechanize"
    
# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
    
#print "ok cookie"
    
# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
    
#print "ok options"
    
# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    
#print "ok handle"
# Want debugging messages?
br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)
    
# User-Agent 
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
print "ok headers"
#--- end headers
url = "https://www3.prefeitura.sp.gov.br/sf8663/formsinternet/Principal.aspx"
j = 2051
my_list = ["['1']", "['2']", "['3']"]
#---- end declarations

response = br.open(url)
html = response.read()
#print "ok have got html"
#print html
root = lxml.html.fromstring(html)
#print "ok have lxml'd it"

for form in br.forms():
    print "Form name:", form.name

br.select_form("frmCadastro")
br["txtSetor"] = "003"
br["txtQuadra"] = "006"
br["txtLote"] = "0001"
br["txtDigito"] = dac

import cgi 

request = br.click() 
for k,v in cgi.parse_qsl(request.get_data()): 
    print (k,v)


