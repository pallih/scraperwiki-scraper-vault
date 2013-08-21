import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #To define the names of columns
    scraperwiki.metadata.save('data_columns', ['Website', \
    'Department','Visits, Apr 09 to March 10','Total costs (excl staff), £','Total costs per visit, £','Staff costs, £',])
    #To find table in html code
    table = soup.find("table", {"class": "in-article sortable"})
    #To find each row of the table
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #To find each cell of the table
        table_td = row.findAll("td")
        #Each row should include three cells
        if len(table_td) == 6:#Check if it is correct
            record['Website'] = table_td[0].text
            record['Total costs (excl staff), £'] = \
            table_td[3].text
            print record,
            print "-" * 10
            #Save one by one
            scraperwiki.datastore.save(["Website"], record)


#Define the website
website = "http://www.guardian.co.uk/news/datablog/2010/jul/05/government-websites-costs"
#Put the all code in html variable
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)
