# Attempt to simply get to the Lobbyist Registry page first

import mechanize 
import lxml.html

url1 = "http://www.lobbyistsregistrar.bc.ca/index.php?option=com_content&view=article&id=55&Itemid=75"
url2 = "https://eservice.pssg.gov.bc.ca/LRA/"
url3 = "https://eservice.pssg.gov.bc.ca/LRA/reporting/public/view.do"

br = mechanize.Browser()

br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url1)

page = response.read()

print page

br.ssl_version = "sslv3" # try

response2 = br.open(url2)

page2 = response2.read()

print page2

response3 = br.open(url3)

page3 = response3.read()

print page3


# Stuff I might use if I can ever actually get to the search form:

#print "All forms:", [ form.name  for form in br.forms() ]

#br.select_form(name="publicReportForm")
#print br.form

#br["designatedFiler"] = ["all"]
#br["registrationStatus"] = ["all"]
#br["startDate"] = "01/01/1990"
#br["endDate"]  = "02/23/2013"

#response = br.submit()
#print response.read()

