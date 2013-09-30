import mechanize 
from BeautifulSoup import BeautifulSoup

url = "http://www.highways.gov.uk/roads/basicRPSearch.aspx"
br = mechanize.Browser()
br.open(url)
br.select_form(name = "roadprojects_search")

# Set the fields
br["BasicRoadProjectSearch1$dlstRegion"] = ["3"]
br["BasicRoadProjectSearch1$dlstResultsPerPage"] = ["50"]

# and submit the form
br.submit()


# We can now start processing it as normal
read_generated_page = br.response().read()
print read_generated_page
soup = BeautifulSoup(read_generated_page)
#prettify cleans up and indents the page​ - beautifulsoup
print soup.prettify()
pagecount = soup.findAll('rp_projectName')

#this generates a weird square when run - no idea what that is. Check documentation.
print soup.findAll('rp_projectName')

#this bit saves the data in the scraperwiki datastore​​
for a in pagecount:
     record = { "project" : a.text } # column name and value
     scraperwiki.datastore.save(["project"], record) # save the records one by one
import mechanize 
from BeautifulSoup import BeautifulSoup

url = "http://www.highways.gov.uk/roads/basicRPSearch.aspx"
br = mechanize.Browser()
br.open(url)
br.select_form(name = "roadprojects_search")

# Set the fields
br["BasicRoadProjectSearch1$dlstRegion"] = ["3"]
br["BasicRoadProjectSearch1$dlstResultsPerPage"] = ["50"]

# and submit the form
br.submit()


# We can now start processing it as normal
read_generated_page = br.response().read()
print read_generated_page
soup = BeautifulSoup(read_generated_page)
#prettify cleans up and indents the page​ - beautifulsoup
print soup.prettify()
pagecount = soup.findAll('rp_projectName')

#this generates a weird square when run - no idea what that is. Check documentation.
print soup.findAll('rp_projectName')

#this bit saves the data in the scraperwiki datastore​​
for a in pagecount:
     record = { "project" : a.text } # column name and value
     scraperwiki.datastore.save(["project"], record) # save the records one by one
import mechanize 
from BeautifulSoup import BeautifulSoup

url = "http://www.highways.gov.uk/roads/basicRPSearch.aspx"
br = mechanize.Browser()
br.open(url)
br.select_form(name = "roadprojects_search")

# Set the fields
br["BasicRoadProjectSearch1$dlstRegion"] = ["3"]
br["BasicRoadProjectSearch1$dlstResultsPerPage"] = ["50"]

# and submit the form
br.submit()


# We can now start processing it as normal
read_generated_page = br.response().read()
print read_generated_page
soup = BeautifulSoup(read_generated_page)
#prettify cleans up and indents the page​ - beautifulsoup
print soup.prettify()
pagecount = soup.findAll('rp_projectName')

#this generates a weird square when run - no idea what that is. Check documentation.
print soup.findAll('rp_projectName')

#this bit saves the data in the scraperwiki datastore​​
for a in pagecount:
     record = { "project" : a.text } # column name and value
     scraperwiki.datastore.save(["project"], record) # save the records one by one
import mechanize 
from BeautifulSoup import BeautifulSoup

url = "http://www.highways.gov.uk/roads/basicRPSearch.aspx"
br = mechanize.Browser()
br.open(url)
br.select_form(name = "roadprojects_search")

# Set the fields
br["BasicRoadProjectSearch1$dlstRegion"] = ["3"]
br["BasicRoadProjectSearch1$dlstResultsPerPage"] = ["50"]

# and submit the form
br.submit()


# We can now start processing it as normal
read_generated_page = br.response().read()
print read_generated_page
soup = BeautifulSoup(read_generated_page)
#prettify cleans up and indents the page​ - beautifulsoup
print soup.prettify()
pagecount = soup.findAll('rp_projectName')

#this generates a weird square when run - no idea what that is. Check documentation.
print soup.findAll('rp_projectName')

#this bit saves the data in the scraperwiki datastore​​
for a in pagecount:
     record = { "project" : a.text } # column name and value
     scraperwiki.datastore.save(["project"], record) # save the records one by one
import mechanize 
from BeautifulSoup import BeautifulSoup

url = "http://www.highways.gov.uk/roads/basicRPSearch.aspx"
br = mechanize.Browser()
br.open(url)
br.select_form(name = "roadprojects_search")

# Set the fields
br["BasicRoadProjectSearch1$dlstRegion"] = ["3"]
br["BasicRoadProjectSearch1$dlstResultsPerPage"] = ["50"]

# and submit the form
br.submit()


# We can now start processing it as normal
read_generated_page = br.response().read()
print read_generated_page
soup = BeautifulSoup(read_generated_page)
#prettify cleans up and indents the page​ - beautifulsoup
print soup.prettify()
pagecount = soup.findAll('rp_projectName')

#this generates a weird square when run - no idea what that is. Check documentation.
print soup.findAll('rp_projectName')

#this bit saves the data in the scraperwiki datastore​​
for a in pagecount:
     record = { "project" : a.text } # column name and value
     scraperwiki.datastore.save(["project"], record) # save the records one by one
