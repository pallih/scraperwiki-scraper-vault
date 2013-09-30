###############################################################################
#
# Rochester, MI shops
#
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.downtownrochestermi.com/business-directory/'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)
    
#get all business listings 
#div = soup.find('div', {'id':'listings'}) 

div = soup.find('div', {'id':'listings'})
print div
print type(div)
businesses = div.findAll('div', {'class':'listing'})

print businesses
print type(businesses)

#for business in businesses[1:]:
#    business_name = ''
#    category = ''
#    phone_num = ''
#    business_site = ''
#    address = ''
#    
#    business_name = business.find('h3')
#    category = business.find('field-value')
    
#    record = { 
#        'business_name' : business_name ,
#        'category' : category ,
#        'phone_num' : phone_num ,
#        'business_site' : business_site ,
#        'address' : address 
#    }
#    scraperwiki.datastore.save(['business_name'],record)

    ###############################################################################
#
# Rochester, MI shops
#
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.downtownrochestermi.com/business-directory/'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)
    
#get all business listings 
#div = soup.find('div', {'id':'listings'}) 

div = soup.find('div', {'id':'listings'})
print div
print type(div)
businesses = div.findAll('div', {'class':'listing'})

print businesses
print type(businesses)

#for business in businesses[1:]:
#    business_name = ''
#    category = ''
#    phone_num = ''
#    business_site = ''
#    address = ''
#    
#    business_name = business.find('h3')
#    category = business.find('field-value')
    
#    record = { 
#        'business_name' : business_name ,
#        'category' : category ,
#        'phone_num' : phone_num ,
#        'business_site' : business_site ,
#        'address' : address 
#    }
#    scraperwiki.datastore.save(['business_name'],record)

    