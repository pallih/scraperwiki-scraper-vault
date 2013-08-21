import scraperwiki
import lxml.html
gasp_helper = scraperwiki.utils.swimport("gasp_helper")


# This is a Python template for a Sunlight Labs Great American Scraper Project
# http://services.sunlightlabs.com/gasp/legislators/


# Step 1) PLACE YOUR CONFIG LINE HERE
gasp = gasp_helper.GaspHelper("4fac0d2b1f944a7fba0089e1c14a94d6", "V000128")


# Step 2) Write Your Scraper Here

# Scrape contact info for offices
html = scraperwiki.scrape("http://vanhollen.house.gov/Contact/")
root = lxml.html.fromstring(html)
print html  # print for reference while coding
for strong in root.xpath("//td[@class='ContentCell']/span[@id='ctl00_ctl11_ctl00_Text']/table['1']/tbody['1']/tr['1']/td/strong"):  
    # This doesn't currently get Hyattsville or past the first line of address/phone info.  Need to mess around with .tail
    oname = strong.text_content()
    oinfo = strong.tail

    data = {
        'officename' : oname,
        'content' : oinfo
        }

    scraperwiki.sqlite.save(unique_keys=['officename'], data=data)

# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded
gasp.finish()