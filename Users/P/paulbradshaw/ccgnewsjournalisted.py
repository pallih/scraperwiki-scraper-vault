import scraperwiki
import lxml.html
from datetime import datetime

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("h4 a")  # selects all parts of 'root' within <h4><a> 
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        # grab the text and put it in 'Headline'
        record['Headline'] = row.text_content()
        #grab the href= attribute in the HTML and put that in 'URL'
        record['URL'] = row.attrib.get('href')
        #use a function in the datetime library to get the current time, and put it in 'date_scraped'
        #we need a date field if this will work as an RSS feed
        #see http://blog.scraperwiki.com/2011/09/21/make-rss-with-an-sql-query/ for more
        record['date_scraped'] = datetime.now()
        print record, '------------'
        # Finally, save the record to the datastore - 'URL' is our unique key
        scraperwiki.datastore.save(["URL"], record)
        
# scrape_and_look_for_next_link function: 
def scrape_and_look_for_next_link(url):
    #use scrape function to grab contents of 'url', and put into 'html' 
    html = scraperwiki.scrape(url)
    #show the results in Console
    print html
    #use fromstring function to convert 'html' into lxml object 'root'
    root = lxml.html.fromstring(html)
    #run scrape_table function (created around line 6 above) on 'root'
    scrape_table(root)
    #If you wanted to scrape more than one page, then add further lines to this function
    #to look for the 'next' link and repeat the process

# SCRAPER STARTS RUNNING HERE
starting_url = 'http://journalisted.com/search?type=article&q=ccg'
#run scrape_and_look_for_next_link function on 'starting_url' 
scrape_and_look_for_next_link(starting_url)
