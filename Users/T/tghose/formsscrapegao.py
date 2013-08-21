# Blank Python
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
base_url = 'gao.gov' 
url = "http://gao.gov/browse/a-z/Department_of_Homeland_Security"
br = mechanize.Browser()
br.open(url)

# Go to the search within page.
soup = BeautifulSoup(br.response().read())
search_within_link = soup.find(id = 'whitelink')
print search_within_link
#url = base_url + search_within_link['href']
url = """http://gao.gov/browse/a-z/Department_of_Homeland_Security/custom?adv_begin_month=9&adv_begin_day=11&adv_begin_year=2001&adv_end_month=9&adv_end_day=11&adv_end_year=2011&all="""
print url
br.open(url)

# Go to the letter reports
#soup = BeautifulSoup(br.response().read())
#letter_report_li = soup.findAll(id='Letter_Report_tag')
#print letter_report_li
#br.open(url + letter_report_li.a['href'])

#index = 1

#--------------------------------------------------------------------------------------
# Loop through all the forms on the page, and print some information about each one.
# This should work with your own URL.
#--------------------------------------------------------------------------------------
for form in []: #br.forms():
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
    print 'scraping page'
    #links = soup.findAll(href=re.compile('pdf$'))
    results = soup.findAll(id='Products_tag')
    print results
    record = {}
    for result in results:
        #record['Index'] = index
        #global index
        #index = index + 1
        record['GAONumber'] = result.dd.a.text
        record['Title'] = result.dt.text
        m = re.search('&nbsp;&nbsp;(.*)', result.dd.text)
        record['PubDate'] = m.group(1)
        record['link'] = result.dd.a['href']
        print result.dt.text
        print result.dd.a.text
        print result.dd.text
        scraperwiki.datastore.save(["GAONumber"],record)
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

#br.select_form(name='docdblite_agency')

# Set the fields: here we're looking for either the agency or topic and a date range

#br["date1_month"] = ["9"]
#br["date1_year"] = ["2001"]
#br["date2_month"] = ["12"]
#br["date2_year"] = ["2010"]
#br["agency[]"] = ["Department of Homeland Security"]

# and submit the form
#br.submit()
#soup = BeautifulSoup(br.response().read())

base_url = 'gao.gov'
starting_url = base_url + '/browse/a-z/Department_of_Homeland_Security/custom?adv_begin_month=9&adv_begin_day=11&adv_begin_year=2001&adv_end_month=9&adv_end_day=11&adv_end_year=2011&all='
br.open(starting_url)
print starting_url
print br.response().read()
soup = BeautifulSoup(br.response().read())
scrape_and_look_for_next_link(base_url, soup)

