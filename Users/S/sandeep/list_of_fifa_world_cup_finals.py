# Blank Python

import scraperwiki
from BeautifulSoup import BeautifulSoup

scraperwiki.sqlite.get_var('data_columns',['rank','year','winners','Final score',' Runner up','venue','location',])

def scrape_table(soup):
    data_table = soup.find("table",{"class":"wikitable sortable"})
    rows1 = data_table.findAll("tbody")

    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells:
            record['rank'] = table_cells[0].text
            record['year'] = table_cells[1].text
            record['winners'] = table_cells[2].text
            record['Final score'] = table_cells[3].text
            record['Runner up'] = table_cells[4].text
            record['venue'] = table_cells[5].text
            record['location'] = table_cells[6].text
            
            
            print record,'------------'
            scraperwiki.datastore.save(["rank"], record)
        

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)
    


starting_url =  "http://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals"
scrape_and_look_for_next_link(starting_url)
# Blank Python

import scraperwiki
from BeautifulSoup import BeautifulSoup

scraperwiki.sqlite.get_var('data_columns',['rank','year','winners','Final score',' Runner up','venue','location',])

def scrape_table(soup):
    data_table = soup.find("table",{"class":"wikitable sortable"})
    rows1 = data_table.findAll("tbody")

    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells:
            record['rank'] = table_cells[0].text
            record['year'] = table_cells[1].text
            record['winners'] = table_cells[2].text
            record['Final score'] = table_cells[3].text
            record['Runner up'] = table_cells[4].text
            record['venue'] = table_cells[5].text
            record['location'] = table_cells[6].text
            
            
            print record,'------------'
            scraperwiki.datastore.save(["rank"], record)
        

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)
    


starting_url =  "http://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals"
scrape_and_look_for_next_link(starting_url)
