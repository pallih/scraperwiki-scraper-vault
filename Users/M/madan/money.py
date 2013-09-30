import scraperwiki
from BeautifulSoup import BeautifulSoup


scraperwiki.metadata.save('data_columns', ['Company', 'Live Price', 'Change', 'Volume','High','Low','Bid Price','Bid Qty','OfferPrice','Offer Qty'])

def scrape_table(soup):
    data_table = soup.find("table",  "references")
    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            
            record['Company'] = table_cells[0].text
            record['Live Price'] = table_cells[1].text
            record['Change'] = table_cells[2].text
            record['Volume'] = table_cells[3].text
            record['High'] = table_cells[4].text
            record['Low'] = table_cells[5].text
            record['Bid Price'] = table_cells[6].text
            record['Bid Qty'] = table_cells[7].text 
            record['OfferPrice'] = table_cells[8].text
            record['Offer Qty'] = table_cells[9].text
            print record, '------------'
            scraperwiki.datastore.save(["Project Name"], record)
        

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)


starting_url =  'http://www.moneycontrol.com/watchlist1/last_visited_fullview.php'
scrape_and_look_for_next_link(starting_url)
import scraperwiki
from BeautifulSoup import BeautifulSoup


scraperwiki.metadata.save('data_columns', ['Company', 'Live Price', 'Change', 'Volume','High','Low','Bid Price','Bid Qty','OfferPrice','Offer Qty'])

def scrape_table(soup):
    data_table = soup.find("table",  "references")
    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            
            record['Company'] = table_cells[0].text
            record['Live Price'] = table_cells[1].text
            record['Change'] = table_cells[2].text
            record['Volume'] = table_cells[3].text
            record['High'] = table_cells[4].text
            record['Low'] = table_cells[5].text
            record['Bid Price'] = table_cells[6].text
            record['Bid Qty'] = table_cells[7].text 
            record['OfferPrice'] = table_cells[8].text
            record['Offer Qty'] = table_cells[9].text
            print record, '------------'
            scraperwiki.datastore.save(["Project Name"], record)
        

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)


starting_url =  'http://www.moneycontrol.com/watchlist1/last_visited_fullview.php'
scrape_and_look_for_next_link(starting_url)
