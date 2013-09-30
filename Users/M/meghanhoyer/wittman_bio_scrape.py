"""
Welcome to a reasonable interpretation of a scraper in scraperwiki.
This is mostly Pythonic, which is always good.

Today, we'll be scraping a member of congress's Web site for the
Great American Scraper (GASP) project from Sunlight Foundation.
"""

# Imports!
import lxml.html
import scraperwiki

# Initialize the scraperwiki/GASP tools.
gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper("67ed2d7ecd144c2bb8d3622113bdba86", "W000804")

# Start with the HTML. Grab his bio page.
bio_html = scraperwiki.scrape('http://wittman.house.gov/index.php?option=com_content&view=article&id=12&Itemid=34')

# Parse the raw HTML with lxml's HTML parser.
bio_doc = lxml.html.fromstring(bio_html)
#print bio_doc
# Use XPATH to find the one div that has property="content:encoded."
# It's a list that returns, so I have to take the first one.
# This might be a little bit brittle.
bio_text = bio_doc.xpath('//table[@class="contentpaneopen"]')[1].text_content()
#print bio_text
# Add this biography text to the GASP via a function.
gasp.add_biography(bio_text)

# Finish. Because mom said you should finish what you start.
gasp.finish()

"""
Welcome to a reasonable interpretation of a scraper in scraperwiki.
This is mostly Pythonic, which is always good.

Today, we'll be scraping a member of congress's Web site for the
Great American Scraper (GASP) project from Sunlight Foundation.
"""

# Imports!
import lxml.html
import scraperwiki

# Initialize the scraperwiki/GASP tools.
gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper("67ed2d7ecd144c2bb8d3622113bdba86", "W000804")

# Start with the HTML. Grab his bio page.
bio_html = scraperwiki.scrape('http://wittman.house.gov/index.php?option=com_content&view=article&id=12&Itemid=34')

# Parse the raw HTML with lxml's HTML parser.
bio_doc = lxml.html.fromstring(bio_html)
#print bio_doc
# Use XPATH to find the one div that has property="content:encoded."
# It's a list that returns, so I have to take the first one.
# This might be a little bit brittle.
bio_text = bio_doc.xpath('//table[@class="contentpaneopen"]')[1].text_content()
#print bio_text
# Add this biography text to the GASP via a function.
gasp.add_biography(bio_text)

# Finish. Because mom said you should finish what you start.
gasp.finish()

