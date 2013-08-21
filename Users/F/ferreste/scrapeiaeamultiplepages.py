######################################################################################################
# scrapes multiple pages from the iaea events section to show event titles, urls, locations and dates#
######################################################################################################

import scraperwiki
import urlparse
import lxml.html


# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("#tblEvents tr") # selects all <tr> blocks within <table id="tblEvents">
    for row in rows:
        # Set up our data record = we'll need it later
        record = {}
        table_cells_1 = row.cssselect("h4 a")
        table_cells_2 = row.cssselect("span")
      
        if table_cells_1:
           record['EventTitle'] = table_cells_1[0].text
           record['PlaceAndDate'] = table_cells_2[1].text
           


        #Print out the data we've gathered
        print record, '------------'
        # Finally, save the record to the datastore - 'EventTitle' is our unique key
        scraperwiki.sqlite.save(["EventTitle"], record)

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url,next_page):
   
   
     html = scraperwiki.scrape(url)
     print html
     root = lxml.html.fromstring(html)
     scrape_table(root)
     next_page += 1
     print next_page
     next_url = 'http://www-news.iaea.org/EventList.aspx?ps=10&pno=' + str(next_page)
     print next_url
     scrape_and_look_for_next_link(next_url,next_page) 

  

     

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------



base_url = 'http://www-news.iaea.org/'
next_page = 0
starting_url = urlparse.urljoin(base_url,'EventList.aspx?ps=10&pno=', allow_fragments=True)
scrape_and_look_for_next_link(starting_url,next_page)