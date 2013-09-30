import scraperwiki
import mechanize # added by Usha
import re # added by Usha
import lxml.html
import string
from mechanize import ParseResponse, urlopen, urljoin
url="http://www.censusindia.gov.in/aboutus/personnel/perdirectory.aspx"
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response=br.open(url)
VAR1=response.read()
print VAR1
#for form in br.forms():
    # print "Form name:", form.name
br.select_form("formQuick")#selecting the corresponding form
br.set_all_readonly(False)
a=[]
#b=[]
root = lxml.html.fromstring(VAR1)

for i in root.cssselect("select#drpstate option"):
    a.append(i.text_content())

#control = br.form.find_control("drpstate")

# Having a select control tells you what values can be selected
#if control.type == "select": # means it's class ClientForm.SelectControl 
  #  for item in control.items: 
   #     a.append(item.text_content())
a=a[2:]
print a
forms = ParseResponse(response, backwards_compat=False)
listlen=len(a)
print listlen
count=0
#control = br.form.find_control("drpstate")
#while count<=listlen:
#control.value=[a[count]]
mnext=re.search("""<select name="drpstate" onchange="javascript:setTimeout('__doPostBack(\'drpstate\',\'\')', 0)" id="drpstate">""",VAR1)
print mnext
print "finished"

import scraperwiki
import mechanize # added by Usha
import re # added by Usha
import lxml.html
import string
from mechanize import ParseResponse, urlopen, urljoin
url="http://www.censusindia.gov.in/aboutus/personnel/perdirectory.aspx"
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response=br.open(url)
VAR1=response.read()
print VAR1
#for form in br.forms():
    # print "Form name:", form.name
br.select_form("formQuick")#selecting the corresponding form
br.set_all_readonly(False)
a=[]
#b=[]
root = lxml.html.fromstring(VAR1)

for i in root.cssselect("select#drpstate option"):
    a.append(i.text_content())

#control = br.form.find_control("drpstate")

# Having a select control tells you what values can be selected
#if control.type == "select": # means it's class ClientForm.SelectControl 
  #  for item in control.items: 
   #     a.append(item.text_content())
a=a[2:]
print a
forms = ParseResponse(response, backwards_compat=False)
listlen=len(a)
print listlen
count=0
#control = br.form.find_control("drpstate")
#while count<=listlen:
#control.value=[a[count]]
mnext=re.search("""<select name="drpstate" onchange="javascript:setTimeout('__doPostBack(\'drpstate\',\'\')', 0)" id="drpstate">""",VAR1)
print mnext
print "finished"

