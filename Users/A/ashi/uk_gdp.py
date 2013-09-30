import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #here we define the table with column names
    scraperwiki.metadata.save('data_columns', ['Website', \
    'Year,quarter','GDP,adjusted for inflat-ion,£m','% change','GDP,adjusted for inflation,£m','inflation-adjusted per capita,£',])
    #from the below function the table is defined in the sort able manner
    data = soup.find("table", {"class": "in-article sortable"})
    #here row is defined which are formed in the table
    rows = data.findAll("tr")
    for rw in rows:
        record = {}
        #the below expression is written to find the cells of the table
        table_ukgdp = rw.findAll("td")
        #the number of cells in the row is calculated and recorded
        if len(table_ukgdp) == 5:#Check if it is correct
            record['Year,quarter'] = table_ukgdp[0].text
            record['GDP,adjusted for inflat-ion,£m'] = table_ukgdp[1].text
            record['% change'] = table_ukgdp[2].text
            record['GDP,adjusted for inflation,£m'] = table_ukgdp[3].text
            record['Year,quarter'] = table_ukgdp[4].text
            print record,
            print "------------"
            # recorded and saved the data which is in the below function
            scraperwiki.datastore.save(["Year,quarter"], record)


#the website link is given below 
website = " http://www.guardian.co.uk/news/datablog/2009/nov/25/gdp-uk-1948-growth-economy"
#changing all codes into HTML coding
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)
import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #here we define the table with column names
    scraperwiki.metadata.save('data_columns', ['Website', \
    'Year,quarter','GDP,adjusted for inflat-ion,£m','% change','GDP,adjusted for inflation,£m','inflation-adjusted per capita,£',])
    #from the below function the table is defined in the sort able manner
    data = soup.find("table", {"class": "in-article sortable"})
    #here row is defined which are formed in the table
    rows = data.findAll("tr")
    for rw in rows:
        record = {}
        #the below expression is written to find the cells of the table
        table_ukgdp = rw.findAll("td")
        #the number of cells in the row is calculated and recorded
        if len(table_ukgdp) == 5:#Check if it is correct
            record['Year,quarter'] = table_ukgdp[0].text
            record['GDP,adjusted for inflat-ion,£m'] = table_ukgdp[1].text
            record['% change'] = table_ukgdp[2].text
            record['GDP,adjusted for inflation,£m'] = table_ukgdp[3].text
            record['Year,quarter'] = table_ukgdp[4].text
            print record,
            print "------------"
            # recorded and saved the data which is in the below function
            scraperwiki.datastore.save(["Year,quarter"], record)


#the website link is given below 
website = " http://www.guardian.co.uk/news/datablog/2009/nov/25/gdp-uk-1948-growth-economy"
#changing all codes into HTML coding
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)
