###############################################################################
# START HERE: Scrape the HSBC/Nasdaq Dubai indices so you don't have to fuck
# around quite so much. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html
import mechanize
import re



# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("div#ILDataViewer1 tr")  # selects all <tr> blocks within <table class="data">
    id = 0
    for row in rows:
        # Set up our data record - we'll need it later
        indexval = {}
        table_cells = row.cssselect("td")
        if table_cells:
            id += 1
            indexval['ID'] = id
            indexval['Date'] = table_cells[0].text
            indexval['Total Return'] = table_cells[1].text
            indexval['Yield'] = table_cells[3].text
            indexval['Spread'] = table_cells[4].text
            # Print out the data we've gathered
            print indexval
            # Finally, save the index value to the datastore - 'ID' is our unique key
            scraperwiki.sqlite.save(['ID'], indexval)


# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    print "w00t"

    scrape_table(root)
    br = mechanize.Browser()
    # sometimes the server is sensitive to this information
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    response = br.open(starting_url)

    html = response.read()
    next_button = 'javascript:__doPostBack("DataViewer1$GridView1$ctl24$ctl01", '')'
    print next_button
    mnextlink = re.search(next_button,'')
    if mnextlink:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

    br.select_form(name='ctl00')
    br.form.set_all_readonly(False)
    br['__EVENTTARGET'] = 'DataViewer1$GridView1$ctl24$ctl01'
    br['__EVENTARGUMENT'] = ''
    response = br.submit()


# ---------------------------------------------------------------------------
# START HERE: Choose which of the HSBC/Nasdaq Dubai sukuk indices you want to scrape.
# ---------------------------------------------------------------------------

base_url = "http://www.nasdaqdubaihsbcindices.com/"
starting_url = urlparse.urljoin(base_url, "Indices.aspx?HSBCCode=HXSUXXX")
scrape_and_look_for_next_link(starting_url)###############################################################################
# START HERE: Scrape the HSBC/Nasdaq Dubai indices so you don't have to fuck
# around quite so much. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html
import mechanize
import re



# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("div#ILDataViewer1 tr")  # selects all <tr> blocks within <table class="data">
    id = 0
    for row in rows:
        # Set up our data record - we'll need it later
        indexval = {}
        table_cells = row.cssselect("td")
        if table_cells:
            id += 1
            indexval['ID'] = id
            indexval['Date'] = table_cells[0].text
            indexval['Total Return'] = table_cells[1].text
            indexval['Yield'] = table_cells[3].text
            indexval['Spread'] = table_cells[4].text
            # Print out the data we've gathered
            print indexval
            # Finally, save the index value to the datastore - 'ID' is our unique key
            scraperwiki.sqlite.save(['ID'], indexval)


# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    print "w00t"

    scrape_table(root)
    br = mechanize.Browser()
    # sometimes the server is sensitive to this information
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    response = br.open(starting_url)

    html = response.read()
    next_button = 'javascript:__doPostBack("DataViewer1$GridView1$ctl24$ctl01", '')'
    print next_button
    mnextlink = re.search(next_button,'')
    if mnextlink:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

    br.select_form(name='ctl00')
    br.form.set_all_readonly(False)
    br['__EVENTTARGET'] = 'DataViewer1$GridView1$ctl24$ctl01'
    br['__EVENTARGUMENT'] = ''
    response = br.submit()


# ---------------------------------------------------------------------------
# START HERE: Choose which of the HSBC/Nasdaq Dubai sukuk indices you want to scrape.
# ---------------------------------------------------------------------------

base_url = "http://www.nasdaqdubaihsbcindices.com/"
starting_url = urlparse.urljoin(base_url, "Indices.aspx?HSBCCode=HXSUXXX")
scrape_and_look_for_next_link(starting_url)###############################################################################
# START HERE: Scrape the HSBC/Nasdaq Dubai indices so you don't have to fuck
# around quite so much. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html
import mechanize
import re



# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("div#ILDataViewer1 tr")  # selects all <tr> blocks within <table class="data">
    id = 0
    for row in rows:
        # Set up our data record - we'll need it later
        indexval = {}
        table_cells = row.cssselect("td")
        if table_cells:
            id += 1
            indexval['ID'] = id
            indexval['Date'] = table_cells[0].text
            indexval['Total Return'] = table_cells[1].text
            indexval['Yield'] = table_cells[3].text
            indexval['Spread'] = table_cells[4].text
            # Print out the data we've gathered
            print indexval
            # Finally, save the index value to the datastore - 'ID' is our unique key
            scraperwiki.sqlite.save(['ID'], indexval)


# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    print "w00t"

    scrape_table(root)
    br = mechanize.Browser()
    # sometimes the server is sensitive to this information
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    response = br.open(starting_url)

    html = response.read()
    next_button = 'javascript:__doPostBack("DataViewer1$GridView1$ctl24$ctl01", '')'
    print next_button
    mnextlink = re.search(next_button,'')
    if mnextlink:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

    br.select_form(name='ctl00')
    br.form.set_all_readonly(False)
    br['__EVENTTARGET'] = 'DataViewer1$GridView1$ctl24$ctl01'
    br['__EVENTARGUMENT'] = ''
    response = br.submit()


# ---------------------------------------------------------------------------
# START HERE: Choose which of the HSBC/Nasdaq Dubai sukuk indices you want to scrape.
# ---------------------------------------------------------------------------

base_url = "http://www.nasdaqdubaihsbcindices.com/"
starting_url = urlparse.urljoin(base_url, "Indices.aspx?HSBCCode=HXSUXXX")
scrape_and_look_for_next_link(starting_url)