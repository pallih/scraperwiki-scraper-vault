import scraperwiki
html =  scraperwiki.scrape("http://www.guardian.co.uk/news/datablog/2011/jan/24/worldwide-cancer-rates-uk-rate-drops")
print html
import BeautifulSoup
soup = BeautifulSoup.BeautifulSoup(html)
for td in soup.findAll('td'):
    print td.string
for td in soup.findAll('td'):
                scraperwiki.datastore.save(unique_keys=['table_cell'],  data={'table_cell':td.string}) 
##########################################################################################################
import scraperwiki
from BeautifulSoup  import BeautifulSoup
website_url=('http://www.guardian.co.uk/news/datablog/2011/jan/24/worldwide-cancer-rates-uk-rate-drops')
def cancer(soup):
    scraperwiki.metadata.save('data_columns', ['Country', 'Overall rate', 'Male rate', 'Female rate'])
    data_table = soup.find("table", { "class" : "stand-alone sortable" })
    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells:
            record['Country'] = table_cells[1].text
            record['Overall rate'] = table_cells[2].text
            record['Male rate'] = table_cells[3].text
            record['Female rate'] = table_cells[4].text
            print record,"---------"
            scraperwiki.datastore.save(["Country"], record)


html = scraperwiki.scrape(website_url)         
soup = Beautifulsoup(html)
cancer(soup)import scraperwiki
html =  scraperwiki.scrape("http://www.guardian.co.uk/news/datablog/2011/jan/24/worldwide-cancer-rates-uk-rate-drops")
print html
import BeautifulSoup
soup = BeautifulSoup.BeautifulSoup(html)
for td in soup.findAll('td'):
    print td.string
for td in soup.findAll('td'):
                scraperwiki.datastore.save(unique_keys=['table_cell'],  data={'table_cell':td.string}) 
##########################################################################################################
import scraperwiki
from BeautifulSoup  import BeautifulSoup
website_url=('http://www.guardian.co.uk/news/datablog/2011/jan/24/worldwide-cancer-rates-uk-rate-drops')
def cancer(soup):
    scraperwiki.metadata.save('data_columns', ['Country', 'Overall rate', 'Male rate', 'Female rate'])
    data_table = soup.find("table", { "class" : "stand-alone sortable" })
    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells:
            record['Country'] = table_cells[1].text
            record['Overall rate'] = table_cells[2].text
            record['Male rate'] = table_cells[3].text
            record['Female rate'] = table_cells[4].text
            print record,"---------"
            scraperwiki.datastore.save(["Country"], record)


html = scraperwiki.scrape(website_url)         
soup = Beautifulsoup(html)
cancer(soup)