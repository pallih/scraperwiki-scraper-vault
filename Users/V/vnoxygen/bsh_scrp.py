import scraperwiki
import lxml.html


def scrape_table(root):
    rows = root.cssselect("p.qt")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        temp_str = row.text_content().strip()
        if not ("\n" in temp_str ) and len(temp_str) > 5 : 
            # Set up our data record - we'll need it later
            record = {}
            record['Quote'] = temp_str 
            # Print out the data we've gathered
            #print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save(["Quote"], record)

max = 419
for i in range(max, -1, -1):
    #print "Hello", i+1
    if i==0:
        html = scraperwiki.scrape('http://bash.org/?browse')
    else:
        html = scraperwiki.scrape('http://bash.org/?browse&p='+ str(i))
    #print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    pass

print "Done"





# scrape_table function: gets passed an individual page to scrape




