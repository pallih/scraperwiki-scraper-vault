import scraperwiki

import mechanize
import re

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open("http://data.fingal.ie/ViewDataSets/")

for i in range(10):
    html = response.read()
    print "Page %d :" % i, html
    br.find_control("btnSearch").disabled = True
    br.select_form(nr=0)
    print br.form
    br.set_all_readonly(False)
    mnext = re.search("""<a id="lnkNext" href="javascript:__doPostBack\('(.*?)','(.*?)'\)">Next >>""", html)
    if not mnext:
        break
    br["__EVENTTARGET"] = mnext.group(1)
    br["__EVENTARGUMENT"] = mnext.group(2)
    response = br.submit()