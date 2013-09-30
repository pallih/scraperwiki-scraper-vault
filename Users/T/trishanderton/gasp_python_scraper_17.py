import scraperwiki
gasp_helper = scraperwiki.utils.swimport("gasp_helper")


# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/


# Step 1) PLACE YOUR CONFIG LINE HERE
#         (it should look something like `gasp = gasp_helper.GaspHelper("your-api-key", "P000001")`)

gasp = gasp_helper.GaspHelper("721dab355e47475da32b69d30b16c9cb", "G000570");

# Step 2) Write Your Scraper Here
#         (refer to https://scraperwiki.com/scrapers/gasp_helper for documentation)

import scraperwiki
import lxml.html
import datetime
import time
     
DEBUG = False
     
if not DEBUG:
    gasp_helper = scraperwiki.utils.swimport("gasp_helper")
else:
    import gasp_helper
     
     
    # This is a Python template for a Sunlight Labs Great American Scraper Project
    # http://services.sunlightlabs.com/gasp/legislators/
     
     
    # Config
gasp = gasp_helper.GaspHelper("721dab355e47475da32b69d30b16c9cb", "G000570")

def _get_html_dom(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)
    
def scrape_offices():
    print "Scraping Offices"
    root = _get_html_dom("https://guinta.house.gov/contact-me")
    offices = root.cssselect("div#office-locations-wrapper")
    addresses = offices[0].text_content()
    print addresses

def scrape_biography():
    print "Scraping bio"
    root = _get_html_dom("http://guinta.house.gov/about-me/full-biography")
    articles = root.find_class("field-name-body")
    for article in articles:
        print article
    bio_text = lxml.html.tostring(articles[0])
    print bio_text
    if not DEBUG:
        gasp.add_biography(bio_text)

def scrape_issues():
    print "Scraping Issues"
    root = _get_html_dom("http://guinta.house.gov/issues")
    issue = root.cssselect("div#left-nav li")
    print issues    
    for ish in issues:
        title = ish.cssselect("li")[0].text_content()
        contained_links = ish.cssselect('a')
        if len(contained_links)==0:
            continue
        issue_link = "http://guinta.house.gov/%s" % contained_links[0].get('href')
        print issue_link 
        issue_root = _get_html_dom(issue_link)
        issue_content_paras = issue_root.find_class("detail-page")
        issue_content = lxml.html.tostring(issue_content_paras[0])
        print title
        print issue_content
    if not DEBUG:
        gasp.add_issue(title, issue_content)

def scrape_all_press_releases():
    """Scrape all press releases we can find"""
    print "Scrape all press releases"
    root = _get_html_dom("https://guinta.house.gov/press-releases/")
    releases = root.cssselect("div#inner-content li")
    print releases
    for release in releases:
        release_title = releases.cssselect("a")[0].text_content()
    print release_title
    #for release in releases
        #title = release.cssselect('h4')[0].text_content()
    #print title

scrape_all_press_releases()

def scrape_social_media():
    """docstring for scrape_social_media"""
    root = _get_html_dom("http://www.guinta.house.gov")
    facebook_url = root.cssselect("div#stay-connected li.fb a")[0].get('href')
    print "Facebook: {0}".format(facebook_url)
    if not DEBUG:
        gasp.add_facebook(facebook_url)
    twitter_url = root.cssselect("div#stay-connected li.twitter a")[0].get('href')
    print "Twitter: {0}".format(twitter_url)
    if not DEBUG:
        gasp.add_facebook(twitter_url)
    youtube_url = root.cssselect("div#stay-connected li.youtube a")[0].get('href')
    print "Youtube: {0}".format(youtube_url)
    if not DEBUG:
        gasp.add_youtube(youtube_url)
    flickr_url = root.cssselect("div#stay-connected li.flickr a")[0].get('href')
    print "Flickr: {0}".format(youtube_url)
    if not DEBUG:
        gasp.add_flickr(flickr_url)
      
    # Step 3) Run Your Scraper
    # call gasp.finish() to let our server know your scraper succeeded
     
scrape_offices()
scrape_biography()
scrape_issues()
#scrape_all_press_releases()
scrape_social_media()     
     
if not DEBUG: gasp.finish()

# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded
gasp.finish()import scraperwiki
gasp_helper = scraperwiki.utils.swimport("gasp_helper")


# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/


# Step 1) PLACE YOUR CONFIG LINE HERE
#         (it should look something like `gasp = gasp_helper.GaspHelper("your-api-key", "P000001")`)

gasp = gasp_helper.GaspHelper("721dab355e47475da32b69d30b16c9cb", "G000570");

# Step 2) Write Your Scraper Here
#         (refer to https://scraperwiki.com/scrapers/gasp_helper for documentation)

import scraperwiki
import lxml.html
import datetime
import time
     
DEBUG = False
     
if not DEBUG:
    gasp_helper = scraperwiki.utils.swimport("gasp_helper")
else:
    import gasp_helper
     
     
    # This is a Python template for a Sunlight Labs Great American Scraper Project
    # http://services.sunlightlabs.com/gasp/legislators/
     
     
    # Config
gasp = gasp_helper.GaspHelper("721dab355e47475da32b69d30b16c9cb", "G000570")

def _get_html_dom(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)
    
def scrape_offices():
    print "Scraping Offices"
    root = _get_html_dom("https://guinta.house.gov/contact-me")
    offices = root.cssselect("div#office-locations-wrapper")
    addresses = offices[0].text_content()
    print addresses

def scrape_biography():
    print "Scraping bio"
    root = _get_html_dom("http://guinta.house.gov/about-me/full-biography")
    articles = root.find_class("field-name-body")
    for article in articles:
        print article
    bio_text = lxml.html.tostring(articles[0])
    print bio_text
    if not DEBUG:
        gasp.add_biography(bio_text)

def scrape_issues():
    print "Scraping Issues"
    root = _get_html_dom("http://guinta.house.gov/issues")
    issue = root.cssselect("div#left-nav li")
    print issues    
    for ish in issues:
        title = ish.cssselect("li")[0].text_content()
        contained_links = ish.cssselect('a')
        if len(contained_links)==0:
            continue
        issue_link = "http://guinta.house.gov/%s" % contained_links[0].get('href')
        print issue_link 
        issue_root = _get_html_dom(issue_link)
        issue_content_paras = issue_root.find_class("detail-page")
        issue_content = lxml.html.tostring(issue_content_paras[0])
        print title
        print issue_content
    if not DEBUG:
        gasp.add_issue(title, issue_content)

def scrape_all_press_releases():
    """Scrape all press releases we can find"""
    print "Scrape all press releases"
    root = _get_html_dom("https://guinta.house.gov/press-releases/")
    releases = root.cssselect("div#inner-content li")
    print releases
    for release in releases:
        release_title = releases.cssselect("a")[0].text_content()
    print release_title
    #for release in releases
        #title = release.cssselect('h4')[0].text_content()
    #print title

scrape_all_press_releases()

def scrape_social_media():
    """docstring for scrape_social_media"""
    root = _get_html_dom("http://www.guinta.house.gov")
    facebook_url = root.cssselect("div#stay-connected li.fb a")[0].get('href')
    print "Facebook: {0}".format(facebook_url)
    if not DEBUG:
        gasp.add_facebook(facebook_url)
    twitter_url = root.cssselect("div#stay-connected li.twitter a")[0].get('href')
    print "Twitter: {0}".format(twitter_url)
    if not DEBUG:
        gasp.add_facebook(twitter_url)
    youtube_url = root.cssselect("div#stay-connected li.youtube a")[0].get('href')
    print "Youtube: {0}".format(youtube_url)
    if not DEBUG:
        gasp.add_youtube(youtube_url)
    flickr_url = root.cssselect("div#stay-connected li.flickr a")[0].get('href')
    print "Flickr: {0}".format(youtube_url)
    if not DEBUG:
        gasp.add_flickr(flickr_url)
      
    # Step 3) Run Your Scraper
    # call gasp.finish() to let our server know your scraper succeeded
     
scrape_offices()
scrape_biography()
scrape_issues()
#scrape_all_press_releases()
scrape_social_media()     
     
if not DEBUG: gasp.finish()

# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded
gasp.finish()