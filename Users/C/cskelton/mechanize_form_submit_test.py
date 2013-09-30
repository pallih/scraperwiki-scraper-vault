###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import mechanize 
import lxml.html
import re

originalurl = "http://www.lobbyistsregistrar.bc.ca/index.php?option=com_content&view=article&id=55&Itemid=75"

br = mechanize.Browser()
response = br.open(originalurl)
page = response.read()
print page

response = br.click(type='button') # doesn't work
page = response.read()
print page

#response=br.follow_link(text_regex='lobbying rules') #this works
#page= response.read()
#print page



#br.follow_link(text_regex='Search Registry')
#page = br.read()
#print page
#br.follow_link(text_regex="Search the Registry')
#page = br.read()
#print page

#print "All forms:", [ form.name  for form in br.forms() ]

#br.select_form(name="publicReportForm")
#print br.form

#br["designatedFiler"] = ["all"]
#br["registrationStatus"] = ["all"]
#br["startDate"] = "01/01/1990"
#br["endDate"]  = "02/23/2013"

#response = br.submit()
#print response.read()


###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import mechanize 
import lxml.html
import re

originalurl = "http://www.lobbyistsregistrar.bc.ca/index.php?option=com_content&view=article&id=55&Itemid=75"

br = mechanize.Browser()
response = br.open(originalurl)
page = response.read()
print page

response = br.click(type='button') # doesn't work
page = response.read()
print page

#response=br.follow_link(text_regex='lobbying rules') #this works
#page= response.read()
#print page



#br.follow_link(text_regex='Search Registry')
#page = br.read()
#print page
#br.follow_link(text_regex="Search the Registry')
#page = br.read()
#print page

#print "All forms:", [ form.name  for form in br.forms() ]

#br.select_form(name="publicReportForm")
#print br.form

#br["designatedFiler"] = ["all"]
#br["registrationStatus"] = ["all"]
#br["startDate"] = "01/01/1990"
#br["endDate"]  = "02/23/2013"

#response = br.submit()
#print response.read()


