import scraperwiki
import mechanize 
import re
import lxml.html
import sys
url="http://www.indiapost.gov.in/Pin/"
##################################
br = mechanize.Browser()
response = br.open(url)
response = br.response()  # this is a copy of response
headers = response.info()  # currently, this is a mimetools.Message
headers["Content-type"] = "text/html; charset=utf-8"
response.set_data(response.get_data().replace("<!---", "<!--"))
br.set_response(response)
##################################
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
br = mechanize.Browser()
response = br.open(url)
VAR1=response.read()
response.set_data(response.get_data()[717:])
br.set_response(response)
br.select_form(nr = 0)
br.set_all_readonly(False)
#mnext = re.search("""<input type="submit" name="search_on" value="Search" id="search_on" tabindex="2" style="width:48px;height:23px;font-size:8pt;font-family:Arial;color:White;border-width:1px;border-style:Solid;border-color:#C04000;background-color:#C04000;" /></td>""", VAR1)
#for i in range(718):
#   print VAR1[i]
#if not mnext:
    #print "Not found"
    #sys.exit(0)
#print mnext
#br["__EVENTTARGET"] = mnext.group(1)
#br["__EVENTARGUMENT"] = mnext.group(2)
response = br.submit()
VAR2 = response.read() # source code after submitting show all
#print VAR2
c=0
root = lxml.html.fromstring(VAR2)
for el in root.cssselect("table#gvw_offices tr"):
    #print c
    #c+=1
    print el.text_content()
    #print el
    #for el2 in el.cssselect("tr. td")
        #print el2.text_content()
#mnext = re.search("""a href="javascript:__doPostBack(&#39;gvw_offices&#39;,&#39;Page$2&#39;)" style="color:Black;""""", VAR2)
#print mnext
from twill.commands import * 
b = get_browser()  
b.go("http://www.indiapost.gov.in/Pin/") 
b.showforms()
