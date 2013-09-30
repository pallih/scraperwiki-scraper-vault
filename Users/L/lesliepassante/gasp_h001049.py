import scraperwiki
import lxml.html

gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper("2f4512add2bc44e3b50bcc1dcfe98e5f", "H001049")

def get_bio():
    bio_html = scraperwiki.scrape('http://www.hagan.senate.gov/?p=biography')
    bio_doc = lxml.html.fromstring(bio_html)
    bio_text = bio_doc.xpath('//div[@class="bd record-bd"]')[0].text_content()
    print 

get_bio();import scraperwiki
import lxml.html

gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper("2f4512add2bc44e3b50bcc1dcfe98e5f", "H001049")

def get_bio():
    bio_html = scraperwiki.scrape('http://www.hagan.senate.gov/?p=biography')
    bio_doc = lxml.html.fromstring(bio_html)
    bio_text = bio_doc.xpath('//div[@class="bd record-bd"]')[0].text_content()
    print 

get_bio();