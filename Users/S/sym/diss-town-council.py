import scraperwiki
from scraperwiki import datastore
import BeautifulSoup
import re

page = scraperwiki.scrape('http://www.disscouncil.com/councillor-information.php')
page = BeautifulSoup.BeautifulSoup(page)

for councillor in page.findAll('div', {'class' : 'councillors'}):
    c_info = councillor.findAll('p', {'class' : 'name'})[0].string
    c_name_role = c_info.split('-')
    if len(c_name_role) >= 2:
        c_name = c_name_role[1]
        c_role = re.sub('\&amp;', '&', c_name_role[0]) 
    else:
        c_name = c_name_role[0]
        c_role = ""
    data = {
            'name' : str(c_name),
            'role' : c_role,
            }
    print data
    datastore.save(unique_keys=['name'], data=data)

    
