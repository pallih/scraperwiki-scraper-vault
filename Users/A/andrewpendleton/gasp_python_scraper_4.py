import scraperwiki, re
from pyquery import PyQuery as pq
gasp_helper = scraperwiki.utils.swimport("gasp_helper")


# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/


# Step 1) PLACE YOUR CONFIG LINE HERE
#         (it should look something like `gasp = gasp_helper.GaspHelper("your-api-key", "P000001")`)
gasp = gasp_helper.GaspHelper("YOUR_SUNLIGHT_KEY", "Y000033")

# Step 2) Write Your Scraper Here
#         (refer to https://scraperwiki.com/scrapers/gasp_helper for documentation)

# first grab homepage for generic stuff
main_doc = pq(url="http://donyoung.house.gov/")

# offices
for address in main_doc(".footer-select .select-content li"):
    m = re.match("".join([
            r"<strong>(?P<name>[\w\s,]+)(<br />)?</strong>(<br />&#13;)?\s*",
            r"(?P<address>[\w\s<>&#/;,\.]+)<br />&#13;\s*",
            r"(?P<city>\w+), (?P<state>\w{2,6}) (?P<zipcode>\d{5})\s*<br />&#13;\s*",
            r"T (?P<phone>\(\d{3}\) \d{3}-\d{4})\s*F?\s*(?P<fax>\(\d{3}\) \d{3}-\d{4})?.*"
        ]),
        pq(address).html()
    )
    if m:
        office = m.groupdict()
        office['address'] = re.sub(r"\s*(<br />&#13;)?\n\s*", "\n", office['address'])
        office['name'] = office['name'].title()
        office['fax'] = "" if office['fax'] is None else office['fax']
        
        gasp.add_office(**office)
    else:
        # what do we do if there's an address that we can't parse? raise an exception?
        pass

# bio
bio_doc = pq(url="http://donyoung.house.gov/Biography/")
bio = bio_doc('#ctl00_ctl00_ctl00_Text').html()
gasp.add_biography(bio)


# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded
gasp.finish()import scraperwiki, re
from pyquery import PyQuery as pq
gasp_helper = scraperwiki.utils.swimport("gasp_helper")


# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/


# Step 1) PLACE YOUR CONFIG LINE HERE
#         (it should look something like `gasp = gasp_helper.GaspHelper("your-api-key", "P000001")`)
gasp = gasp_helper.GaspHelper("YOUR_SUNLIGHT_KEY", "Y000033")

# Step 2) Write Your Scraper Here
#         (refer to https://scraperwiki.com/scrapers/gasp_helper for documentation)

# first grab homepage for generic stuff
main_doc = pq(url="http://donyoung.house.gov/")

# offices
for address in main_doc(".footer-select .select-content li"):
    m = re.match("".join([
            r"<strong>(?P<name>[\w\s,]+)(<br />)?</strong>(<br />&#13;)?\s*",
            r"(?P<address>[\w\s<>&#/;,\.]+)<br />&#13;\s*",
            r"(?P<city>\w+), (?P<state>\w{2,6}) (?P<zipcode>\d{5})\s*<br />&#13;\s*",
            r"T (?P<phone>\(\d{3}\) \d{3}-\d{4})\s*F?\s*(?P<fax>\(\d{3}\) \d{3}-\d{4})?.*"
        ]),
        pq(address).html()
    )
    if m:
        office = m.groupdict()
        office['address'] = re.sub(r"\s*(<br />&#13;)?\n\s*", "\n", office['address'])
        office['name'] = office['name'].title()
        office['fax'] = "" if office['fax'] is None else office['fax']
        
        gasp.add_office(**office)
    else:
        # what do we do if there's an address that we can't parse? raise an exception?
        pass

# bio
bio_doc = pq(url="http://donyoung.house.gov/Biography/")
bio = bio_doc('#ctl00_ctl00_ctl00_Text').html()
gasp.add_biography(bio)


# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded
gasp.finish()