import lxml.html

import scraperwiki
gasp_helper = scraperwiki.utils.swimport("gasp_helper")

gasp = gasp_helper.GaspHelper("ce429200f22a42c68bdf8bfa611bd085", "M000702")

# Begin what Tom added
print scraperwiki.scrape("http://sunlightfoundation.com/")
from urllib2 import urlopen
bio_html = urlopen("http://mikulski.senate.gov/about/biography.cfm").read()
# End what Tom added

bio_html = scraperwiki.scrape("http://mikulski.senate.gov/about/biography.cfm")

bio_doc = lxml.html.fromstring(bio_html)
biotext = bio_doc.xpath('//div[@class="CS_Textblock_Text"]').text_content()
gasp.add_biography(biotext)



# <div class="CS_Textblock_Text">

# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded

gasp.finish()