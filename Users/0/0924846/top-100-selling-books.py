import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):

    scraperwiki.metadata.save('data_columns', ['Pos','Title','Author','Imprint','Volume','Value,£',])
    
    table = soup.find("table", {"class": "in-article sortable"})
    
    rows = table.findAll("tr")
    for row in rows:
        record = {}
       
        table_td = row.findAll("td")
    
        if len(table_td) == 6:
            record['Pos'] = table_td[0].text
            record['Title'] = table_td[1].text
            record['Author'] = table_td[2].text
            record['Value,£'] = table_td[5].text
            print record,
            print "-" * 10
          
            scraperwiki.datastore.save(["Pos"], record)


#Define the website
website = "http://www.guardian.co.uk/news/datablog/2011/jan/01/top-100-books-of-all-time"
#Put the all code in html variable
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)

import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):

    scraperwiki.metadata.save('data_columns', ['Pos','Title','Author','Imprint','Volume','Value,£',])
    
    table = soup.find("table", {"class": "in-article sortable"})
    
    rows = table.findAll("tr")
    for row in rows:
        record = {}
       
        table_td = row.findAll("td")
    
        if len(table_td) == 6:
            record['Pos'] = table_td[0].text
            record['Title'] = table_td[1].text
            record['Author'] = table_td[2].text
            record['Value,£'] = table_td[5].text
            print record,
            print "-" * 10
          
            scraperwiki.datastore.save(["Pos"], record)


#Define the website
website = "http://www.guardian.co.uk/news/datablog/2011/jan/01/top-100-books-of-all-time"
#Put the all code in html variable
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)

