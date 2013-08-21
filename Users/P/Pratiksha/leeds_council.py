# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #here we define the names of the column which are in the table 
    scraperwiki.metadata.save('data_columns', ['Website', \
    'Body name','Service dvision lable','Detailed expenditure type','Net amount','Supplier name',])
    #from the below function the table is defined in the sort able manner
    table = soup.find("table", {"class": "in-article sortable"})
    #in this section each row is defined which are formed in the table
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #in order to find the cells in the table the below expression is written
        table_leeds = row.findAll("td")
        #the number of cells in the row is calculated and recorded
        if len(table_leeds) == 5:#Check if it is correct
            record['Body name'] = table_leeds[0].text
            record['Service dvision lable'] = table_leeds[1].text
            record['Detailed expenditure type'] = table_leeds[2].text
            record['Net amount'] = table_leeds[3].text
            record['Supplier name'] = table_leeds[4].text
            print record,
            print "-" * 10
            #the data is recorded and saved in the below function
            scraperwiki.datastore.save(["Body name"], record)


#the link of the website is given below 
website = "http://www.guardian.co.uk/leeds/2011/feb/18/leeds-council-reveals-spending-over-500"
#all the codes are changed into HTML coding
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)

