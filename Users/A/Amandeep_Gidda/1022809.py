import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #To name the columns accordingly:
    scraperwiki.metadata.save('data_columns', ['Aircraft Type', \
    'Fatal accidents to passengers', \
    'Total number currently operating', \
    'Total passenger fatalities'])
    #To determine the table in html code
    table = soup.find("table", {"class": "in-article sortable"})
    #To select each row of the table
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #To select each cell of the table
        table_td = row.findAll("td")
        #Each row should consist of four cells
        if len(table_td) == 4:#Cross check
            record['Aircraft Type'] = table_td[0].text
            record['Fatal accidents to passengers'] = \
            table_td[1].text
            record['Total number currently operating'] = \
            table_td[2].text
            record['Total passenger fatalities'] = \
            table_td[3].text
            print record,
            print "-" * 10
            #Save data
            scraperwiki.datastore.save(["Aircraft Type"], record)


website = "http://www.guardian.co.uk/news/datablog/2010/nov/05/qantas-engine-failure-airliner-safety"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)
