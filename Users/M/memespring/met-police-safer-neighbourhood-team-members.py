import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

# Met Police Safer Neighbourhood Team Members #

base_url = 'http://www.met.police.uk/'

#get list of boroughs
home_html = scraperwiki.scrape(base_url)
home_page = BeautifulSoup.BeautifulSoup(home_html)

for home_option in  home_page.find('form', {'name': 'localpoliceform'}).find('select').findAll('option')[1:]:

    #scrape borough page
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

            #Get the members of the team. Not all wards have photos
            has_images = False
            members = ward_page.find('ul', {'class': 'jcarousel-skin-tango'})
            if members:
                has_images = True
                members = members.findAll('li')
            else:
                members = ward_page.find('div', {'class': 'metSNMembers'}).findAll('li')                
            if members:
                for member_li in members:
                    rank =  member_li.acronym['title']
                    officer_name =  member_li.contents[-1]
                    if has_images:
                        photo_url = member_li.img['style'].replace('background:URL(../../', 'http://www.met.police.uk/teams/').replace(') no-repeat 0.4em','')

                    else:
                        photo_url = None

                    #save to datastore
                    data = {
                            'borough' : borough_name,
                            'ward' : ward_name,
                            'officer_name' : officer_name,
                            'rank': rank,
                            'photo_url': photo_url
                            }
                    datastore.save(unique_keys=['borough', 'ward', 'officer_name'], data=data)

import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

# Met Police Safer Neighbourhood Team Members #

base_url = 'http://www.met.police.uk/'

#get list of boroughs
home_html = scraperwiki.scrape(base_url)
home_page = BeautifulSoup.BeautifulSoup(home_html)

for home_option in  home_page.find('form', {'name': 'localpoliceform'}).find('select').findAll('option')[1:]:

    #scrape borough page
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

            #Get the members of the team. Not all wards have photos
            has_images = False
            members = ward_page.find('ul', {'class': 'jcarousel-skin-tango'})
            if members:
                has_images = True
                members = members.findAll('li')
            else:
                members = ward_page.find('div', {'class': 'metSNMembers'}).findAll('li')                
            if members:
                for member_li in members:
                    rank =  member_li.acronym['title']
                    officer_name =  member_li.contents[-1]
                    if has_images:
                        photo_url = member_li.img['style'].replace('background:URL(../../', 'http://www.met.police.uk/teams/').replace(') no-repeat 0.4em','')

                    else:
                        photo_url = None

                    #save to datastore
                    data = {
                            'borough' : borough_name,
                            'ward' : ward_name,
                            'officer_name' : officer_name,
                            'rank': rank,
                            'photo_url': photo_url
                            }
                    datastore.save(unique_keys=['borough', 'ward', 'officer_name'], data=data)

