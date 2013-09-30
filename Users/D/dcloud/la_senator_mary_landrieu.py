import scraperwiki
import lxml.html

gasp_helper = scraperwiki.utils.swimport("gasp_helper")

URL_BASE = "http://www.landrieu.senate.gov/"

bio_path = "about/biography.cfm"
bio_div_id = 'cs_control_1919'

# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/


# Step 1) PLACE YOUR CONFIG LINE HERE
#         (it should look something like `gasp = gasp_helper.GaspHelper("your-api-key", "P000001")`)

gasp = gasp_helper.GaspHelper("YOUR_SUNLIGHT_KEY", "L000550")


# Step 2) Write Your Scraper Here
#         (refer to https://scraperwiki.com/scrapers/gasp_helper for documentation)

#def main():
#    bio_txt = _get_bio()
#    print "bio_text: {0}".format(bio_text)
#    gasp.add_biography(bio_txt)
    
def _get_bio():
    url = "{0}{1}".format(URL_BASE,bio_path)
    print "Getting bio from '{0}'".format(url)
    page_str = scraperwiki.scrape(url)
    print "Retrieved page_str from url"
    doc = lxml.html.fromstring(page_str)
    print "Parsed doc using lxml"
    return doc.get_element_by_id(bio_div_id).text_content()
    

# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded

#main()
#gasp.finish()

url = "{0}{1}".format(URL_BASE,bio_path)
print "Getting bio from '{0}'".format(url)
page_str = scraperwiki.scrape(url)
print "Retrieved page_str from url"
doc = lxml.html.fromstring(page_str)
print "Parsed doc using lxml"
print doc.get_element_by_id(bio_div_id).text_content()import scraperwiki
import lxml.html

gasp_helper = scraperwiki.utils.swimport("gasp_helper")

URL_BASE = "http://www.landrieu.senate.gov/"

bio_path = "about/biography.cfm"
bio_div_id = 'cs_control_1919'

# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/


# Step 1) PLACE YOUR CONFIG LINE HERE
#         (it should look something like `gasp = gasp_helper.GaspHelper("your-api-key", "P000001")`)

gasp = gasp_helper.GaspHelper("YOUR_SUNLIGHT_KEY", "L000550")


# Step 2) Write Your Scraper Here
#         (refer to https://scraperwiki.com/scrapers/gasp_helper for documentation)

#def main():
#    bio_txt = _get_bio()
#    print "bio_text: {0}".format(bio_text)
#    gasp.add_biography(bio_txt)
    
def _get_bio():
    url = "{0}{1}".format(URL_BASE,bio_path)
    print "Getting bio from '{0}'".format(url)
    page_str = scraperwiki.scrape(url)
    print "Retrieved page_str from url"
    doc = lxml.html.fromstring(page_str)
    print "Parsed doc using lxml"
    return doc.get_element_by_id(bio_div_id).text_content()
    

# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded

#main()
#gasp.finish()

url = "{0}{1}".format(URL_BASE,bio_path)
print "Getting bio from '{0}'".format(url)
page_str = scraperwiki.scrape(url)
print "Retrieved page_str from url"
doc = lxml.html.fromstring(page_str)
print "Parsed doc using lxml"
print doc.get_element_by_id(bio_div_id).text_content()