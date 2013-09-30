import scraperwiki
import lxml.html
import mechanize
import re
import urlparse
import string
import time


base_url = 'http://data.fingal.ie/default.aspx'
#base_url = 'http://data.fingal.ie/details.aspx?datasetID=363'

##
# -----------------------------------------------------------------------------
# We need these lines to handle ASPX pages.  Gives you more reason to hate
# ASPX pages and the people that invented them.
# -----------------------------------------------------------------------------
browzer = mechanize.Browser()
browzer.addheaders = [('User-agent', 'Chrome/11.0.696.68 Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
rezzie = browzer.open(base_url)

# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <td> 
#    and <td> tags.  This part will get all the details of the dataset.
# -----------------------------------------------------------------------------

def scrape_metadata(url, record):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for p in root.cssselect('div #contentDetails p'):
        field = p.cssselect('b')
        if field and str(field[0].text).strip("\r\n ") == "Created:":
            record['Created'] = p.text_content().split(":")[1].strip("\r\n ")
        elif field and str(field[0].text).strip("\r\n ") == "Categories:":
            record['Categories'] = p.text_content().split(":")[1].strip("\r\n ")

    for tr in root.cssselect('table.dataset tr'):
        th = tr.cssselect('th')
        #print th[0].text
        name = th[0].text
        td = tr.cssselect('td')
        link = tr.cssselect('a')
        if len(link):
            #print link[0].text
            if str(link[0].text).strip("\r\n ").startswith('/'):
                #print base_url.rstrip('/') + str(link[0].text).strip("\r\n ")
                record[''+str(name).strip("\r\n ")] = base_url.rstrip('/') + str(link[0].text).strip("\r\n ")
            elif str(link[0].text).strip("\r\n ").startswith("\\"):
                #print base_url.rstrip('/') + str(link[0].text).strip("\r\n ").replace("\\", '/')
                record[''+str(name).strip("\r\n ")] = base_url.rstrip('/') + str(link[0].text).strip("\r\n ").replace("\\", '/')
            else:
                str(link[0].text).strip("\r\n ")
                record[''+str(name).strip("\r\n ")] = str(link[0].text).strip("\r\n ")
        else:
            #print td[0].text
            record[''+str(name).strip("\r\n ")] = str(td[0].text).strip("\r\n ")
    scraperwiki.sqlite.save(["Dataset_Title"], record) #store in record in db after each dataset

# ------------------------------------------------------------------------------
# 2. Parse the raw HTML to get the interesting bits - the part inside <td> <h2> 
#    and <a> tags.  We have to get the title and the description of each dataset
#    as well as the link to the dataset page
# ------------------------------------------------------------------------------
def scrape_page(root):
    record = {}
    for td in root.cssselect('td'):
        title = td.cssselect('h2 a')
        if title:
            #print "Title = %s" % title[0].text
            record['Dataset_Title'] = str(title[0].text).strip("\r\n ")
            next_link = title[0].attrib.get('href')
            desc = td.cssselect('p')
            #print "Description = %s" % desc[0].text
            record['Description'] = str(desc[0].text).strip("\r\n ")
            
            if next_link:#get link
                next_url = urlparse.urljoin(base_url, next_link)
                #print next_url
                record['URL'] = next_url
                scrape_metadata(next_url, record) #call secondary function to scrape metadata in the next page


# -----------------------------------------------------------------------------
# 3. Iterate through the next link.
# 
# -----------------------------------------------------------------------------

def scrape_and_look_for_next_link(rezzie):
    
    # Follows refresh 0 but not hangs on refresh > 0
    browzer.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    #page += 1
    page = 1
    for page in range(3):
        html = rezzie.read()
        root = lxml.html.fromstring(html)
        print "Scraping page %d" % page
        print html
        #scrape_page(root)
        print "page length %d" % (len(html))
        next_url = re.search("javascript:__doPostBack\(&#39;lnkNext&#39;,&#39;&#39;\).>Next >>", html) 
        print "Getting next page."
        print next_url
        if not next_url:
            break
    #for page in (1,4):
        browzer.select_form(nr=0)
        browzer.form.set_all_readonly(False)
        browzer['__EVENTTARGET'] = 'lnkNext'
        browzer['__EVENTARGUMENT'] = ''
        rezzie = browzer.submit()
        print rezzie.info()
        print browzer.response().read()
        #scrape_and_look_for_next_link(rezzie, page)
        
# -----------------------------------------------------------------------------
# 4. Get data from DB and Display.
# 
# -----------------------------------------------------------------------------
def display_table():
    # connect to the source database giving it the name src
    #scraperwiki.sqlite.attach(sourcescraper, "src")
    

    # the default table in most scrapers is called swdata
    sdata = scraperwiki.sqlite.execute("select * from swdata")
    print sdata
    keys = sdata.get("keys")
    print keys
    rows = sdata.get("data")
    print rows
    ctr = 0

    print '<h2>Metadata from %s Datasets</h2>' % base_url
    print '<table border="1" style="border-collapse:collapse;">'

    # column headings
    print "<tr>",
    print "<th>#</th>",
    for key in keys:
        print "<th>%s</th>" % key,
    print "</tr>"

    # rows
    for row in rows:
        print "<tr>",
        print "<td>%d</td>" % ctr,
        for value in row:
            print "<td>%s</td>" % value,
        print "</tr>"
        ctr += 1
    print "</table>"


##
scrape_and_look_for_next_link(rezzie)
#display_table()


import scraperwiki
import lxml.html
import mechanize
import re
import urlparse
import string
import time


base_url = 'http://data.fingal.ie/default.aspx'
#base_url = 'http://data.fingal.ie/details.aspx?datasetID=363'

##
# -----------------------------------------------------------------------------
# We need these lines to handle ASPX pages.  Gives you more reason to hate
# ASPX pages and the people that invented them.
# -----------------------------------------------------------------------------
browzer = mechanize.Browser()
browzer.addheaders = [('User-agent', 'Chrome/11.0.696.68 Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
rezzie = browzer.open(base_url)

# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <td> 
#    and <td> tags.  This part will get all the details of the dataset.
# -----------------------------------------------------------------------------

def scrape_metadata(url, record):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for p in root.cssselect('div #contentDetails p'):
        field = p.cssselect('b')
        if field and str(field[0].text).strip("\r\n ") == "Created:":
            record['Created'] = p.text_content().split(":")[1].strip("\r\n ")
        elif field and str(field[0].text).strip("\r\n ") == "Categories:":
            record['Categories'] = p.text_content().split(":")[1].strip("\r\n ")

    for tr in root.cssselect('table.dataset tr'):
        th = tr.cssselect('th')
        #print th[0].text
        name = th[0].text
        td = tr.cssselect('td')
        link = tr.cssselect('a')
        if len(link):
            #print link[0].text
            if str(link[0].text).strip("\r\n ").startswith('/'):
                #print base_url.rstrip('/') + str(link[0].text).strip("\r\n ")
                record[''+str(name).strip("\r\n ")] = base_url.rstrip('/') + str(link[0].text).strip("\r\n ")
            elif str(link[0].text).strip("\r\n ").startswith("\\"):
                #print base_url.rstrip('/') + str(link[0].text).strip("\r\n ").replace("\\", '/')
                record[''+str(name).strip("\r\n ")] = base_url.rstrip('/') + str(link[0].text).strip("\r\n ").replace("\\", '/')
            else:
                str(link[0].text).strip("\r\n ")
                record[''+str(name).strip("\r\n ")] = str(link[0].text).strip("\r\n ")
        else:
            #print td[0].text
            record[''+str(name).strip("\r\n ")] = str(td[0].text).strip("\r\n ")
    scraperwiki.sqlite.save(["Dataset_Title"], record) #store in record in db after each dataset

# ------------------------------------------------------------------------------
# 2. Parse the raw HTML to get the interesting bits - the part inside <td> <h2> 
#    and <a> tags.  We have to get the title and the description of each dataset
#    as well as the link to the dataset page
# ------------------------------------------------------------------------------
def scrape_page(root):
    record = {}
    for td in root.cssselect('td'):
        title = td.cssselect('h2 a')
        if title:
            #print "Title = %s" % title[0].text
            record['Dataset_Title'] = str(title[0].text).strip("\r\n ")
            next_link = title[0].attrib.get('href')
            desc = td.cssselect('p')
            #print "Description = %s" % desc[0].text
            record['Description'] = str(desc[0].text).strip("\r\n ")
            
            if next_link:#get link
                next_url = urlparse.urljoin(base_url, next_link)
                #print next_url
                record['URL'] = next_url
                scrape_metadata(next_url, record) #call secondary function to scrape metadata in the next page


# -----------------------------------------------------------------------------
# 3. Iterate through the next link.
# 
# -----------------------------------------------------------------------------

def scrape_and_look_for_next_link(rezzie):
    
    # Follows refresh 0 but not hangs on refresh > 0
    browzer.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    #page += 1
    page = 1
    for page in range(3):
        html = rezzie.read()
        root = lxml.html.fromstring(html)
        print "Scraping page %d" % page
        print html
        #scrape_page(root)
        print "page length %d" % (len(html))
        next_url = re.search("javascript:__doPostBack\(&#39;lnkNext&#39;,&#39;&#39;\).>Next >>", html) 
        print "Getting next page."
        print next_url
        if not next_url:
            break
    #for page in (1,4):
        browzer.select_form(nr=0)
        browzer.form.set_all_readonly(False)
        browzer['__EVENTTARGET'] = 'lnkNext'
        browzer['__EVENTARGUMENT'] = ''
        rezzie = browzer.submit()
        print rezzie.info()
        print browzer.response().read()
        #scrape_and_look_for_next_link(rezzie, page)
        
# -----------------------------------------------------------------------------
# 4. Get data from DB and Display.
# 
# -----------------------------------------------------------------------------
def display_table():
    # connect to the source database giving it the name src
    #scraperwiki.sqlite.attach(sourcescraper, "src")
    

    # the default table in most scrapers is called swdata
    sdata = scraperwiki.sqlite.execute("select * from swdata")
    print sdata
    keys = sdata.get("keys")
    print keys
    rows = sdata.get("data")
    print rows
    ctr = 0

    print '<h2>Metadata from %s Datasets</h2>' % base_url
    print '<table border="1" style="border-collapse:collapse;">'

    # column headings
    print "<tr>",
    print "<th>#</th>",
    for key in keys:
        print "<th>%s</th>" % key,
    print "</tr>"

    # rows
    for row in rows:
        print "<tr>",
        print "<td>%d</td>" % ctr,
        for value in row:
            print "<td>%s</td>" % value,
        print "</tr>"
        ctr += 1
    print "</table>"


##
scrape_and_look_for_next_link(rezzie)
#display_table()


