import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

# Met Police Safer Neighbourhood Team Members   #

base_url = 'http://www.met.police.uk/'

#get list of boroughs
home_html = scraperwiki.scrape(base_url)
home_page = BeautifulSoup.BeautifulSoup(home_html) 



for home_option in  home_page.find('form', {'name': 'localpoliceform'}).find('select').findAll('option')[1:]:


    #scrape borough page
    borough_short_name = home_option['value']
    
    if borough_short_name!= 'heathrow':

        #handle special case of hammersmith
        if borough_short_name.startswith('http'):
            borough_short_name = borough_short_name.replace('http://cms.met.police.uk/met/boroughs/', '').replace('/index', '')
            
        #special case hammersmithandfulham
        if borough_short_name == 'hammersmith':
            borough_short_name = 'hammersmithandfulham'            

        borough_name = home_option.string.replace('&amp;', '&')

    
        borough_html = scraperwiki.scrape(base_url + '/teams/' + borough_short_name + '/index.php')
        borough_page = BeautifulSoup.BeautifulSoup(borough_html)


        #find links to ward pages
        for ward_li in borough_page.findAll('div', {'class': 'metSNTeamList'})[0].findAll('li'):
            ward_url = base_url + 'teams/' + borough_short_name + '/'+ ward_li.find('a')['href']
            ward_name = ward_li.find('a').string
            ward_html = scraperwiki.scrape(ward_url)
            ward_page = BeautifulSoup.BeautifulSoup(ward_html)
        
            #address
            address_block = ward_page.find('div', {'class': 'metSNAddress'}).find('p')
            address = ''
            for line in address_block.contents:
                if line.string != None and line.string.strip() != '':
                    if address == '':
                        address = line.string
                    else:
                        address = address + ', ' + line.string
                
            address = address.rstrip(' ,')

            #phone
            phone = ''
            mobile_phone = ''
            phone_numbers = ward_page.find('div', {'class': 'metSNPhone'}).ul.findAll('li')
            if len(phone_numbers) > 0:
                phone = phone_numbers[0].string
            if len(phone_numbers) > 1:
                mobile_phone = phone_numbers[1].string


            #save to datastore
            data = {
                    'borough' : borough_name,
                    'ward' : ward_name,
                    'address' : address,
                    'phone': phone,
                    'mobile_phone': mobile_phone
                    }
            datastore.save(unique_keys=['borough', 'ward'], data=data)




