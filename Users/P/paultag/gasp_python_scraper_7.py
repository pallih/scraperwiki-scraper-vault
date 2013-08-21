import scraperwiki

import lxml.html

WEBSITE_URL = "http://www.kerry.senate.gov/"

gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper("e22d3af15e034c03bc66117be59fda38", "K000148")

def get_page( url ):
    return lxml.html.fromstring(
        scraperwiki.scrape(url)
    )

def get_xpath( url, xpath ):
    return get_page(url).xpath(xpath)

root = get_page( WEBSITE_URL )
# OK. Prep'd.

###############
# Offices
#offices = get_xpath( "%s/contact" % WEBSITE_URL, "//div[@class='pod-content']/p" )[1:]
#for office in offices:
#    office = office.text_content()
#    addr = [ o.strip() for o in office.split("\r") ]

###############
# Social Media (this is a hack)
medias = get_xpath( WEBSITE_URL, "//ul[@id='social-tools-top']/li" )
for media in medias:
    m_type = media[0][0].attrib["class"]
    #              a/href
    url = media[0].attrib["href"].split("'")[1]
    # This is ultra hacky, sorry.
    gasp.add_social_media( m_type, url )

###############
# Bio
bio = get_xpath( "%s/about" % WEBSITE_URL, "//div[@id='sam-main']/p/text()" )
biography = ""
for para in bio:
    biography += para + "\n\n"
gasp.add_biography(biography)

###############
# Issues
issues = get_xpath( "%s/work/issues" % WEBSITE_URL, "//div[@class='issue-description']" )
for issue in issues:
    title  = issue.xpath("./h3")[0].text_content()
    stance = issue.xpath("./p" )[0].text_content()
    gasp.add_issue( title, stance )

# All done.
gasp.finish()