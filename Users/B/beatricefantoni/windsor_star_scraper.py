import scraperwiki
import re
import time

# Blank Python
def our_scraper(Toronto_Craigslist):
    the_page = scraperwiki.scrape(Toronto_Craigslist)
    for every_post in re.finditer('<p><a href="http://toronto.en.craigslist.ca/tor/mis/.+?html">(.+?) <font size="-1">', the_page):

        every_post = every_post.group(1)
        print every_post

        scraperwiki.sqlite.save(unique_keys=["listing"],data={"listing": every_post})

base_link = "http://toronto.craigslist.ca/mis/index"
base_number = 0

while base_number < 500:
    Toronto_Craigslist = base_link + str(base_number) + ".html"
    our_scraper(Toronto_Craigslist)
    base_number = base_number + 100
    time.sleep(2)
