import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #To define the names of columns
    scraperwiki.metadata.save('data_columns', ['Category', \
    'UsesocialnetworkingsitesQ12009', \
    'UsesocialnetworkingsitesQ12008'])
    #To find table in html code
    table = soup.find("table", {"class": "in-article sortable"})
    #To find each row of the table
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #To find each cell of the table
        table_td = row.findAll("td")
        #Each row should include three cells
        if len(table_td) == 3:#Check if it is correct
            record['Category'] = table_td[0].text
            record['Usesocialnetworking sitesQ12009'] = \
            table_td[1].text
            record['Usesocialnetworking sitesQ12008'] = \
            table_td[2].text
            print record,
            print "-" * 10
            #Save one by one
            scraperwiki.datastore.save(["Category"], record)


#Define the website
website = "http://www.guardian.co.uk/news/datablog/2009/aug/06/ofcom-socialnetworking"
#Put the all code in html variable
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)

