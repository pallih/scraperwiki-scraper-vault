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
gasp = gasp_helper.GaspHelper("35c7f25a14624b968eb771c9062ecb30", "H001052")

# Start with the HTML. Grab his bio page.
bio_html = scraperwiki.scrape('http://harris.house.gov/about-me/full-biography')

# Parse the raw HTML with lxml's HTML parser.
bio_doc = lxml.html.fromstring(bio_html)

# Use XPATH to find the one div that has property="content:encoded."
# It's a list that returns, so I have to take the first one.
# This might be a little bit brittle.
bio_text = bio_doc.xpath('//div[@property="content:encoded"]')[0].text_content()

# Add this biography text to the GASP via a function.
gasp.add_biography(bio_text)

# Finish. Because mom said you should finish what you start.
# gasp.finish()

