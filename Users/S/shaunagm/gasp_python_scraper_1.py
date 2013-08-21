import scraperwiki
import lxml.html
gasp_helper = scraperwiki.utils.swimport("gasp_helper")


# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/


# Config
gasp = gasp_helper.GaspHelper("4fac0d2b1f944a7fba0089e1c14a94d6", "B001268")

# Scrape contact info for offices
html = scraperwiki.scrape("http://www.scottbrown.senate.gov/public/index.cfm/officeinformation/")
root = lxml.html.fromstring(html)
print html  # print for reference while coding
officenames = ["dc","boston","plymouth","springfield","worcester"]  # each div class has different name, so create an array of names
for oname in officenames:
    for tr in root.xpath("//div[@class='"+oname+"']/div[@class='content']"):   # finds divs with class attributes equalling oname, finds content inside (which is the same across divs)
            data = {
                'officename' : oname,
                'content' : tr.text_content()  # text_content() gets text inside the div
            }
            scraperwiki.sqlite.save(unique_keys=['officename'], data=data)

# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded
gasp.finish()