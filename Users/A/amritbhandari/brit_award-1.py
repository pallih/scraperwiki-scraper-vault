# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup

def scrape_table(soup):
    #each column is defined here:
    scraperwiki.metadata.save('data_columns', ['Year','Category','Winner'])
    #table is recognised from the website:
    table = soup.find("table", {"class": "in-article sortable"})
    #ows of the table is defined here:
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #each cell is defined
        table_award = row.findAll("td")
        #there are 3 cells which are defined in the table:
        if len(table_award) == 3:
            record['Year'] = table_award[0].text
            record['Category'] = table_award[1].text
            record['Winner'] = table_award[2].text
            
            print record,
            print "-------------"
            #the data is extracted and saved:
            scraperwiki.datastore.save(["Year"], record)

# information is collected through the website link.
website = "http://www.guardian.co.uk/news/datablog/2011/feb/16/brit-awards-2011-all-winners-take-that"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)
