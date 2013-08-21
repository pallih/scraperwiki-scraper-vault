import scraperwiki
import mechanize
import re
import lxml.html
import sys
url="www.indiapost.gov.in/pin"
##################################
#br = mechanize.Browser()
#response = br.open(url)
#response = br.response()  # this is a copy of response
#headers = response.info()  # currently, this is a mimetools.Message
#headers["Content-type"] = "text/html; charset=utf-8"
#response.set_data(response.get_data().replace("<!---", "<!--"))
#br.set_response(response)
##################################
#html = scraperwiki.scrape(url)
#root = lxml.html.fromstring(html)
br = mechanize.Browser()
response = br.open(url)
VAR1=response.read()
print br

response.set_data(response.get_data()[717:])
br.set_response(response)

br.select_form(nr = 0)
br.set_all_readonly(False)
response = br.submit()
VAR2 = response.read()
print br

while True:
    c=2
    root = lxml.html.fromstring(VAR2)
    for el in root.cssselect("table#gvw_offices td"):
        # for el2 in el.cssselect("td")
        print el.text_content()

        #response=br.open(url)
    response.set_data(response.get_data()[717:])
    br.set_response(response)
    print response.read()

    br.select_form(nr = 0)
    #mnext = re.search("Page\$2", VAR2)
    #if not mnext:
    #    print"breaking"
    #    break

    #br.form.new_control('hidden', '__EVENTTARGET', {'gvw_offices':''})
    #br.form.new_control('hidden', '__EVENTARGUMENT', {'Page$7':''})
    #br.form.fixup()
    br.set_all_readonly(False)
    br["__EVENTTARGET"] = "gvw_offices"
    br["__EVENTARGUMENT"] = "Page$7"
    response=br.submit()
    VAR2 = response.read()
    print VAR2

    c+=1
