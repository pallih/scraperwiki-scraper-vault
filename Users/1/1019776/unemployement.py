# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup

def scrape_table(soup):
    #the column is defind where the data can be easily be defined:
    scraperwiki.metadata.save('data_columns', ['Constituency','Region','Male %','Women %','Total','% rate','Total % change on yr'])
    #here the table are standardised by HTML codings:
    table = soup.find("table", {"class": "in-article sortable"})
    #rows are defined:
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #every cell of the table is defined
        table_unemp = row.findAll("td")
        #there are 7 no of cells in the table:
        if len(table_unemp) == 7:
            record['Constituency'] = table_unemp[0].text
            record['Region'] = table_unemp[1].text
            record['Male %'] = table_unemp[2].text
            record['Women %'] = table_unemp[3].text
            record['Total'] = table_unemp[4].text
            record['% rate'] = table_unemp[5].text
            record['Total % change on yr'] = table_unemp[6].text
            print record,
            print "-------------"
            #Data is saved here:
            scraperwiki.datastore.save(["Constituency"], record)

# URL of the website is defined here so that the scraper can identify the link.
website = "http://www.guardian.co.uk/news/datablog/2010/nov/17/unemployment-and-employment-statistics-economics"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)
