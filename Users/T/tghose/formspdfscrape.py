###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://api.plone.org/Plone/2.5.3/private/PasswordResetTool/private/mechanize._mechanize.Browser-class.html
###############################################################################
import mechanize 
import re
import urlparse
import scraperwiki

from BeautifulSoup import BeautifulSoup

# We're scraping the National Lottery grants form. You can
# replace this with the URL you're interested in. 
url = "http://gao.gov/docsearch/agency.php"
br = mechanize.Browser()
br.open(url)
index = 1

#--------------------------------------------------------------------------------------
# Loop through all the forms on the page, and print some information about each one.
# This should work with your own URL.
#--------------------------------------------------------------------------------------
for form in br.forms():
    print "--------------------"
    print "Form name : " + form.name 
    br.select_form(name=form.name)
    
    # loop through the controls in the form
    print "Controls:"
    for control in br.form.controls:
        if not control.name:
            print " - (type) =", (control.type)
            continue
            
        print " - (name, type, value) =", (control.name, control.type, br[control.name])

        # loop through all the options in any select (drop-down) controls
        if control.type == 'select' or control.type == 'checkbox':
            for item in control.items:
                print " - - - (value, labels) =", (str(item), [label.text  for label in item.get_labels()])

#--------------------------------------------------------------------------------------
# Next, let's submit the main form.
#--------------------------------------------------------------------------------------

# First, tell Mechanize which form to submit.
# If your form didn't have a CSS name attribute, use 'nr' instead 
# - e.g. br.select_form(nr=0) to find the first form on the page. 


def scrape_page(soup):
    #links = soup.findAll(href=re.compile('pdf$'))
    results = soup.findAll(attrs={'class' : 'scannableList'})
    print results
    record = {}
    for result in results:
        record['Index'] = index
        global index
        index = index + 1
        record['GAONumber'] = result.dd.a.text
        record['Title'] = result.dt.text
        m = re.search('&nbsp;&nbsp;(.*)', result.dd.text)
        record['PubDate'] = m.group(1)
        record['link'] = result.dd.a['href']
        print result.dt.text
        print result.dd.a.text
        print result.dd.text
        scraperwiki.datastore.save(["GAONumber","Index"],record)
    #does it for every page of search results

def scrape_and_look_for_next_link(base_url, soup):
    scrape_page(soup)
    next_link = soup.find(title="Next Page")
    print next_link
    if next_link:
        next_url = base_url + next_link['href']
        print next_url
        br.open(next_url)
        next_soup = BeautifulSoup(br.response().read())
        scrape_and_look_for_next_link(base_url, next_soup)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
br.select_form(name='docdblite_agency')

# Set the fields: here we're looking for grants by Arts Council England in London
br["date1_month"] = ["9"]
br["date1_year"] = ["2001"]
br["date2_month"] = ["12"]
br["date2_year"] = ["2010"]
br["agency[]"] = ["Department of Homeland Security"]

# and submit the form
br.submit()
soup = BeautifulSoup(br.response().read())

base_url = 'http://gao.gov/docsearch/'
starting_url = base_url + 'app_processform.php'
scrape_and_look_for_next_link(base_url, soup)
###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://api.plone.org/Plone/2.5.3/private/PasswordResetTool/private/mechanize._mechanize.Browser-class.html
###############################################################################
import mechanize 
import re
import urlparse
import scraperwiki

from BeautifulSoup import BeautifulSoup

# We're scraping the National Lottery grants form. You can
# replace this with the URL you're interested in. 
url = "http://gao.gov/docsearch/agency.php"
br = mechanize.Browser()
br.open(url)
index = 1

#--------------------------------------------------------------------------------------
# Loop through all the forms on the page, and print some information about each one.
# This should work with your own URL.
#--------------------------------------------------------------------------------------
for form in br.forms():
    print "--------------------"
    print "Form name : " + form.name 
    br.select_form(name=form.name)
    
    # loop through the controls in the form
    print "Controls:"
    for control in br.form.controls:
        if not control.name:
            print " - (type) =", (control.type)
            continue
            
        print " - (name, type, value) =", (control.name, control.type, br[control.name])

        # loop through all the options in any select (drop-down) controls
        if control.type == 'select' or control.type == 'checkbox':
            for item in control.items:
                print " - - - (value, labels) =", (str(item), [label.text  for label in item.get_labels()])

#--------------------------------------------------------------------------------------
# Next, let's submit the main form.
#--------------------------------------------------------------------------------------

# First, tell Mechanize which form to submit.
# If your form didn't have a CSS name attribute, use 'nr' instead 
# - e.g. br.select_form(nr=0) to find the first form on the page. 


def scrape_page(soup):
    #links = soup.findAll(href=re.compile('pdf$'))
    results = soup.findAll(attrs={'class' : 'scannableList'})
    print results
    record = {}
    for result in results:
        record['Index'] = index
        global index
        index = index + 1
        record['GAONumber'] = result.dd.a.text
        record['Title'] = result.dt.text
        m = re.search('&nbsp;&nbsp;(.*)', result.dd.text)
        record['PubDate'] = m.group(1)
        record['link'] = result.dd.a['href']
        print result.dt.text
        print result.dd.a.text
        print result.dd.text
        scraperwiki.datastore.save(["GAONumber","Index"],record)
    #does it for every page of search results

def scrape_and_look_for_next_link(base_url, soup):
    scrape_page(soup)
    next_link = soup.find(title="Next Page")
    print next_link
    if next_link:
        next_url = base_url + next_link['href']
        print next_url
        br.open(next_url)
        next_soup = BeautifulSoup(br.response().read())
        scrape_and_look_for_next_link(base_url, next_soup)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
br.select_form(name='docdblite_agency')

# Set the fields: here we're looking for grants by Arts Council England in London
br["date1_month"] = ["9"]
br["date1_year"] = ["2001"]
br["date2_month"] = ["12"]
br["date2_year"] = ["2010"]
br["agency[]"] = ["Department of Homeland Security"]

# and submit the form
br.submit()
soup = BeautifulSoup(br.response().read())

base_url = 'http://gao.gov/docsearch/'
starting_url = base_url + 'app_processform.php'
scrape_and_look_for_next_link(base_url, soup)
