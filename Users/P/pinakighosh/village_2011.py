import scraperwiki
import mechanize
import lxml.html

url="http://censusindia.gov.in/2011census/Listofvillagesandtowns.aspx"
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
html=scraperwiki.scrape(url)
print html
response = br.open(url)
VAR1 = response.read() #reads the source file for the web page
br.select_form("Form1")
br.set_all_readonly(False)
######drpState
d=dict()
for control in br.form.controls:
    d[control.name]=br[control.name]
#for i in d:
 #   print i+" "+str(d[i])
br["drpState"]=['19']
#response = br.submit()
#response = br.open(url)
#var=response.read()
#print response.read()
br["drpDistrict"]=['null']
br["drpsubdistrict"]=['null']
response = br.submit()
response = br.open(url)
#print response
var=response.read()
br.select_form("Form1")
br.set_all_readonly(False)
#root=lxml.html.fromstring(var)
#print root
for control in br.form.controls:
    d[control.name]=br[control.name]
#for i in d:
 #   print i+" "+str(d[i])
br["drpState"]=['19']
#response = br.submit()
#response = br.open(url)
#var=response.read()
#print response.read()
br["drpDistrict"]=['638']
br["drpsubdistrict"]=['05916']import scraperwiki
import mechanize
import lxml.html

url="http://censusindia.gov.in/2011census/Listofvillagesandtowns.aspx"
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
html=scraperwiki.scrape(url)
print html
response = br.open(url)
VAR1 = response.read() #reads the source file for the web page
br.select_form("Form1")
br.set_all_readonly(False)
######drpState
d=dict()
for control in br.form.controls:
    d[control.name]=br[control.name]
#for i in d:
 #   print i+" "+str(d[i])
br["drpState"]=['19']
#response = br.submit()
#response = br.open(url)
#var=response.read()
#print response.read()
br["drpDistrict"]=['null']
br["drpsubdistrict"]=['null']
response = br.submit()
response = br.open(url)
#print response
var=response.read()
br.select_form("Form1")
br.set_all_readonly(False)
#root=lxml.html.fromstring(var)
#print root
for control in br.form.controls:
    d[control.name]=br[control.name]
#for i in d:
 #   print i+" "+str(d[i])
br["drpState"]=['19']
#response = br.submit()
#response = br.open(url)
#var=response.read()
#print response.read()
br["drpDistrict"]=['638']
br["drpsubdistrict"]=['05916']