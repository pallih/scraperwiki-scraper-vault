import scraperwiki
import lxml.html
#import string
import mechanize
import re

targetURL="http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Economic_Data/Cultivators.aspx"
br = mechanize.Browser()       #open the url
br.addHeaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
webPage = br.open(targetURL)
print "All forms:", [ form.name  for form in br.forms() ]
print 'webPage'
print webPage

br.select_form(name="Form1")
print br.form

br.set_all_readonly(False)
html = webPage.read()
  
br.form['document.Form1.txtUserID.value']='vivekrawat'
br.form['document.Form1.txtPassword.value']='powerzone'
br.find_control("btnSearch").disabled = True

VAR = br.submit()



