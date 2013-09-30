import lxml.html
import scraperwiki

gasp_helper = scraperwiki.utils.swimport("gasp_helper")

gasp = gasp_helper.GaspHelper("ce429200f22a42c68bdf8bfa611bd085", "R000576")

bio_html = scraperwiki.scrape("http://dutch.house.gov/bio.shtml")
bio_doc = lxml.html.fromstring(bio_html)
biotext = bio_doc.xpath('//div[@class="asset-body"]')[0].text_content()
gasp.add_biography(biotext)

gasp.add_twitter('http://twitter.com/call_me_dutch')


# offices
# http://dutch.house.gov/office-information.shtml

gasp.finish()
import lxml.html
import scraperwiki

gasp_helper = scraperwiki.utils.swimport("gasp_helper")

gasp = gasp_helper.GaspHelper("ce429200f22a42c68bdf8bfa611bd085", "R000576")

bio_html = scraperwiki.scrape("http://dutch.house.gov/bio.shtml")
bio_doc = lxml.html.fromstring(bio_html)
biotext = bio_doc.xpath('//div[@class="asset-body"]')[0].text_content()
gasp.add_biography(biotext)

gasp.add_twitter('http://twitter.com/call_me_dutch')


# offices
# http://dutch.house.gov/office-information.shtml

gasp.finish()
