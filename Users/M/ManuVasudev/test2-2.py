import scraperwiki
from BeautifulSoup import BeautifulSoup

def scrape_table(url):
    htmlCode = scraperwiki.scrape(url)
    #definition of column name that is going to be stored
    scraperwiki.metadata.save('data_columns', ['Ignore', 'Country','Overall rate',\
    'Male rate','Female rate'])
    
    soup = BeautifulSoup(htmlCode)
    #find table
    rankingTable = soup.find("table", {"class": "stand-alone sortable"})
    
    #find rows of the rankingTable
    rows = rankingTable.findAll("tr")
    for row in rows:
        #declaration of the records
        records = {}
        cells = row.findAll("td")
        if cells:
            records['Ignore'] = cells[0].text
            records['Country'] = cells[1].text
            records['Overall rate'] = cells[7].text
            records['Male rate']= cells[4].text
            records['Female rate'] = cells[5].text
            print records, '------------'
            #save the data
            scraperwiki.datastore.save(['Ignore'], records)
    
#Website - Source - call scrape_table function to process data
source = "http://www.guardian.co.uk/news/datablog/2011/jan/24/worldwide-cancer-rates-uk-rate-drops"
scrape_table(source)

