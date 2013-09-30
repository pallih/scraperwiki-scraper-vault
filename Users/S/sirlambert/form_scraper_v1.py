###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import scraperwiki 
import mechanize 
import lxml.html

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

br = mechanize.Browser()
response = br.open(lotterygrantsurl)

print "All forms:", [ form.name  for form in br.forms() ]

br.select_form(name="aspnetForm")
print "input:"
print br.form

#Submit form data
br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
br["ctl00$phMainContent$txtGrantDateFrom"] = "01/01/2004"
br["ctl00$phMainContent$txtGrantDateTo"]  = "20/01/2004"


response = br.submit()
print "output:"
print response.read()


# Parse HTML         



# Save to datastore


###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import scraperwiki 
import mechanize 
import lxml.html

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

br = mechanize.Browser()
response = br.open(lotterygrantsurl)

print "All forms:", [ form.name  for form in br.forms() ]

br.select_form(name="aspnetForm")
print "input:"
print br.form

#Submit form data
br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
br["ctl00$phMainContent$txtGrantDateFrom"] = "01/01/2004"
br["ctl00$phMainContent$txtGrantDateTo"]  = "20/01/2004"


response = br.submit()
print "output:"
print response.read()


# Parse HTML         



# Save to datastore


