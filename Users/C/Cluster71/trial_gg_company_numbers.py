# Scrape Guernsey company data

from BeautifulSoup import BeautifulSoup as Soup
import mechanize, re, string, sys, scraperwiki

search_chars = string.ascii_lowercase + string.digits + """ .+-*(&+/*!"""
url = "https://www.greg.gg/webCompSearch.aspx"
form_id = "aspnetForm"
search_field = "ctl00$cntPortal$txtCompName"
search_form_id = "ctl00_cntPortal_btnSearch"
results_id = "ctl00_cntPortal_grdSearchResults"
page_select = "ctl00$cntPortal$grdSearchResults$ctl13$ddlPages"

browser = mechanize.Browser()
browser.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)')]
browser.open(url)


# Scrape the table with company details, return the BeatifulSoup instance
def scrape_results(html):
    soup = Soup(html, convertEntities=Soup.HTML_ENTITIES)
    container = soup.find("table", id=results_id)

    if container == None:
        return soup

    rows = container.findAll("tr", {"class": re.compile("^(grid|grid_alt)$")})
    for row in rows:
        view, registry, reg_num, name, is_current_name, company_type, status = row.findAll("td")

        data = {
            "CompanyName": name.text, 
            "CompanyNumber": reg_num.text, 
            "Status": status.text, 
            "EntityType": company_type.text, 
        }

        scraperwiki.sqlite.save(["CompanyNumber"], data)

    return soup


# Uses the <select> of the results pager to read the next page of results
def scrape_next_results(page_num):
    browser.select_form(form_id)
    browser.form.set_all_readonly(False)
    browser.form['__EVENTTARGET'] = page_select
    browser.form[page_select] = [str(page_num)]

    response = browser.submit()
    scrape_results(response.get_data())
    browser.back()

# Post the search form
def scrape_search(prefix):    
    browser.select_form(form_id)
    browser.form.set_all_readonly(False)
    browser.form[search_field] = prefix
    response = browser.submit(id=search_form_id)
    soup = scrape_results(response.get_data())

    pager = soup.find('select', {"name":page_select})
    if pager != None:
        num_pages = len(pager.findAll("option"))
        
        for page_num in range(2, num_pages + 1):
            scrape_next_results(page_num)

    browser.back()


#Generate all permutations, with repetition, can start from any possible permutation.
def permutations_from(chrs, num, start=False):
    if start == False:
        index = 0
    else:
        index = chrs.index(start[0])

    if num <= 1:
        for c in chrs[index:]:
            yield c
    else:
        for c in chrs[index:]:
            for p in permutations_from(chrs, num - 1, start[1:] if start and c == start[0] else False):
                yield c + p


first_prefix = scraperwiki.sqlite.get_var('search_from', False)

if first_prefix:
    print "Resuming scrape from '%s'" % first_prefix
else:
    print "Starting new scrape"
    

# Start the scraping...
for prefix in permutations_from(search_chars, 2, first_prefix):
    scraperwiki.sqlite.save_var('search_from', prefix)
    try:
        scrape_search(prefix)
    except Exception, e:
        #Scaper can resume ok so let scraper die silently when vm times out
        if "CPU time exceeded" in e.args[0]:
            sys.exit()
        else:
            raise e

scraperwiki.sqlite.save_var('search_from', False)
# Scrape Guernsey company data

from BeautifulSoup import BeautifulSoup as Soup
import mechanize, re, string, sys, scraperwiki

search_chars = string.ascii_lowercase + string.digits + """ .+-*(&+/*!"""
url = "https://www.greg.gg/webCompSearch.aspx"
form_id = "aspnetForm"
search_field = "ctl00$cntPortal$txtCompName"
search_form_id = "ctl00_cntPortal_btnSearch"
results_id = "ctl00_cntPortal_grdSearchResults"
page_select = "ctl00$cntPortal$grdSearchResults$ctl13$ddlPages"

browser = mechanize.Browser()
browser.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)')]
browser.open(url)


# Scrape the table with company details, return the BeatifulSoup instance
def scrape_results(html):
    soup = Soup(html, convertEntities=Soup.HTML_ENTITIES)
    container = soup.find("table", id=results_id)

    if container == None:
        return soup

    rows = container.findAll("tr", {"class": re.compile("^(grid|grid_alt)$")})
    for row in rows:
        view, registry, reg_num, name, is_current_name, company_type, status = row.findAll("td")

        data = {
            "CompanyName": name.text, 
            "CompanyNumber": reg_num.text, 
            "Status": status.text, 
            "EntityType": company_type.text, 
        }

        scraperwiki.sqlite.save(["CompanyNumber"], data)

    return soup


# Uses the <select> of the results pager to read the next page of results
def scrape_next_results(page_num):
    browser.select_form(form_id)
    browser.form.set_all_readonly(False)
    browser.form['__EVENTTARGET'] = page_select
    browser.form[page_select] = [str(page_num)]

    response = browser.submit()
    scrape_results(response.get_data())
    browser.back()

# Post the search form
def scrape_search(prefix):    
    browser.select_form(form_id)
    browser.form.set_all_readonly(False)
    browser.form[search_field] = prefix
    response = browser.submit(id=search_form_id)
    soup = scrape_results(response.get_data())

    pager = soup.find('select', {"name":page_select})
    if pager != None:
        num_pages = len(pager.findAll("option"))
        
        for page_num in range(2, num_pages + 1):
            scrape_next_results(page_num)

    browser.back()


#Generate all permutations, with repetition, can start from any possible permutation.
def permutations_from(chrs, num, start=False):
    if start == False:
        index = 0
    else:
        index = chrs.index(start[0])

    if num <= 1:
        for c in chrs[index:]:
            yield c
    else:
        for c in chrs[index:]:
            for p in permutations_from(chrs, num - 1, start[1:] if start and c == start[0] else False):
                yield c + p


first_prefix = scraperwiki.sqlite.get_var('search_from', False)

if first_prefix:
    print "Resuming scrape from '%s'" % first_prefix
else:
    print "Starting new scrape"
    

# Start the scraping...
for prefix in permutations_from(search_chars, 2, first_prefix):
    scraperwiki.sqlite.save_var('search_from', prefix)
    try:
        scrape_search(prefix)
    except Exception, e:
        #Scaper can resume ok so let scraper die silently when vm times out
        if "CPU time exceeded" in e.args[0]:
            sys.exit()
        else:
            raise e

scraperwiki.sqlite.save_var('search_from', False)
