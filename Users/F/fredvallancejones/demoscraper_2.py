import scraperwiki
import re
import time

file_path = open("our_file.txt", "a")

def our_scraper(our_url):
    the_page = scraperwiki.scrape(our_url)
    print the_page
    for every_post in re.finditer("<td class='noWrap alignTop' >(....-..-..)</td>", the_page):

                every_post = every_post.group(1)
                every_post = re.sub(" - ", "\t", every_post)
                print every_post
                scraperwiki.sqlite.save(unique_keys=["listing"], data={"listing": every_post})

our_scraper("http://www.tbs-sct.gc.ca/scripts/contracts-contrats/reports-rapports-eng.asp")

base_link = "http://ottawa.en.craigslist.ca/mis/index"
#http://www.tbs-sct.gc.ca/scripts/contracts-contrats/reports-rapports-eng.asp?r=l&yr=2011&q=3&d=

year = 2004
quarter = 1
     
while quarter < 5:
    our_url  =  base_link + str(base_number) + ".html"
    our_scraper(our_url)
    base_number = base_number + 100
    time.sleep(2)
import scraperwiki
import re
import time

file_path = open("our_file.txt", "a")

def our_scraper(our_url):
    the_page = scraperwiki.scrape(our_url)
    print the_page
    for every_post in re.finditer("<td class='noWrap alignTop' >(....-..-..)</td>", the_page):

                every_post = every_post.group(1)
                every_post = re.sub(" - ", "\t", every_post)
                print every_post
                scraperwiki.sqlite.save(unique_keys=["listing"], data={"listing": every_post})

our_scraper("http://www.tbs-sct.gc.ca/scripts/contracts-contrats/reports-rapports-eng.asp")

base_link = "http://ottawa.en.craigslist.ca/mis/index"
#http://www.tbs-sct.gc.ca/scripts/contracts-contrats/reports-rapports-eng.asp?r=l&yr=2011&q=3&d=

year = 2004
quarter = 1
     
while quarter < 5:
    our_url  =  base_link + str(base_number) + ".html"
    our_scraper(our_url)
    base_number = base_number + 100
    time.sleep(2)
