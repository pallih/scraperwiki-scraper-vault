import scraperwiki
gasp_helper = scraperwiki.utils.swimport("gasp_helper")


# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/


# Step 1) PASTE SCRAPER CONFIG HERE
#         (it should look something like `gasp = gasp_helper.GaspHelper("your-api-key", "P000001")`)
gasp = gasp_helper.GaspHelper('c1c8fe4e515841b8b1d3814e42eebe26', 'P000523')

# Step 2) Write Your Scraper Here
#         (refer to https://scraperwiki.com/scrapers/gasp_helper for documentation)
gasp.add_issue('Beef', "What's Beef?")

# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded
gasp.finish()import scraperwiki
gasp_helper = scraperwiki.utils.swimport("gasp_helper")


# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/


# Step 1) PASTE SCRAPER CONFIG HERE
#         (it should look something like `gasp = gasp_helper.GaspHelper("your-api-key", "P000001")`)
gasp = gasp_helper.GaspHelper('c1c8fe4e515841b8b1d3814e42eebe26', 'P000523')

# Step 2) Write Your Scraper Here
#         (refer to https://scraperwiki.com/scrapers/gasp_helper for documentation)
gasp.add_issue('Beef', "What's Beef?")

# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded
gasp.finish()