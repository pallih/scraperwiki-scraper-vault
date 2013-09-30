###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import mechanize 
import lxml.html

url = "http://www.news.gov.bc.ca/"

br = mechanize.Browser()
response = br.open(url)

print response.read()

print "All forms:", [ form.name  for form in br.forms() ]

br.select_form(name="aspnetForm")
print br.form # looking at form for key input types is important before looking at source html

br["ctl00$ContentPlaceHolder1$btnNextPage"] = ">" # this works to grab next page 

#br["ctl00$ContentPlaceHolder1$listOrganisation"] = ["58fcb55a-7d99-4c65-96ed-8658de8496f6"] # this works as search on one of the ministries, check source to see which code corresponds with which ministry

response = br.submit()
print response.read()


###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import mechanize 
import lxml.html

url = "http://www.news.gov.bc.ca/"

br = mechanize.Browser()
response = br.open(url)

print response.read()

print "All forms:", [ form.name  for form in br.forms() ]

br.select_form(name="aspnetForm")
print br.form # looking at form for key input types is important before looking at source html

br["ctl00$ContentPlaceHolder1$btnNextPage"] = ">" # this works to grab next page 

#br["ctl00$ContentPlaceHolder1$listOrganisation"] = ["58fcb55a-7d99-4c65-96ed-8658de8496f6"] # this works as search on one of the ministries, check source to see which code corresponds with which ministry

response = br.submit()
print response.read()


