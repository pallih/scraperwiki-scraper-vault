###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

def scrape_list(indus, starting_url):
    print starting_url
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)
    #print html
#Rank    Company    Country    Sales    Profits    Assets    Market Value
    rows = soup.findAll('tr',{'style': 'cursor: pointer;'}) 
    for row in rows:
        record = {'rank':None, 'company':None,'company_url':None, 'country':None, 'sales':None, 'profit':None, 'assets':None, 'market_value':None,'industry':None}
        record['industry'] = indus
        record['rank'] = row.find('td',{'class':'rank'}).text
        company = row.find('td',{'class':'company'})
        record['company'] = company.text
        record['company_url'] = company.find('a')
        
        record['country'] = row.findAll('td')[2].text

        metric = row.findAll('td',{'class':'nowrap'})
        #print metric
        record['sales'] = metric[0].text
        record['profit'] = metric[1].text
        record['assets'] = metric[2].text
        record['market_value'] = metric[3].text

        print record
        scraperwiki.sqlite.save(unique_keys=['rank','company'], data=record)

#    table = soup.find('table',{'cellpadding':'3'})    
#    recs = table.findAll('strong')

#    for rec in recs:
#        try:
#            record = {'city':city, 'area':None}   
#            record['area'] = rec.text                        
#            print record
#            scraperwiki.datastore.save([], record)
#        except:
#            print 'post dropped under exceptional circumstances'
#            pass


#http://www.forbes.com/global2000/list?page=1
industry=['Advertising','Aerospace%20%26%20Defense','Air%20Courier','Airline','Aluminum','Apparel-Accessories','Apparel-Footwear%20Retail','Auto%20%26%20Truck%20Manufacturers','Auto%20%26%20Truck%20Parts','Beverages','Biotechs','Broadcasting%20%26%20Cable','Business%20%26%20Personal%20Services','Business%20Products%20%26%20Supplies','Casinos%20%26%20Gaming','Communications%20Equipment','Computer%20%26%20Electronics%20Retail','Computer%20Hardware','Computer%20Services','Computer%20Storage%20Devices','Conglomerates','Construction%20Materials','Construction%20Services','Consumer%20Electronics','Consumer%20Financial%20Services','Containers%20%26%20Packaging','Department%20Stores','Discount%20Stores','Diversified%20Chemicals','Diversified%20Insurance','Diversified%20Metals%20%26%20Mining','Diversified%20Utilities','Drug%20Retail','Electric%20Utilities','Electrical%20Equipment','Electronics','Environmental%20%26%20Waste','Food%20Processing','Food%20Retail','Forest%20Products','Furniture%20%26%20Fixtures','Healthcare%20Services','Heavy%20Equipment','Home%20Improvement%20Retail','Hotels%20%26%20Motels','Household%20Appliances','Household-Personal%20Care','Insurance%20Brokers','Internet%20%26%20Catalog%20Retail','Investment%20Services','Iron%20%26%20Steel','Life%20%26%20Health%20Insurance','Major%20Banks','Managed%20Health%20Care','Medical%20Equipment%20%26%20Supplies','Natural%20Gas%20Utilities','Oil%20%26%20Gas%20Operations','Oil%20Services%20%26%20Equipment','Other%20Industrial%20Equipment','Other%20Tranportation','Paper%20%26%20Paper%20Products','Pharmaceuticals','Precision%20Healthcare%20Equipment','Printing%20%26%20Publishing','Property%20%26%20Casualty%20Insurance','Railroads','Real%20Estate','Recreational%20Products','Regional%20Banks','Rental%20%26%20Leasing','Restaurants','Security%20Systems','Semiconductors','Software%20%26%20Programming','Specialized%20Chemicals','Specialty%20Stores','Telecommunications%20services','Thrifts%20%26%20Mortgage%20Finance','Tobacco','Trading%20Companies','Trucking']

for i in range(len(industry)):
    scrape_list(industry[i],'http://www.forbes.com/global2000/list?industry='+industry[i])


###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

def scrape_list(indus, starting_url):
    print starting_url
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)
    #print html
#Rank    Company    Country    Sales    Profits    Assets    Market Value
    rows = soup.findAll('tr',{'style': 'cursor: pointer;'}) 
    for row in rows:
        record = {'rank':None, 'company':None,'company_url':None, 'country':None, 'sales':None, 'profit':None, 'assets':None, 'market_value':None,'industry':None}
        record['industry'] = indus
        record['rank'] = row.find('td',{'class':'rank'}).text
        company = row.find('td',{'class':'company'})
        record['company'] = company.text
        record['company_url'] = company.find('a')
        
        record['country'] = row.findAll('td')[2].text

        metric = row.findAll('td',{'class':'nowrap'})
        #print metric
        record['sales'] = metric[0].text
        record['profit'] = metric[1].text
        record['assets'] = metric[2].text
        record['market_value'] = metric[3].text

        print record
        scraperwiki.sqlite.save(unique_keys=['rank','company'], data=record)

#    table = soup.find('table',{'cellpadding':'3'})    
#    recs = table.findAll('strong')

#    for rec in recs:
#        try:
#            record = {'city':city, 'area':None}   
#            record['area'] = rec.text                        
#            print record
#            scraperwiki.datastore.save([], record)
#        except:
#            print 'post dropped under exceptional circumstances'
#            pass


#http://www.forbes.com/global2000/list?page=1
industry=['Advertising','Aerospace%20%26%20Defense','Air%20Courier','Airline','Aluminum','Apparel-Accessories','Apparel-Footwear%20Retail','Auto%20%26%20Truck%20Manufacturers','Auto%20%26%20Truck%20Parts','Beverages','Biotechs','Broadcasting%20%26%20Cable','Business%20%26%20Personal%20Services','Business%20Products%20%26%20Supplies','Casinos%20%26%20Gaming','Communications%20Equipment','Computer%20%26%20Electronics%20Retail','Computer%20Hardware','Computer%20Services','Computer%20Storage%20Devices','Conglomerates','Construction%20Materials','Construction%20Services','Consumer%20Electronics','Consumer%20Financial%20Services','Containers%20%26%20Packaging','Department%20Stores','Discount%20Stores','Diversified%20Chemicals','Diversified%20Insurance','Diversified%20Metals%20%26%20Mining','Diversified%20Utilities','Drug%20Retail','Electric%20Utilities','Electrical%20Equipment','Electronics','Environmental%20%26%20Waste','Food%20Processing','Food%20Retail','Forest%20Products','Furniture%20%26%20Fixtures','Healthcare%20Services','Heavy%20Equipment','Home%20Improvement%20Retail','Hotels%20%26%20Motels','Household%20Appliances','Household-Personal%20Care','Insurance%20Brokers','Internet%20%26%20Catalog%20Retail','Investment%20Services','Iron%20%26%20Steel','Life%20%26%20Health%20Insurance','Major%20Banks','Managed%20Health%20Care','Medical%20Equipment%20%26%20Supplies','Natural%20Gas%20Utilities','Oil%20%26%20Gas%20Operations','Oil%20Services%20%26%20Equipment','Other%20Industrial%20Equipment','Other%20Tranportation','Paper%20%26%20Paper%20Products','Pharmaceuticals','Precision%20Healthcare%20Equipment','Printing%20%26%20Publishing','Property%20%26%20Casualty%20Insurance','Railroads','Real%20Estate','Recreational%20Products','Regional%20Banks','Rental%20%26%20Leasing','Restaurants','Security%20Systems','Semiconductors','Software%20%26%20Programming','Specialized%20Chemicals','Specialty%20Stores','Telecommunications%20services','Thrifts%20%26%20Mortgage%20Finance','Tobacco','Trading%20Companies','Trucking']

for i in range(len(industry)):
    scrape_list(industry[i],'http://www.forbes.com/global2000/list?industry='+industry[i])


