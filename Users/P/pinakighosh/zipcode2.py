import scraperwiki
import mechanize
import re
import lxml.html
import sys
url="http://www.indiapost.gov.in/Pin/"
br = mechanize.Browser()
response = br.open(url)
print response
response = br.response()  
print response

headers = response.info() 
print "headers"
print headers
headers["Content-type"] = "text/html; charset=utf-8"
response.set_data(response.get_data().replace("<!---", "<!--"))
br.set_response(response)
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
br.set_handle_robots(False)
VAR1=response.read()
response.set_data(response.get_data()[717:])
br.set_response(response)
br.select_form(nr=0)
br.set_all_readonly(False)
print br
response = br.submit() #click on the submit button 
print br
VAR2 = response.read()
print "VAR2"
print VAR2
while True:
    c=2
    root = lxml.html.fromstring(VAR2)

    print root
    #for el in root.cssselect("table#gvw_offices td"):
       #print el.text_content()
    #print VAR2
    mnext = re.search("""<a href="javascript:__doPostBack(&#39;gvw_offices&#39;,&#39;Page$2&#39;)" style="color:Black;">2""", VAR2)
    #if not mnext:
        #print"breaking"
        #break
    br["__EVENTTARGET"] = 'gvw_offices'
    br["__eventArgument"] = 'Page$2'
    VAR2=br.submit()
    print VAR2
    VAR1=VAR2.read()
    VAR2.set_data(VAR2.get_data()[717:])
    br.set_response(VAR2)
    br.select_form(nr=0)
    br.set_all_readonly(False)
    print br
    response = br.submit() #click on the submit button 
    print br
    VAR2 = response.read()
    VAR2=br.submit()
    response = br.submit()
    VAR2 = response.read() # source code after submitting show all
    root = lxml.html.fromstring(VAR2)
    print root
    c+=1
import scraperwiki
import mechanize
import re
import lxml.html
import sys
url="http://www.indiapost.gov.in/Pin/"
br = mechanize.Browser()
response = br.open(url)
print response
response = br.response()  
print response

headers = response.info() 
print "headers"
print headers
headers["Content-type"] = "text/html; charset=utf-8"
response.set_data(response.get_data().replace("<!---", "<!--"))
br.set_response(response)
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
br.set_handle_robots(False)
VAR1=response.read()
response.set_data(response.get_data()[717:])
br.set_response(response)
br.select_form(nr=0)
br.set_all_readonly(False)
print br
response = br.submit() #click on the submit button 
print br
VAR2 = response.read()
print "VAR2"
print VAR2
while True:
    c=2
    root = lxml.html.fromstring(VAR2)

    print root
    #for el in root.cssselect("table#gvw_offices td"):
       #print el.text_content()
    #print VAR2
    mnext = re.search("""<a href="javascript:__doPostBack(&#39;gvw_offices&#39;,&#39;Page$2&#39;)" style="color:Black;">2""", VAR2)
    #if not mnext:
        #print"breaking"
        #break
    br["__EVENTTARGET"] = 'gvw_offices'
    br["__eventArgument"] = 'Page$2'
    VAR2=br.submit()
    print VAR2
    VAR1=VAR2.read()
    VAR2.set_data(VAR2.get_data()[717:])
    br.set_response(VAR2)
    br.select_form(nr=0)
    br.set_all_readonly(False)
    print br
    response = br.submit() #click on the submit button 
    print br
    VAR2 = response.read()
    VAR2=br.submit()
    response = br.submit()
    VAR2 = response.read() # source code after submitting show all
    root = lxml.html.fromstring(VAR2)
    print root
    c+=1
