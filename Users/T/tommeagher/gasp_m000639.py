import scraperwiki
import lxml.html
import datetime
import time
gasp_helper = scraperwiki.utils.swimport("gasp_helper")
 
DEBUG = False
 
if not DEBUG:
    gasp_helper = scraperwiki.utils.swimport("gasp_helper")
else:
    import gasp_helper

# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/
 
# Config
gasp = gasp_helper.GaspHelper("MYAPIKEYHERE", "M000639")
 
def _get_html_dom(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)
 
 
# Scrape contact info for offices
def scrape_offices():
    print "Scraping offices"
    root = _get_html_dom("http://menendez.senate.gov/services/assistance/")

    officenames = ["dc","barrington","newark"]  # each div class has different name, so create an array of names
    for oname in officenames:
        for tr in root.cssselect("div[class='"+oname+"'] div[class='content']"):   # finds divs with class attributes equalling oname, finds content inside (which is the same across divs)
            print tr
            text = tr.text_content().strip() # text_content() gets text inside the div
            print "Office text: {0}".format(text)
            if not DEBUG:
                gasp.add_office(address=text, phone="")

def scrape_biography():
    print "Scraping bio"
    root = _get_html_dom("http://menendez.senate.gov/biography/")
    articles = root.cssselect("div#sam-main p")   
    articles = root.find_class("amend-textarea")
    bio_text = lxml.html.tostring(articles[0])
#    for article in articles:
#        print unicode(article.text)
    print bio_text
 #       if not DEBUG:
 #           gasp.add_biography(article.text)

    if not DEBUG:
        gasp.add_biography(bio_text)



def scrape_issues():
    print "Scraping Issues"
    root = _get_html_dom("http://menendez.senate.gov/issues/")
    issues = root.cssselect("div.issues-list")
    for ish in issues:
        title = ish.cssselect('h4')[0].text_content()
        content = lxml.html.tostring(ish.cssselect('div.abstract')[0])
        print title
        print content
        if not DEBUG:
            gasp.add_issue(title, content)

def scrape_press_release_page(url):
    """Scrape a single press release page adn store the result"""
    pr_dom = _get_html_dom(url)
    date = pr_dom.cssselect("div#copy h4.date")[0].text_content() # Raw date is fine
    print date
    title = pr_dom.cssselect("div#copy h1.title")[0].text_content()
    print title
    content_el = pr_dom.cssselect("div#copy div.content")[0]
    content = lxml.html.tostring(content_el)
    print content
    if not DEBUG:
        gasp.add_press_release(title, date, content, url=url)

def scrape_press_releases_month(getdate=datetime.date.today()):
    """Scrapes press releases for a particular month. We won't always want to scrape every month"""
    press_date_url = "http://www.scottbrown.senate.gov/public/index.cfm/pressreleases?MonthDisplay={month}&YearDisplay={year}".format(month=getdate.month, year=getdate.year)
    print "Scraping Press Releases from {0}".format(press_date_url)
    root = _get_html_dom(press_date_url)
    pr_links = root.cssselect("table.recordList td.recordListTitle a")
    for link in pr_links:
        print link.get('href')
        scrape_press_release_page(link.get('href'))
        time.sleep(0.125) # Just so we don't hit them too fast

def scrape_all_press_releases():
    """Scrape all press releases we can find"""
    print "Scrape all press releases"
    root = _get_html_dom("http://menendez.senate.gov/newsroom/press/")
    year_els = root.cssselect("select[name='YearDisplay'] > option")
    years = [int(y.get('value')) for y in year_els if y.get('value') != '0']
    years.sort()
    months = range(1,13)
    now = datetime.date.today()
    dates = [datetime.date(year=y,month=m, day=1) for y in years for m in months]
    # dates = [d for d in dates if d < now] # Go over again and remove dates in the future.
    print dates
    for d in dates:
        print "Getting releases for {0}".format(d)
        scrape_press_releases_month(d)
        
# Scott Brown does not appear to have an events page???
def scrape_events():
    """docstring for scrape_events"""
    pass
 
 
 
def scrape_social_media():
    """docstring for scrape_social_media"""
    root = _get_html_dom("http://menendez.senate.gov/")


    social = root.cssselect("ul.social-media")
    for sosh in social:
        title = sosh.cssselect('li')[0].text_content()
        content = lxml.html.tostring(sosh.cssselect('href')[0])
        print title
        print content
        if not DEBUG:
            gasp.add_facebook(facebook_url)



#    facebook_url = root.cssselect("li#facebook a").get('href')
#    print "Facebook: {0}".format(facebook_url)
#    if not DEBUG:
#        gasp.add_facebook(facebook_url)
#    twitter_url = root.cssselect("li#twitter a").get('href')
##    print "Twitter: {0}".format(twitter_url)
#    if not DEBUG:
#        gasp.add_facebook(twitter_url)
#    youtube_url = root.cssselect("li#youtube a").get('href')
#    print "Youtube: {0}".format(youtube_url)
#    if not DEBUG:
#        gasp.add_youtube(youtube_url)

# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded

scrape_biography() 
scrape_offices()
scrape_issues()
scrape_all_press_releases()
scrape_social_media()
 
 
#if not DEBUG: gasp.finish()import scraperwiki
import lxml.html
import datetime
import time
gasp_helper = scraperwiki.utils.swimport("gasp_helper")
 
DEBUG = False
 
if not DEBUG:
    gasp_helper = scraperwiki.utils.swimport("gasp_helper")
else:
    import gasp_helper

# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/
 
# Config
gasp = gasp_helper.GaspHelper("MYAPIKEYHERE", "M000639")
 
def _get_html_dom(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)
 
 
# Scrape contact info for offices
def scrape_offices():
    print "Scraping offices"
    root = _get_html_dom("http://menendez.senate.gov/services/assistance/")

    officenames = ["dc","barrington","newark"]  # each div class has different name, so create an array of names
    for oname in officenames:
        for tr in root.cssselect("div[class='"+oname+"'] div[class='content']"):   # finds divs with class attributes equalling oname, finds content inside (which is the same across divs)
            print tr
            text = tr.text_content().strip() # text_content() gets text inside the div
            print "Office text: {0}".format(text)
            if not DEBUG:
                gasp.add_office(address=text, phone="")

def scrape_biography():
    print "Scraping bio"
    root = _get_html_dom("http://menendez.senate.gov/biography/")
    articles = root.cssselect("div#sam-main p")   
    articles = root.find_class("amend-textarea")
    bio_text = lxml.html.tostring(articles[0])
#    for article in articles:
#        print unicode(article.text)
    print bio_text
 #       if not DEBUG:
 #           gasp.add_biography(article.text)

    if not DEBUG:
        gasp.add_biography(bio_text)



def scrape_issues():
    print "Scraping Issues"
    root = _get_html_dom("http://menendez.senate.gov/issues/")
    issues = root.cssselect("div.issues-list")
    for ish in issues:
        title = ish.cssselect('h4')[0].text_content()
        content = lxml.html.tostring(ish.cssselect('div.abstract')[0])
        print title
        print content
        if not DEBUG:
            gasp.add_issue(title, content)

def scrape_press_release_page(url):
    """Scrape a single press release page adn store the result"""
    pr_dom = _get_html_dom(url)
    date = pr_dom.cssselect("div#copy h4.date")[0].text_content() # Raw date is fine
    print date
    title = pr_dom.cssselect("div#copy h1.title")[0].text_content()
    print title
    content_el = pr_dom.cssselect("div#copy div.content")[0]
    content = lxml.html.tostring(content_el)
    print content
    if not DEBUG:
        gasp.add_press_release(title, date, content, url=url)

def scrape_press_releases_month(getdate=datetime.date.today()):
    """Scrapes press releases for a particular month. We won't always want to scrape every month"""
    press_date_url = "http://www.scottbrown.senate.gov/public/index.cfm/pressreleases?MonthDisplay={month}&YearDisplay={year}".format(month=getdate.month, year=getdate.year)
    print "Scraping Press Releases from {0}".format(press_date_url)
    root = _get_html_dom(press_date_url)
    pr_links = root.cssselect("table.recordList td.recordListTitle a")
    for link in pr_links:
        print link.get('href')
        scrape_press_release_page(link.get('href'))
        time.sleep(0.125) # Just so we don't hit them too fast

def scrape_all_press_releases():
    """Scrape all press releases we can find"""
    print "Scrape all press releases"
    root = _get_html_dom("http://menendez.senate.gov/newsroom/press/")
    year_els = root.cssselect("select[name='YearDisplay'] > option")
    years = [int(y.get('value')) for y in year_els if y.get('value') != '0']
    years.sort()
    months = range(1,13)
    now = datetime.date.today()
    dates = [datetime.date(year=y,month=m, day=1) for y in years for m in months]
    # dates = [d for d in dates if d < now] # Go over again and remove dates in the future.
    print dates
    for d in dates:
        print "Getting releases for {0}".format(d)
        scrape_press_releases_month(d)
        
# Scott Brown does not appear to have an events page???
def scrape_events():
    """docstring for scrape_events"""
    pass
 
 
 
def scrape_social_media():
    """docstring for scrape_social_media"""
    root = _get_html_dom("http://menendez.senate.gov/")


    social = root.cssselect("ul.social-media")
    for sosh in social:
        title = sosh.cssselect('li')[0].text_content()
        content = lxml.html.tostring(sosh.cssselect('href')[0])
        print title
        print content
        if not DEBUG:
            gasp.add_facebook(facebook_url)



#    facebook_url = root.cssselect("li#facebook a").get('href')
#    print "Facebook: {0}".format(facebook_url)
#    if not DEBUG:
#        gasp.add_facebook(facebook_url)
#    twitter_url = root.cssselect("li#twitter a").get('href')
##    print "Twitter: {0}".format(twitter_url)
#    if not DEBUG:
#        gasp.add_facebook(twitter_url)
#    youtube_url = root.cssselect("li#youtube a").get('href')
#    print "Youtube: {0}".format(youtube_url)
#    if not DEBUG:
#        gasp.add_youtube(youtube_url)

# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded

scrape_biography() 
scrape_offices()
scrape_issues()
scrape_all_press_releases()
scrape_social_media()
 
 
#if not DEBUG: gasp.finish()