# Imports!
import lxml.html
import scraperwiki

# Initialize the scraperwiki/GASP tools.
gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper("67ed2d7ecd144c2bb8d3622113bdba86", "S000185")

# Start with the HTML. Grab his bio page.
bio_html = scraperwiki.scrape('http://bobbyscott.house.gov/index.php?option=com_content&view=article&id=267&Itemid=61')

# Parse the raw HTML with lxml's HTML parser.
bio_doc = lxml.html.fromstring(bio_html)
#print bio_doc
# Use XPATH to find the one div that has property="content:encoded."
# It's a list that returns, so I have to take the first one.
# This might be a little bit brittle.
bio_text = bio_doc.xpath('//div[@id="page"]/p')[1].text_content()+bio_doc.xpath('//div[@id="page"]/p')[2].text_content()+bio_doc.xpath('//div[@id="page"]/p')[3].text_content()+bio_doc.xpath('//div[@id="page"]/p')[4].text_content()+bio_doc.xpath('//div[@id="page"]/p')[5].text_content()+bio_doc.xpath('//div[@id="page"]/p')[6].text_content()+bio_doc.xpath('//div[@id="page"]/p')[7].text_content()+bio_doc.xpath('//div[@id="page"]/p')[8].text_content()+bio_doc.xpath('//div[@id="page"]/p')[9].text_content()+bio_doc.xpath('//div[@id="page"]/p')[10].text_content()


print bio_text
#Add this biography text to the GASP via a function.
gasp.add_biography(bio_text)

# Finish. Because mom said you should finish what you start.
gasp.finish()


# Imports!
import lxml.html
import scraperwiki

# Initialize the scraperwiki/GASP tools.
gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper("67ed2d7ecd144c2bb8d3622113bdba86", "S000185")

# Start with the HTML. Grab his bio page.
bio_html = scraperwiki.scrape('http://bobbyscott.house.gov/index.php?option=com_content&view=article&id=267&Itemid=61')

# Parse the raw HTML with lxml's HTML parser.
bio_doc = lxml.html.fromstring(bio_html)
#print bio_doc
# Use XPATH to find the one div that has property="content:encoded."
# It's a list that returns, so I have to take the first one.
# This might be a little bit brittle.
bio_text = bio_doc.xpath('//div[@id="page"]/p')[1].text_content()+bio_doc.xpath('//div[@id="page"]/p')[2].text_content()+bio_doc.xpath('//div[@id="page"]/p')[3].text_content()+bio_doc.xpath('//div[@id="page"]/p')[4].text_content()+bio_doc.xpath('//div[@id="page"]/p')[5].text_content()+bio_doc.xpath('//div[@id="page"]/p')[6].text_content()+bio_doc.xpath('//div[@id="page"]/p')[7].text_content()+bio_doc.xpath('//div[@id="page"]/p')[8].text_content()+bio_doc.xpath('//div[@id="page"]/p')[9].text_content()+bio_doc.xpath('//div[@id="page"]/p')[10].text_content()


print bio_text
#Add this biography text to the GASP via a function.
gasp.add_biography(bio_text)

# Finish. Because mom said you should finish what you start.
gasp.finish()


