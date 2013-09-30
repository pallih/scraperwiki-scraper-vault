# ***********************************************************************************************************************
# This is a test
# This scraper scrapes the site (http://www.sec.gov/Archives/edgar/data/1264314/000119312508208976/0001193125-08-208976-index.htm) 
#     for world university ranking 
# ***********************************************************************************************************************

import scraperwiki
from BeautifulSoup import BeautifulSoup
html = scraperwiki.scrape('http://www.sec.gov/Archives/edgar/data/1264314/000119312508208976/0001193125-08-208976-index.htm')
my_html = BeautifulSoup(html)

def my_scraper(my_html):
    scraperwiki.metadata.save('data_columns', ['Seq', 'Description', 'Document', 'Type', 'Size'])     
    
    datas = my_html.findAll("tr")
    for row in datas:         
        record = {}
        cells = row.findAll("td")
        if cells:
            record['Seq'] = cells[1].text
            record['Description'] = cells[2].text
            record['Document'] = cells[3].text 
            record['Type'] = cells[3].text
            record['Size'] = cells[4].text            
            
            print record    
            
            scraperwiki.datastore.save(['Seq'], record) 
    

my_scraper(my_html) #calling the function

# ****************************************************************
# Reference:
# This code is a modified version of tutorial 3 of scraperwiki
# ****************************************************************




# Blank Python
# ***********************************************************************************************************************
# This is a test
# This scraper scrapes the site (http://www.sec.gov/Archives/edgar/data/1264314/000119312508208976/0001193125-08-208976-index.htm) 
#     for world university ranking 
# ***********************************************************************************************************************

import scraperwiki
from BeautifulSoup import BeautifulSoup
html = scraperwiki.scrape('http://www.sec.gov/Archives/edgar/data/1264314/000119312508208976/0001193125-08-208976-index.htm')
my_html = BeautifulSoup(html)

def my_scraper(my_html):
    scraperwiki.metadata.save('data_columns', ['Seq', 'Description', 'Document', 'Type', 'Size'])     
    
    datas = my_html.findAll("tr")
    for row in datas:         
        record = {}
        cells = row.findAll("td")
        if cells:
            record['Seq'] = cells[1].text
            record['Description'] = cells[2].text
            record['Document'] = cells[3].text 
            record['Type'] = cells[3].text
            record['Size'] = cells[4].text            
            
            print record    
            
            scraperwiki.datastore.save(['Seq'], record) 
    

my_scraper(my_html) #calling the function

# ****************************************************************
# Reference:
# This code is a modified version of tutorial 3 of scraperwiki
# ****************************************************************




# Blank Python
