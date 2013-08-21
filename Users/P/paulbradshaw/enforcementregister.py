import scraperwiki
import urlparse
import lxml.html

#THIS SCRAPER GENERATES AN INFINITE REDIRECT ERROR - DOES NOT WORK
#MAY BE WORTH TRYING REQUEST?

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    #<span class="enforce_result_link_text">
    rows = root.cssselect("div")  # selects all <span class="enforce_result_link_text">
    for row in rows:
        # Set up our data record - we'll need it later
        print row
        record = {}
        record['Artist'] = row.text
        scraperwiki.datastore.save(["Artist"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    rows = root.cssselect("div.enforce_result_container_complied")  # selects all <span class="enforce_result_link_text">
    for row in rows:
        # Set up our data record - we'll need it later
        print row
        record = {}
        record['Artist'] = row.text_content()
        scraperwiki.datastore.save(["Artist"], record)
#    scrape_table(root)

starting_url ='http://www.cfoa.org.uk/11823?pv=search&page=1&results_per_page=50&premises_type_id=&premise_id=&frs_id=&organisation_name=&responsible_person=&address=&address_postcode=&status_id='
scrape_and_look_for_next_link(starting_url)
