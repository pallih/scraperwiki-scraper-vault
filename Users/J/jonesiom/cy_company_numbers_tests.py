###############################################################################
# CYPRUS TESTS
###############################################################################

# V1: 21 March 2011
# tested but incompatible with Firefox 3.6.15 and IE 9
# wow - online service delivered by IBM in Dec 2010 and part funded by EU is only compatible with IE 6, 7 and 8
# questions: login to https? apsx?

# V2: 28 March 2011
# tested with tutorial source code on aspx

import scraperwiki
import mechanize
import lxml.html

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("table#ProviderSearchResultsTable1_ProvidersGrid tr")
    for row in rows:
        record = {}
        table_cells = row.cssselect("td")
        if table_cells: 
            record['Clinician'] = table_cells[0].text
            record['Location'] = table_cells[1].text
            record['CurrentRecognitions'] = table_cells[2].text.rstrip('&nbsp;')
            # Finally, save the record to the datastore
            scraperwiki.datastore.save(["Clinician"], record)
        
# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(root):
    scrape_table(root)
    next_link = root.cssselect("a#ProviderSearchResultsTable1_NextLinkButton")
    if next_link:
        # find the page's form
        br.select_form(name='ctl00')
        br.form.set_all_readonly(False)
        # set the relevant ASP.NET fields, as required in the page's onSubmit function
        # Your .aspx page may not have these
        # Luckily we can ignore the __VIEWSTATE variable: mechanize handles this for us.
        br['__EVENTTARGET'] = 'ProviderSearchResultsTable1$NextLinkButton'
        br['__EVENTARGUMENT'] = ''
        br.submit()
        root = lxml.html.fromstring(br.response().read())
        scrape_and_look_for_next_link(root)

# ---------------------------------------------------------------------------
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

base_url = 'https://efiling.drcor.mcit.gov.cy/'
starting_url = base_url + 'DrcorPublic/SearchForm.aspx?lang=EN'
br = mechanize.Browser()
# Set the user-agent - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)')]
br.open(starting_url)
# simulate an 'onSubmit' JavaScript function as per click on a 'next' link
root = lxml.html.fromstring(br.response().read())
print lxml.html.tostring(root)
# scrape
scrape_and_look_for_next_link(root)

###############################################################################
# CYPRUS TESTS
###############################################################################

# V1: 21 March 2011
# tested but incompatible with Firefox 3.6.15 and IE 9
# wow - online service delivered by IBM in Dec 2010 and part funded by EU is only compatible with IE 6, 7 and 8
# questions: login to https? apsx?

# V2: 28 March 2011
# tested with tutorial source code on aspx

import scraperwiki
import mechanize
import lxml.html

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("table#ProviderSearchResultsTable1_ProvidersGrid tr")
    for row in rows:
        record = {}
        table_cells = row.cssselect("td")
        if table_cells: 
            record['Clinician'] = table_cells[0].text
            record['Location'] = table_cells[1].text
            record['CurrentRecognitions'] = table_cells[2].text.rstrip('&nbsp;')
            # Finally, save the record to the datastore
            scraperwiki.datastore.save(["Clinician"], record)
        
# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(root):
    scrape_table(root)
    next_link = root.cssselect("a#ProviderSearchResultsTable1_NextLinkButton")
    if next_link:
        # find the page's form
        br.select_form(name='ctl00')
        br.form.set_all_readonly(False)
        # set the relevant ASP.NET fields, as required in the page's onSubmit function
        # Your .aspx page may not have these
        # Luckily we can ignore the __VIEWSTATE variable: mechanize handles this for us.
        br['__EVENTTARGET'] = 'ProviderSearchResultsTable1$NextLinkButton'
        br['__EVENTARGUMENT'] = ''
        br.submit()
        root = lxml.html.fromstring(br.response().read())
        scrape_and_look_for_next_link(root)

# ---------------------------------------------------------------------------
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

base_url = 'https://efiling.drcor.mcit.gov.cy/'
starting_url = base_url + 'DrcorPublic/SearchForm.aspx?lang=EN'
br = mechanize.Browser()
# Set the user-agent - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)')]
br.open(starting_url)
# simulate an 'onSubmit' JavaScript function as per click on a 'next' link
root = lxml.html.fromstring(br.response().read())
print lxml.html.tostring(root)
# scrape
scrape_and_look_for_next_link(root)

