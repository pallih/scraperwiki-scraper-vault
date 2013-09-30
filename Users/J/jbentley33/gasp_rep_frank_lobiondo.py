# This is my first try at using scraperwiki and python
# A majority of this code is from Sunlight Labs
# http://services.sunlightlabs.com/gasp/examples/
# I still need to add some comments

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
gasp = gasp_helper.GaspHelper("ab4686629daa4f80b6b1559eaa7eee4b", "L000554")
 
def _get_html_dom(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)
 
 
# Scrape contact info for offices
def scrape_offices():
    print "Scraping offices"
    root = _get_html_dom("http://lobiondo.house.gov/office/mays-landing-office")
    for office in range(2):
        addr_text = root.cssselect("div.address")[office].text_content()
        city_text = root.cssselect("div.city")[office].text_content()
        full_addr = addr_text + " " + city_text
        phone_text = root.cssselect("div.phone")[office].text_content()
        fax_text = root.cssselect("div.fax")[office].text_content()
        if not DEBUG:
            gasp.add_office(address=full_addr, phone=phone_text, fax=fax_text)


# Scrape biography info
def scrape_biography():
    print "Scraping bio"
    root = _get_html_dom("http://lobiondo.house.gov/about-me/full-biography")
    officenames = ["div#inner-content"]  # each div class has different name, so create an array of names
    for oname in officenames:
        tr2 = root.cssselect(oname)[0]  # finds divs with class attributes equalling oname, finds content inside (which is the same across divs)
        bio_text = tr2.text_content().strip() # text_content() gets text inside the div
        if not DEBUG:
            gasp.add_biography(bio_text)



# Frank Lobiondo does not appear to have an issues page
def scrape_issues():
    """docstring for scrape_events"""
    pass



def scrape_press_release_page(url, title, date):
    """Scrape a single press release page adn store the result"""
    pr_dom = "http://lobiondo.house.gov"
    pr_dom2 = pr_dom + url
    pr_dom3 = _get_html_dom(pr_dom2)
         
    for pr_con in pr_dom3.cssselect('div.field-item'):
        if not DEBUG:
            gasp.add_press_release(title, date, pr_con.text_content(), url=pr_dom2)


#This is only pulling the press releases from the first page
def scrape_all_press_releases():
    """Scrape all press releases we can find"""
    print "Scrape all press releases"
    root = _get_html_dom("http://lobiondo.house.gov/press-releases")
    
    for link in range(10):
        pr_link = root.cssselect('div.list-item a')[link].get('href')
        pr_text = root.cssselect('div.list-item a')[link].text_content()
        pr_date = root.cssselect('div.date-tag')[link].text_content()
        scrape_press_release_page(pr_link, pr_text, pr_date)
        time.sleep(1) # Just so we don't hit them too fast


        
# The events section didn't have a tutorial so that will be left till the rest is working
def scrape_events(url):
    """Scrape a single press release page adn store the result"""
    ev_dom = "http://lobiondo.house.gov"
    ev_dom2 = ev_dom + url
    ev_dom3 = _get_html_dom(ev_dom2)
         

#   ev_tle = root.cssselect('div.list-item a')[link].text_content()
#   print ev_tle
    ev_date = ev_dom3.cssselect("span.event-date")[0].text_content()
    print ev_date
    ev_loc = ev_dom3.cssselect("span.event-date")[2].text_content()
    print ev_loc
#        if not DEBUG:
#            gasp.add_event(ev_tle, ev_date, ev_loc, ev_con, url=ev_dom2)     

def scrape_all_events():
    """docstring for scrape_events"""
    print "Scrape all events"
    root = _get_html_dom("http://lobiondo.house.gov/events/archive")
    
    for link in range(10):
        ev_link = root.cssselect('div.list-item a')[link].get('href')
        scrape_events(ev_link)
        time.sleep(1) # Just so we don't hit them too fast




def scrape_social_media():
    """docstring for scrape_social_media"""
    root = _get_html_dom("http://lobiondo.house.gov/media-center/social-media")
    facebook_url = root.cssselect("div#inner-content a")[0].get('href')
    if not DEBUG:
        gasp.add_facebook(facebook_url)
    twitter_url = root.cssselect("div#inner-content a")[2].get('href')
    if not DEBUG:
        gasp.add_twitter(twitter_url)
    youtube_url = root.cssselect("div#inner-content a")[1].get('href')
    if not DEBUG:
        gasp.add_youtube(youtube_url)
    flickr_url = root.cssselect("div#inner-content a")[3].get('href')
    if not DEBUG:
        gasp.add_flickr(flickr_url)



# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded
 
scrape_offices()
scrape_biography()
#scrape_all_events()  #Rep. Lobiondo's events page in not uniform so I need to tweak it some
scrape_all_press_releases()
scrape_social_media()
 
 
if not DEBUG: gasp.finish()# This is my first try at using scraperwiki and python
# A majority of this code is from Sunlight Labs
# http://services.sunlightlabs.com/gasp/examples/
# I still need to add some comments

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
gasp = gasp_helper.GaspHelper("ab4686629daa4f80b6b1559eaa7eee4b", "L000554")
 
def _get_html_dom(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)
 
 
# Scrape contact info for offices
def scrape_offices():
    print "Scraping offices"
    root = _get_html_dom("http://lobiondo.house.gov/office/mays-landing-office")
    for office in range(2):
        addr_text = root.cssselect("div.address")[office].text_content()
        city_text = root.cssselect("div.city")[office].text_content()
        full_addr = addr_text + " " + city_text
        phone_text = root.cssselect("div.phone")[office].text_content()
        fax_text = root.cssselect("div.fax")[office].text_content()
        if not DEBUG:
            gasp.add_office(address=full_addr, phone=phone_text, fax=fax_text)


# Scrape biography info
def scrape_biography():
    print "Scraping bio"
    root = _get_html_dom("http://lobiondo.house.gov/about-me/full-biography")
    officenames = ["div#inner-content"]  # each div class has different name, so create an array of names
    for oname in officenames:
        tr2 = root.cssselect(oname)[0]  # finds divs with class attributes equalling oname, finds content inside (which is the same across divs)
        bio_text = tr2.text_content().strip() # text_content() gets text inside the div
        if not DEBUG:
            gasp.add_biography(bio_text)



# Frank Lobiondo does not appear to have an issues page
def scrape_issues():
    """docstring for scrape_events"""
    pass



def scrape_press_release_page(url, title, date):
    """Scrape a single press release page adn store the result"""
    pr_dom = "http://lobiondo.house.gov"
    pr_dom2 = pr_dom + url
    pr_dom3 = _get_html_dom(pr_dom2)
         
    for pr_con in pr_dom3.cssselect('div.field-item'):
        if not DEBUG:
            gasp.add_press_release(title, date, pr_con.text_content(), url=pr_dom2)


#This is only pulling the press releases from the first page
def scrape_all_press_releases():
    """Scrape all press releases we can find"""
    print "Scrape all press releases"
    root = _get_html_dom("http://lobiondo.house.gov/press-releases")
    
    for link in range(10):
        pr_link = root.cssselect('div.list-item a')[link].get('href')
        pr_text = root.cssselect('div.list-item a')[link].text_content()
        pr_date = root.cssselect('div.date-tag')[link].text_content()
        scrape_press_release_page(pr_link, pr_text, pr_date)
        time.sleep(1) # Just so we don't hit them too fast


        
# The events section didn't have a tutorial so that will be left till the rest is working
def scrape_events(url):
    """Scrape a single press release page adn store the result"""
    ev_dom = "http://lobiondo.house.gov"
    ev_dom2 = ev_dom + url
    ev_dom3 = _get_html_dom(ev_dom2)
         

#   ev_tle = root.cssselect('div.list-item a')[link].text_content()
#   print ev_tle
    ev_date = ev_dom3.cssselect("span.event-date")[0].text_content()
    print ev_date
    ev_loc = ev_dom3.cssselect("span.event-date")[2].text_content()
    print ev_loc
#        if not DEBUG:
#            gasp.add_event(ev_tle, ev_date, ev_loc, ev_con, url=ev_dom2)     

def scrape_all_events():
    """docstring for scrape_events"""
    print "Scrape all events"
    root = _get_html_dom("http://lobiondo.house.gov/events/archive")
    
    for link in range(10):
        ev_link = root.cssselect('div.list-item a')[link].get('href')
        scrape_events(ev_link)
        time.sleep(1) # Just so we don't hit them too fast




def scrape_social_media():
    """docstring for scrape_social_media"""
    root = _get_html_dom("http://lobiondo.house.gov/media-center/social-media")
    facebook_url = root.cssselect("div#inner-content a")[0].get('href')
    if not DEBUG:
        gasp.add_facebook(facebook_url)
    twitter_url = root.cssselect("div#inner-content a")[2].get('href')
    if not DEBUG:
        gasp.add_twitter(twitter_url)
    youtube_url = root.cssselect("div#inner-content a")[1].get('href')
    if not DEBUG:
        gasp.add_youtube(youtube_url)
    flickr_url = root.cssselect("div#inner-content a")[3].get('href')
    if not DEBUG:
        gasp.add_flickr(flickr_url)



# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded
 
scrape_offices()
scrape_biography()
#scrape_all_events()  #Rep. Lobiondo's events page in not uniform so I need to tweak it some
scrape_all_press_releases()
scrape_social_media()
 
 
if not DEBUG: gasp.finish()