import mechanize 
import lxml.html
import scraperwiki

tnmethlabdb = "http://www.rid-meth.org/frmSearchSite2.aspx"

br = mechanize.Browser()
response = br.open(tnmethlabdb)

print "All forms:", [ form.name  for form in br.forms() ]

br.select_form(name="aspnetForm")
print br.form

response = br.submit()
print response.read()

