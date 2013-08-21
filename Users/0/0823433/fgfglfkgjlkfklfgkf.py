# ***********************************************************************************************************************
# This is part of my portfolio for CP4010
# Name: Olubukola Sokunbi
# Student Number: 0823433
# This scraper scrapes the site (http://www.timeshighereducation.co.uk/world-university-rankings/2010-2011/top-200.html) 
#     for world university ranking 
# ***********************************************************************************************************************

import scraperwiki
from BeautifulSoup import BeautifulSoup
html = scraperwiki.scrape('http://www.timeshighereducation.co.uk/world-university-rankings/2010-2011/top-200.html')
my_html = BeautifulSoup(html)

def my_scraper(my_html):
    scraperwiki.metadata.save('data_columns', ['WORLD RANK', 'INSTITUTION', 'COUNTRY / REGION', 'OVERALL SCORE'])     
    
    datas = my_html.findAll("tr")
    for row in datas:         
        record = {}
        cells = row.findAll("td")
        if cells:
            record['WORLD RANK'] = cells[1].text
            record['INSTITUTION'] = cells[2].text
            record['COUNTRY / REGION'] = cells[3].text
            record['OVERALL SCORE']= cells[4].text            
            
            print record    
            
            scraperwiki.datastore.save(['WORLD RANK'], record) 
    

my_scraper(my_html) #calling the function

# ****************************************************************
# Reference:
# This code is a modified version of tutorial 3 of scraperwiki
# ****************************************************************
