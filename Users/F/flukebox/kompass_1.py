import scraperwiki
import re
import mechanize 
from BeautifulSoup import BeautifulSoup
import lxml.html
br=mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


url = "http://upresults.nic.in"
res = br.open(url)
url = "http://upresults.nic.in/UPXII13/InterGetRoll.htm"
br.open(url)
br.select_form(name="FrontPage_Form1")
br.form.set_all_readonly(False)
br["regno"]="0000001"
br.submit()
html = lxml.html.parse(br.response()) 

print "%r" %html.xpath("//html/body/center/table[2]")[0]import scraperwiki
import re
import mechanize 
from BeautifulSoup import BeautifulSoup
import lxml.html
br=mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


url = "http://upresults.nic.in"
res = br.open(url)
url = "http://upresults.nic.in/UPXII13/InterGetRoll.htm"
br.open(url)
br.select_form(name="FrontPage_Form1")
br.form.set_all_readonly(False)
br["regno"]="0000001"
br.submit()
html = lxml.html.parse(br.response()) 

print "%r" %html.xpath("//html/body/center/table[2]")[0]