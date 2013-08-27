###############################################################################
# START HERE: Tutorial for scraping ASP.NET pages (HTML pages that end .aspx), using the
# very powerful Mechanize library. In general, when you follow a 'next' link on 
# .aspx pages, you're actually submitting a form.
# This tutorial demonstrates scraping a particularly tricky example. 
###############################################################################
import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(soup):
    data_table = soup.find("table", { "class" : "reports" })
    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['Name'] = table_cells[0].text
            record['Town'] = table_cells[1].text
            record['Country'] = table_cells[2].text
            record['Year'] = table_cells[3].text
            record['Ages'] = table_cells[4].text
            record['Gender'] = table_cells[5].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Name' is our unique key - 
            scraperwiki.datastore.save(["Name"], record)
        
# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(soup):
    scrape_table(soup)
#    next_link = soup.find("a", { "id" : "ProviderSearchResultsTable1_NextLinkButton" })
 #   if next_link:
  #      # find the page's form
   #     br.select_form(name='ctl00')
    #    br.form.set_all_readonly(False)
     #   # set the relevant ASP.NET fields, as required in the page's onSubmit function
      #  # Your .aspx page may not have these
       # # Luckily we can ignore the __VIEWSTATE variable: mechanize handles this for us.
#        br['__EVENTTARGET'] = 'ProviderSearchResultsTable1$NextLinkButton'
 #       br['__EVENTARGUMENT'] = ''
  #      br.submit()
   #     soup = BeautifulSoup(br.response().read())
    #    scrape_and_look_for_next_link(soup)

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

starting_url = 'http://www.isi.net/reports/'
br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(starting_url)
print "All forms:", [ form.name  for form in br.forms() ]
br.select_form(name="form")
response = br.submit()
soup = BeautifulSoup(br.response().read())
# Have a look at 'soup': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.
print soup 
# start scraping
scrape_and_look_for_next_link(soup)
###############################################################################
# START HERE: Tutorial for scraping ASP.NET pages (HTML pages that end .aspx), using the
# very powerful Mechanize library. In general, when you follow a 'next' link on 
# .aspx pages, you're actually submitting a form.
# This tutorial demonstrates scraping a particularly tricky example. 
###############################################################################
import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(soup):
    data_table = soup.find("table", { "class" : "reports" })
    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['Name'] = table_cells[0].text
            record['Town'] = table_cells[1].text
            record['Country'] = table_cells[2].text
            record['Year'] = table_cells[3].text
            record['Ages'] = table_cells[4].text
            record['Gender'] = table_cells[5].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Name' is our unique key - 
            scraperwiki.datastore.save(["Name"], record)
        
# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(soup):
    scrape_table(soup)
#    next_link = soup.find("a", { "id" : "ProviderSearchResultsTable1_NextLinkButton" })
 #   if next_link:
  #      # find the page's form
   #     br.select_form(name='ctl00')
    #    br.form.set_all_readonly(False)
     #   # set the relevant ASP.NET fields, as required in the page's onSubmit function
      #  # Your .aspx page may not have these
       # # Luckily we can ignore the __VIEWSTATE variable: mechanize handles this for us.
#        br['__EVENTTARGET'] = 'ProviderSearchResultsTable1$NextLinkButton'
 #       br['__EVENTARGUMENT'] = ''
  #      br.submit()
   #     soup = BeautifulSoup(br.response().read())
    #    scrape_and_look_for_next_link(soup)

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

starting_url = 'http://www.isi.net/reports/'
br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(starting_url)
print "All forms:", [ form.name  for form in br.forms() ]
br.select_form(name="form")
response = br.submit()
soup = BeautifulSoup(br.response().read())
# Have a look at 'soup': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.
print soup 
# start scraping
scrape_and_look_for_next_link(soup)
###############################################################################
# START HERE: Tutorial for scraping ASP.NET pages (HTML pages that end .aspx), using the
# very powerful Mechanize library. In general, when you follow a 'next' link on 
# .aspx pages, you're actually submitting a form.
# This tutorial demonstrates scraping a particularly tricky example. 
###############################################################################
import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(soup):
    data_table = soup.find("table", { "class" : "reports" })
    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['Name'] = table_cells[0].text
            record['Town'] = table_cells[1].text
            record['Country'] = table_cells[2].text
            record['Year'] = table_cells[3].text
            record['Ages'] = table_cells[4].text
            record['Gender'] = table_cells[5].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Name' is our unique key - 
            scraperwiki.datastore.save(["Name"], record)
        
# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(soup):
    scrape_table(soup)
#    next_link = soup.find("a", { "id" : "ProviderSearchResultsTable1_NextLinkButton" })
 #   if next_link:
  #      # find the page's form
   #     br.select_form(name='ctl00')
    #    br.form.set_all_readonly(False)
     #   # set the relevant ASP.NET fields, as required in the page's onSubmit function
      #  # Your .aspx page may not have these
       # # Luckily we can ignore the __VIEWSTATE variable: mechanize handles this for us.
#        br['__EVENTTARGET'] = 'ProviderSearchResultsTable1$NextLinkButton'
 #       br['__EVENTARGUMENT'] = ''
  #      br.submit()
   #     soup = BeautifulSoup(br.response().read())
    #    scrape_and_look_for_next_link(soup)

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

starting_url = 'http://www.isi.net/reports/'
br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(starting_url)
print "All forms:", [ form.name  for form in br.forms() ]
br.select_form(name="form")
response = br.submit()
soup = BeautifulSoup(br.response().read())
# Have a look at 'soup': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.
print soup 
# start scraping
scrape_and_look_for_next_link(soup)
###############################################################################
# START HERE: Tutorial for scraping ASP.NET pages (HTML pages that end .aspx), using the
# very powerful Mechanize library. In general, when you follow a 'next' link on 
# .aspx pages, you're actually submitting a form.
# This tutorial demonstrates scraping a particularly tricky example. 
###############################################################################
import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(soup):
    data_table = soup.find("table", { "class" : "reports" })
    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['Name'] = table_cells[0].text
            record['Town'] = table_cells[1].text
            record['Country'] = table_cells[2].text
            record['Year'] = table_cells[3].text
            record['Ages'] = table_cells[4].text
            record['Gender'] = table_cells[5].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Name' is our unique key - 
            scraperwiki.datastore.save(["Name"], record)
        
# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(soup):
    scrape_table(soup)
#    next_link = soup.find("a", { "id" : "ProviderSearchResultsTable1_NextLinkButton" })
 #   if next_link:
  #      # find the page's form
   #     br.select_form(name='ctl00')
    #    br.form.set_all_readonly(False)
     #   # set the relevant ASP.NET fields, as required in the page's onSubmit function
      #  # Your .aspx page may not have these
       # # Luckily we can ignore the __VIEWSTATE variable: mechanize handles this for us.
#        br['__EVENTTARGET'] = 'ProviderSearchResultsTable1$NextLinkButton'
 #       br['__EVENTARGUMENT'] = ''
  #      br.submit()
   #     soup = BeautifulSoup(br.response().read())
    #    scrape_and_look_for_next_link(soup)

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

starting_url = 'http://www.isi.net/reports/'
br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(starting_url)
print "All forms:", [ form.name  for form in br.forms() ]
br.select_form(name="form")
response = br.submit()
soup = BeautifulSoup(br.response().read())
# Have a look at 'soup': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.
print soup 
# start scraping
scrape_and_look_for_next_link(soup)
