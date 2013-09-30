###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

def scrape_post(city,starting_url):
    
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)
#    print html

    table = soup.find('table',{'cellpadding':'3'})    
    recs = table.findAll('strong')

    for rec in recs:
        try:
            record = {'city':city, 'area':None}   
            record['area'] = rec.text                        
#            print record
            scraperwiki.datastore.save([], record)
        except:
            print 'post dropped under exceptional circumstances'
            pass



city = ['Chennai','Mumbai','Delhi-NCR','Hyderabad','Bangalore','Pune']
alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
for i in range(len(city)):
    for k in range(len(alpha)):
        scrape_post(city[i],'http://www.commonfloor.com/localities/index/city/'+city[i]+'/c/'+alpha[k])

###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

def scrape_post(city,starting_url):
    
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)
#    print html

    table = soup.find('table',{'cellpadding':'3'})    
    recs = table.findAll('strong')

    for rec in recs:
        try:
            record = {'city':city, 'area':None}   
            record['area'] = rec.text                        
#            print record
            scraperwiki.datastore.save([], record)
        except:
            print 'post dropped under exceptional circumstances'
            pass



city = ['Chennai','Mumbai','Delhi-NCR','Hyderabad','Bangalore','Pune']
alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
for i in range(len(city)):
    for k in range(len(alpha)):
        scrape_post(city[i],'http://www.commonfloor.com/localities/index/city/'+city[i]+'/c/'+alpha[k])

