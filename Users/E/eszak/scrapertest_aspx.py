import mechanize
import lxml.html

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

br = mechanize.Browser()
response = br.open(lotterygrantsurl)

print "All forms:", [ form.name  for form in br.forms() ]

br.select_form(name="aspnetForm")
print br.form

br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
br["ctl00$phMainContent$txtGrantDateFrom"] = "01/01/2004"
br["ctl00$phMainContent$txtGrantDateTo"]  = "20/01/2004"

response = br.submit()
print response.read()
import mechanize
import lxml.html

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

br = mechanize.Browser()
response = br.open(lotterygrantsurl)

print "All forms:", [ form.name  for form in br.forms() ]

br.select_form(name="aspnetForm")
print br.form

br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
br["ctl00$phMainContent$txtGrantDateFrom"] = "01/01/2004"
br["ctl00$phMainContent$txtGrantDateTo"]  = "20/01/2004"

response = br.submit()
print response.read()
