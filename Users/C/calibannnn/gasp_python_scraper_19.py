import scraperwiki

gasp_helper = scraperwiki.utils.swimport("gasp_helper")


# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/

import scraperwiki
import lxml.html
import datetime
import time
 
DEBUG = False
 
if not DEBUG:
    gasp_helper = scraperwiki.utils.swimport("gasp_helper")
else:
    import gasp_helper 
# Step 1) PLACE YOUR CONFIG LINE HERE
#         (it should look something like `gasp = gasp_helper.GaspHelper("your-api-key", "P000001")`)
gasp = gasp_helper.GaspHelper("8de2a31f83cf4546a61d9d5cc57e542e", "L000504")

# Step 2) Write Your Scraper Here
#         (refer to https://scraperwiki.com/scrapers/gasp_helper for documentation)
def _get_html_dom(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)

# Scrape contact info for offices -- this code is not yet working
#def scrape_offices():
#    print "Scraping offices"
#    root = _get_html_dom("http://lugar.senate.gov/contact/offices/")
#    officenames = ["evansville","fortwayne","indy","valparaiso","dc"]  # each div class has different name, so create an array of names
#    for oname in officenames:
#        for tr in root.cssselect("id[id='"+oname+"'] id[id='content']"):   # finds divs with class attributes equalling oname, finds content inside (which is the same across divs)
#            print tr
#            text = tr.text_content().strip() # text_content() gets text inside the div
#            print "Office text: {0}".format(text)
#            if not DEBUG:
#                gasp.add_office(address=text, phone="")
#            print lxml.html.tostring(text)

def scrape_biography():
    print "Scraping bio"
    root = _get_html_dom("http://lugar.senate.gov/bio/")
    content = root.get_element_by_id("content")
    print lxml.html.tostring(content)
    if not DEBUG:
        gasp.add_biography(bio_text)

#def scrape_issues():
#    print "Scraping Issues"
#    root = _get_html_dom("http://lugar.senate.gov/issues/")
#    link_tags = root.cssselect('ul:nth-child(10) li a')
#    for ish in link_tags:  
#        title = ish.cssselect("a")[0].text_content()   
#        print ish     
#        print title
#        urls = ish.cssselect('a')[0].get('href')
#        print urls     
#        issue_root = "http://lugar.senate.gov/%s" % urls
#        print issue_root
#        issue_content_paras = issue_root.cssselect("div#content")
#        print issue_content_paras
#        issue_content = lxml.html.tostring(issue_content_paras[0])
#        print issue_content
#        if not DEBUG:
#            gasp.add_issue(title, issue_content)

# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded
 
#scrape_offices()
scrape_biography()
#scrape_issues()
#scrape_all_press_releases()
#scrape_social_media()

 
if not DEBUG: gasp.finish()
import scraperwiki

gasp_helper = scraperwiki.utils.swimport("gasp_helper")


# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/

import scraperwiki
import lxml.html
import datetime
import time
 
DEBUG = False
 
if not DEBUG:
    gasp_helper = scraperwiki.utils.swimport("gasp_helper")
else:
    import gasp_helper 
# Step 1) PLACE YOUR CONFIG LINE HERE
#         (it should look something like `gasp = gasp_helper.GaspHelper("your-api-key", "P000001")`)
gasp = gasp_helper.GaspHelper("8de2a31f83cf4546a61d9d5cc57e542e", "L000504")

# Step 2) Write Your Scraper Here
#         (refer to https://scraperwiki.com/scrapers/gasp_helper for documentation)
def _get_html_dom(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)

# Scrape contact info for offices -- this code is not yet working
#def scrape_offices():
#    print "Scraping offices"
#    root = _get_html_dom("http://lugar.senate.gov/contact/offices/")
#    officenames = ["evansville","fortwayne","indy","valparaiso","dc"]  # each div class has different name, so create an array of names
#    for oname in officenames:
#        for tr in root.cssselect("id[id='"+oname+"'] id[id='content']"):   # finds divs with class attributes equalling oname, finds content inside (which is the same across divs)
#            print tr
#            text = tr.text_content().strip() # text_content() gets text inside the div
#            print "Office text: {0}".format(text)
#            if not DEBUG:
#                gasp.add_office(address=text, phone="")
#            print lxml.html.tostring(text)

def scrape_biography():
    print "Scraping bio"
    root = _get_html_dom("http://lugar.senate.gov/bio/")
    content = root.get_element_by_id("content")
    print lxml.html.tostring(content)
    if not DEBUG:
        gasp.add_biography(bio_text)

#def scrape_issues():
#    print "Scraping Issues"
#    root = _get_html_dom("http://lugar.senate.gov/issues/")
#    link_tags = root.cssselect('ul:nth-child(10) li a')
#    for ish in link_tags:  
#        title = ish.cssselect("a")[0].text_content()   
#        print ish     
#        print title
#        urls = ish.cssselect('a')[0].get('href')
#        print urls     
#        issue_root = "http://lugar.senate.gov/%s" % urls
#        print issue_root
#        issue_content_paras = issue_root.cssselect("div#content")
#        print issue_content_paras
#        issue_content = lxml.html.tostring(issue_content_paras[0])
#        print issue_content
#        if not DEBUG:
#            gasp.add_issue(title, issue_content)

# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded
 
#scrape_offices()
scrape_biography()
#scrape_issues()
#scrape_all_press_releases()
#scrape_social_media()

 
if not DEBUG: gasp.finish()
