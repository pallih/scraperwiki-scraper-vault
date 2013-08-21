# Blank Python


import scraperwiki
from BeautifulSoup import BeautifulSoup


#define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Page Name', 'Fans'])

#scrape the fan section
def scrape_fans(soup):
    data_table = soup.find("table",{ "class" : "uiGrid"})  #find the pages with most fans section 
    rows= data_table.findAll("tr") #find all the table rows
    for row in rows: #loop through the rows
        cells = row.findAll("td") #find all the cells
        for cell in cells: #loop through the cells
            #setup the data record
            record={} 
            table_cells=cell.findAll("p") #find all the p items
            if table_cells: #if the item exists store it
                record['Page Name'] = table_cells[0].text
                record['Fans'] = table_cells[1].text[:-5]
                scraperwiki.datastore.save(["Page Name"], record)


def scrape_page(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    #print soup.prettify()
    link_table=soup.find("div", {"class" : "alphabet_list clearfix"})
    #next_link=soup.findAll("a")
    for link in link_table:
        next_url=link['href']
        #print next_url
        html1 = scraperwiki.scrape(next_url)
        soup1 = BeautifulSoup(html1)
        scrape_fans(soup1)   
    

#setup the base url
base_url = 'http://facebook.com/directory/pages/'
#setup the startup url 



#call the scraping function
scrape_page(base_url)
