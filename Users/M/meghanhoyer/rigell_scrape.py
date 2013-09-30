import scraperwiki
import lxml.html

gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper("67ed2d7ecd144c2bb8d3622113bdba86", "R000589")

bio_html = scraperwiki.scrape("http://rigell.house.gov/Biography/")

bio_doc = lxml.html.fromstring(bio_html)

bio_text = bio_doc.xpath('//p')[1].text_content()

gasp.add_biography(bio_text)

gasp.finish()
#print bio_text
#print bio_doc
#print bio_html

import scraperwiki
import lxml.html

gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper("67ed2d7ecd144c2bb8d3622113bdba86", "R000589")

bio_html = scraperwiki.scrape("http://rigell.house.gov/Biography/")

bio_doc = lxml.html.fromstring(bio_html)

bio_text = bio_doc.xpath('//p')[1].text_content()

gasp.add_biography(bio_text)

gasp.finish()
#print bio_text
#print bio_doc
#print bio_html

