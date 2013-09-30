import scraperwiki
import urlparse
import lxml.html
import datetime
now = datetime.datetime.now()

# scrape_table function: gets passed an individual page to scrape
url = 'http://stoke.gov.uk/ccm/content/xml-feeds/events/events---events-next-month.en?bbp.s=1&form.events---events-next-month=visited&bbp.i=d0.1'
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
rows = root.cssselect("div.greeting table tbody tr")  # selects all <tr> blocks within <table class="data">
    #print rows
for row in rows:
        record = {}
        table_cells = row.cssselect("td a")
        if table_cells: 
            record['Book'] = table_cells[0].text
            print record
        table_cells2 = row.cssselect("td")
        if table_cells2: 
            record['Details'] = table_cells2[1].text_content()
        #table_cells3 = row.cssselect("div.highlightedBy")
        #if table_cells3: 
            #record['Highlighted_by'] = table_cells3[0].text   
            scraperwiki.sqlite.save(unique_keys=[], data={'Scrape_date' : now, 'Name' : table_cells[0].text,'Details' : table_cells2[1].text_content(),'Place' : table_cells2[2].text_content(),'Dates' : table_cells2[3].text_content(),'View_link' : table_cells[1].attrib['href']})
        

import scraperwiki
import urlparse
import lxml.html
import datetime
now = datetime.datetime.now()

# scrape_table function: gets passed an individual page to scrape
url = 'http://stoke.gov.uk/ccm/content/xml-feeds/events/events---events-next-month.en?bbp.s=1&form.events---events-next-month=visited&bbp.i=d0.1'
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
rows = root.cssselect("div.greeting table tbody tr")  # selects all <tr> blocks within <table class="data">
    #print rows
for row in rows:
        record = {}
        table_cells = row.cssselect("td a")
        if table_cells: 
            record['Book'] = table_cells[0].text
            print record
        table_cells2 = row.cssselect("td")
        if table_cells2: 
            record['Details'] = table_cells2[1].text_content()
        #table_cells3 = row.cssselect("div.highlightedBy")
        #if table_cells3: 
            #record['Highlighted_by'] = table_cells3[0].text   
            scraperwiki.sqlite.save(unique_keys=[], data={'Scrape_date' : now, 'Name' : table_cells[0].text,'Details' : table_cells2[1].text_content(),'Place' : table_cells2[2].text_content(),'Dates' : table_cells2[3].text_content(),'View_link' : table_cells[1].attrib['href']})
        

