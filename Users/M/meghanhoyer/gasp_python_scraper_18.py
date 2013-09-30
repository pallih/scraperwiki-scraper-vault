import lxml.html
import scraperwiki
gasp_helper = scraperwiki.utils.swimport("gasp_helper")


# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/


# Step 1) PLACE YOUR CONFIG LINE HERE
#         (it should look something like `gasp = gasp_helper.GaspHelper("your-api-key", "P000001")`)
gasp = gasp_helper.GaspHelper("67ed2d7ecd144c2bb8d3622113bdba86", "W000805")


# Step 2) Write Your Scraper Here
#         (refer to https://scraperwiki.com/scrapers/gasp_helper for documentation)
bio_html = scraperwiki.scrape('http://www.warner.senate.gov/public/index.cfm/biography')
bio_doc = lxml.html.fromstring(bio_html)
bio_text = bio_doc.xpath('//div[@class="article"]')[0].text_content()

gasp.add_biography(bio_text)

# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded
gasp.finish()import lxml.html
import scraperwiki
gasp_helper = scraperwiki.utils.swimport("gasp_helper")


# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/


# Step 1) PLACE YOUR CONFIG LINE HERE
#         (it should look something like `gasp = gasp_helper.GaspHelper("your-api-key", "P000001")`)
gasp = gasp_helper.GaspHelper("67ed2d7ecd144c2bb8d3622113bdba86", "W000805")


# Step 2) Write Your Scraper Here
#         (refer to https://scraperwiki.com/scrapers/gasp_helper for documentation)
bio_html = scraperwiki.scrape('http://www.warner.senate.gov/public/index.cfm/biography')
bio_doc = lxml.html.fromstring(bio_html)
bio_text = bio_doc.xpath('//div[@class="article"]')[0].text_content()

gasp.add_biography(bio_text)

# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded
gasp.finish()