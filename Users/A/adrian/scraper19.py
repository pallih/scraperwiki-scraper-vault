import scraperwiki
#import the libraries containing our functions
import scraperwiki
import lxml.html
import urllib
# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("tr") # selects all <tr> blocks
    for row in rows:

# Blank Python
# Set up our data record -we'll need it later
        record = {}
        table_cells = row.cssselect("td")
#if theres anything in the table_cells variable (a list)

        if table_cells:
#add to the variable record (a dictionary)these pairs:label'Horse': the text inthe first [0] table_-cells item...
            record['Horse'] = table_cells[0].text_content()
#create variable 'table_-cellsurls' and put init any links withinthe first table_cells item
            table_cellsurls = table_cells[0].cssselect("a")

#grab the href=" attribute and put that in 'HorseURL'
            record['HorseURL'] = table_cellsurls[0].attrib.get('href')
#creates variable 'horselink'which is a URL addingthe href attribute tothe end of the horsedeathwatch.com/base url
            #horselink = 'http://www.horsedeathwatch.com/'+table_cellsurls[0].attrib.get('href') //x3 sgtes lineas
            testingreplace = 'http://www.horsedeathwatch.com/'+table_cellsurls[0].attrib.get('href')
            print testingreplace.replace(" ", "%20")
            horselink = testingreplace.replace(" ", "%20")

#create another variable containing the scraped contents from that URL
            horsehtml = scraperwiki.scrape(horselink)
#Turn the webpage string into an lxml object
            horseroot = lxml.html.fromstring(horsehtml)
#put all the <p> tags on the horse page into a list
            pars = horseroot.cssselect("p")

#print and then store the text_content for the first item <p> in the pars list, the Age
            print pars[0].text_content()
            record['Agetest2'] = pars[0].text_content()
            record['Date'] = table_cells[1].text
            record['Course'] = table_cells[2].text
            record['Cause of death']= table_cells[3].text
# Print out the data we've gathered into the record variable, followed by '-----'
            print record, '------------'
# Finally, save the record to the datastore - 'Horse' is our unique key
            scraperwiki.sqlite.save(["Horse"],record)
# scrape_and_look_for_next_link function: scrapes page, converts to lxml object then calls the scrape_table function
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)

# START HERE: define your starting URL - then call a function to scrape it
starting_url = 'http://www.horsedeathwatch.com/'
scrape_and_look_for_next_link(starting_url)


