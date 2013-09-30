import scraperwiki
import BeautifulSoup

from scraperwiki import sqlite
from time import gmtime, strftime

# Met Police Safer Neighbourhood Priorities by ward #

# example page:  http://content.met.police.uk/Page/TeamFinder?scope_id=1257246763496
#                http://content.met.police.uk/Team/Barking/Abbey

# the priority pages for another police force are seen here
# http://www.westyorkshire.police.uk/npt/area.asp?id=50#150

# Clean up for database
#scraperwiki.sqlite.execute("delete from swdata where (priority || date_scraped || ward || borough) in (select priority || min(date_scraped) || ward || borough from swdata group by borough, ward, priority having count(priority) > 1)")
#scraperwiki.sqlite.commit()
#scraperwiki.sqlite.execute("delete from swdata where borough like 'Hamm%' and borough not like 'Hammersmith &%' and priority || ward in (select priority || ward from swdata where borough = 'Hammersmith & Fulham')")
#scraperwiki.sqlite.execute("update swdata set borough = 'Hammersmith & Fulham' where borough like 'Hamm%'")
#scraperwiki.sqlite.commit()


base_url = 'http://content.met.police.uk'
all_boroughs_url = '/Page/AllBoroughs'

def save_priority (borough, ward, priority):
    
    data = {
        'borough' : borough,
        'ward' : ward,
        'priority' : priority,
        'date_scraped' : strftime("%Y-%m-%d %H:%M:%S", gmtime()),
        }
    print data
    sqlite.save(unique_keys=['borough', 'ward', 'priority'], data=data)    


def get_borough_list ():
    
    boroughs = []
    home_html = scraperwiki.scrape(base_url + all_boroughs_url)
    home_page = BeautifulSoup.BeautifulSoup(home_html)
    
    borough_divs = home_page.find('div', {'id': 'content'}).findAll('div', {'id': True})
    
    for borough_div in borough_divs:
        borough_short_name = borough_div['id']
        borough_url = borough_div.findAll('li')[2].find('a')['href']
        borough_name = borough_div.find('h3').find('a').string.replace('&#38;', '&').replace(' and ', ' & ')
        boroughs.append({'borough_short_name': borough_short_name,'borough_name': borough_name,'borough_url': borough_url})

    return boroughs


def get_borough_wards(borough_url):
    wards = []
    borough_html = scraperwiki.scrape(base_url + borough_url)
    borough_page = BeautifulSoup.BeautifulSoup(borough_html)

    for ward_li in borough_page.findAll('div', {'class': 'mod-main'})[0].findAll('li'):
        ward_name = ward_li.find('a').string.replace('&amp;', '&')
        ward_url = ward_li.find('a')['href']
        wards.append({'ward_name': ward_name, 'ward_url': ward_url})
    
    return wards

def get_ward_priorities(ward_url):
    
    priorities = []
    ward_html = scraperwiki.scrape(base_url + ward_url)
    ward_page = BeautifulSoup.BeautifulSoup(ward_html)
    
    priority_ul = ward_page.find('div', {'class': 'mod-main'}).find('ul').findAll('li')
    for priority_li in priority_ul:
        priorities.append(priority_li.string)
        print priority_li 
    return priorities

def run_scraper():
    
    borough_list = get_borough_list()
    
    for borough in borough_list:
        
        ward_list = get_borough_wards(borough['borough_url'])
        for ward in ward_list:          
            ward_priorities = get_ward_priorities(ward['ward_url'])
            for ward_priority in ward_priorities:
                print borough['borough_name'], ward['ward_name'], ward_priority
                save_priority(borough['borough_name'], ward['ward_name'], ward_priority)

run_scraper()


import scraperwiki
import BeautifulSoup

from scraperwiki import sqlite
from time import gmtime, strftime

# Met Police Safer Neighbourhood Priorities by ward #

# example page:  http://content.met.police.uk/Page/TeamFinder?scope_id=1257246763496
#                http://content.met.police.uk/Team/Barking/Abbey

# the priority pages for another police force are seen here
# http://www.westyorkshire.police.uk/npt/area.asp?id=50#150

# Clean up for database
#scraperwiki.sqlite.execute("delete from swdata where (priority || date_scraped || ward || borough) in (select priority || min(date_scraped) || ward || borough from swdata group by borough, ward, priority having count(priority) > 1)")
#scraperwiki.sqlite.commit()
#scraperwiki.sqlite.execute("delete from swdata where borough like 'Hamm%' and borough not like 'Hammersmith &%' and priority || ward in (select priority || ward from swdata where borough = 'Hammersmith & Fulham')")
#scraperwiki.sqlite.execute("update swdata set borough = 'Hammersmith & Fulham' where borough like 'Hamm%'")
#scraperwiki.sqlite.commit()


base_url = 'http://content.met.police.uk'
all_boroughs_url = '/Page/AllBoroughs'

def save_priority (borough, ward, priority):
    
    data = {
        'borough' : borough,
        'ward' : ward,
        'priority' : priority,
        'date_scraped' : strftime("%Y-%m-%d %H:%M:%S", gmtime()),
        }
    print data
    sqlite.save(unique_keys=['borough', 'ward', 'priority'], data=data)    


def get_borough_list ():
    
    boroughs = []
    home_html = scraperwiki.scrape(base_url + all_boroughs_url)
    home_page = BeautifulSoup.BeautifulSoup(home_html)
    
    borough_divs = home_page.find('div', {'id': 'content'}).findAll('div', {'id': True})
    
    for borough_div in borough_divs:
        borough_short_name = borough_div['id']
        borough_url = borough_div.findAll('li')[2].find('a')['href']
        borough_name = borough_div.find('h3').find('a').string.replace('&#38;', '&').replace(' and ', ' & ')
        boroughs.append({'borough_short_name': borough_short_name,'borough_name': borough_name,'borough_url': borough_url})

    return boroughs


def get_borough_wards(borough_url):
    wards = []
    borough_html = scraperwiki.scrape(base_url + borough_url)
    borough_page = BeautifulSoup.BeautifulSoup(borough_html)

    for ward_li in borough_page.findAll('div', {'class': 'mod-main'})[0].findAll('li'):
        ward_name = ward_li.find('a').string.replace('&amp;', '&')
        ward_url = ward_li.find('a')['href']
        wards.append({'ward_name': ward_name, 'ward_url': ward_url})
    
    return wards

def get_ward_priorities(ward_url):
    
    priorities = []
    ward_html = scraperwiki.scrape(base_url + ward_url)
    ward_page = BeautifulSoup.BeautifulSoup(ward_html)
    
    priority_ul = ward_page.find('div', {'class': 'mod-main'}).find('ul').findAll('li')
    for priority_li in priority_ul:
        priorities.append(priority_li.string)
        print priority_li 
    return priorities

def run_scraper():
    
    borough_list = get_borough_list()
    
    for borough in borough_list:
        
        ward_list = get_borough_wards(borough['borough_url'])
        for ward in ward_list:          
            ward_priorities = get_ward_priorities(ward['ward_url'])
            for ward_priority in ward_priorities:
                print borough['borough_name'], ward['ward_name'], ward_priority
                save_priority(borough['borough_name'], ward['ward_name'], ward_priority)

run_scraper()


