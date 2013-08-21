
# Blank Python
import scraperwiki

our_url = "http://www.ottawacitizen.com"

the_page =scraperwiki.scrape(our_url)

print the_page

scraperwiki.sqlite.save(unique_keys=["raw_html"], data={"raw_html": the_page})
