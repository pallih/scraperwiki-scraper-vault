import scraperwiki
gasp_helper = scraperwiki.utils.swimport("gasp_helper")


# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/


# Step 1) PLACE YOUR CONFIG LINE HERE
#         (it should look something like `gasp = gasp_helper.GaspHelper("your-api-key", "P000001")`)
gasp = gasp_helper.GaspHelper('6148c35a4140401d806856ec149c0a86', 'H001051')

# Step 2) Write Your Scraper Here
#         (refer to https://scraperwiki.com/scrapers/gasp_helper for documentation)

import lxml.html
#front page
front_html = scraperwiki.scrape('http://hanna.house.gov/index.php')
bio_html = scraperwiki.scrape('http://hanna.house.gov/index.php?option=com_content&view=article&id=3039&Itemid=300114')
# agriculture issue page
# issue_ag_html = scraperwiki.scrape('http://hanna.house.gov/index.php?option=com_content&view=article&id=3044&Itemid=300095')

front_root = lxml.html.fromstring(front_html)
bio_root = lxml.html.fromstring(bio_html)
# issue_ag_root = lxml.html.fromstring(issue_ag_html)

# ~--find offices--~
for div in front_root.cssselect("div.office"):
    
    office_name = div.cssselect("a > b")[0].text
    addy1, addy2, ph, fx = [ p.text for p in div.cssselect("p")]

    city, state_zip = addy2.split(', ')
    state, zip = state_zip.rsplit(' ', 2)
    gasp.add_office(addy1, city, state, zip, ph, fax=fx, name=office_name)

# ~--find biography--~
bio = ''
for p in bio_root.cssselect("div#page p"):
    bio += p.text + '\n\n'

gasp.add_biography(bio)
    




# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded
gasp.finish()import scraperwiki
gasp_helper = scraperwiki.utils.swimport("gasp_helper")


# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/


# Step 1) PLACE YOUR CONFIG LINE HERE
#         (it should look something like `gasp = gasp_helper.GaspHelper("your-api-key", "P000001")`)
gasp = gasp_helper.GaspHelper('6148c35a4140401d806856ec149c0a86', 'H001051')

# Step 2) Write Your Scraper Here
#         (refer to https://scraperwiki.com/scrapers/gasp_helper for documentation)

import lxml.html
#front page
front_html = scraperwiki.scrape('http://hanna.house.gov/index.php')
bio_html = scraperwiki.scrape('http://hanna.house.gov/index.php?option=com_content&view=article&id=3039&Itemid=300114')
# agriculture issue page
# issue_ag_html = scraperwiki.scrape('http://hanna.house.gov/index.php?option=com_content&view=article&id=3044&Itemid=300095')

front_root = lxml.html.fromstring(front_html)
bio_root = lxml.html.fromstring(bio_html)
# issue_ag_root = lxml.html.fromstring(issue_ag_html)

# ~--find offices--~
for div in front_root.cssselect("div.office"):
    
    office_name = div.cssselect("a > b")[0].text
    addy1, addy2, ph, fx = [ p.text for p in div.cssselect("p")]

    city, state_zip = addy2.split(', ')
    state, zip = state_zip.rsplit(' ', 2)
    gasp.add_office(addy1, city, state, zip, ph, fax=fx, name=office_name)

# ~--find biography--~
bio = ''
for p in bio_root.cssselect("div#page p"):
    bio += p.text + '\n\n'

gasp.add_biography(bio)
    




# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded
gasp.finish()