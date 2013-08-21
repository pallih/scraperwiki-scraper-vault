import scraperwiki
from BeautifulSoup import BeautifulSoup
import urllib2
from time import sleep

gasp_helper = scraperwiki.utils.swimport("gasp_helper")


# This is a Python template for a Sunlight Labs Great American Scraper Project
# http://services.sunlightlabs.com/gasp/legislators/


# Step 1) PLACE YOUR CONFIG LINE HERE
#         (it should look something like `gasp = gasp_helper.GaspHelper("your-api-key", "P000001")`)


# So it'll run with a fake api key -
gasp = gasp_helper.GaspHelper("YOUR_SUNLIGHT_KEY", "F000043")

# Step 2) Write Your Scraper Here
#         (refer to https://scraperwiki.com/scrapers/gasp_helper for documentation)




## News releases live here: http://fattah.house.gov/index.cfm?sectionid=34&itemid=10

## Full text of release is within this <div class="item" id="itemid_97"> but replace 97 with the actual itemid

## Text start within item: <div class="contentdata"><p>FOR IMMEDIATE RELEASE<br />

## section front has the most itemid--i.e. max: http://fattah.house.gov/index.cfm?sectionid=34


## News release time stamp is within this span: <span class="contentdate">01/17/07</span>


## test on known news releases: 100-110

for news_release_id in range(100,110):
    news_release_url = "http://fattah.house.gov/index.cfm?sectionid=34&itemid=%s" % news_release_id
    news_page = urllib2.urlopen(news_release_url).read()
    print "Got page %s" % (news_release_url)
    print "page: %s" % (news_page)
    soup = BeautifulSoup(news_page)
    div_name = "itemid_%s" % (news_release_id)
    # we're allowing markup in the fields, right?
    release_text = soup('div', id=div_name)
    release_date = soup('span', attrs={"class" : "contentdate"})
    

    
    # sleep(1)


# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded
#gasp.finish()




