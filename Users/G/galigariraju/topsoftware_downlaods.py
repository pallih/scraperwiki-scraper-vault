import scraperwiki
from BeautifulSoup import BeautifulSoup


scraperwiki.metadata.save('data_columns', ['Rank', 'Project Name', 'Downloads', 'Last Rank','Change'])


def scrape_table(soup):
    data_table = soup.find("table")
    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            
            record['Rank'] = table_cells[0].text
            record['Project Name'] = table_cells[1].text
            record['Downloads'] = table_cells[2].text
            record['Last Rank'] = table_cells[3].text
            record['Change'] = table_cells[4].text
            
            print record, '------------'
            scraperwiki.datastore.save(["Project Name"], record)
        

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)


starting_url =  'http://sourceforge.net/top/toplist.php'
scrape_and_look_for_next_link(starting_url)