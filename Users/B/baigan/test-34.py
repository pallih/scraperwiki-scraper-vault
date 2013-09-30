import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #To define the names of columns
    scraperwiki.metadata.save('data_columns', ['Domain', \
    'Country, %', \
    'Sponsor, Q1 2008, %'])
    #To find table in html code
    table = soup.find("table", {"class": "in-article sortable"})
    #To find each row of the table
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #To find each cell of the table
        table_td = row.findAll("td")
        #Each row should include three cells
        if len(table_td) == 5:#Check if it is correct
            record['Domain'] = table_td[1].text
            record['Country/Purpose'] = \
            table_td[2].text
            record['Sponsoring Organisation'] = \
            table_td[3].text
            print record,
            print "-" * 10
            #Save one by one
            scraperwiki.datastore.save(["domain"], record)


#Define the website
website = "http://www.guardian.co.uk/news/datablog/2009/nov/24/internet-domain-names-worldwide"
#Put the all code in html variable
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)


import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #To define the names of columns
    scraperwiki.metadata.save('data_columns', ['Domain', \
    'Country, %', \
    'Sponsor, Q1 2008, %'])
    #To find table in html code
    table = soup.find("table", {"class": "in-article sortable"})
    #To find each row of the table
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #To find each cell of the table
        table_td = row.findAll("td")
        #Each row should include three cells
        if len(table_td) == 5:#Check if it is correct
            record['Domain'] = table_td[1].text
            record['Country/Purpose'] = \
            table_td[2].text
            record['Sponsoring Organisation'] = \
            table_td[3].text
            print record,
            print "-" * 10
            #Save one by one
            scraperwiki.datastore.save(["domain"], record)


#Define the website
website = "http://www.guardian.co.uk/news/datablog/2009/nov/24/internet-domain-names-worldwide"
#Put the all code in html variable
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)


