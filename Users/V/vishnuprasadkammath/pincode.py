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
#html = scraperwiki.scrape(url)
#root = lxml.html.fromstring(html)
br = mechanize.Browser()
response = br.open(url)
VAR1=response.read()
response.set_data(response.get_data()[717:])
br.set_response(response)
br.select_form(nr = 0)
br.set_all_readonly(False)
response = br.submit() #click on the submit button
VAR2 = response.read()
while True:
    c=2
    root = lxml.html.fromstring(VAR2)
    for el in root.cssselect("table#gvw_offices td"):
        print el.text_content()

    print VAR2

    mnext = re.search("""a href="javascript:__doPostBack(&#39;gvw_offices&#39;,&#39;Page$2&#39;)" style="color:Black;">""", VAR2)
    if not mnext:
        print"breaking"
        break

    br["__EVENTTARGET"] = mnext.group(1)
    br["__EVENTARGUMENT"] = mnext.group(2)
    VAR2=br.submit()
    
    c+=1

