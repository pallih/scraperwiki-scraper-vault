import scraperwiki
import re
from BeautifulSoup import BeautifulSoup


days = 'Mon|Tue|Wed|Thu|Fri|Sat|Sun|Tues|Monday|Friday|Saturday|Sunday|Thur'

short_days = [['Mon', 'Monday'], ['Tue', 'Tues'], ['Wed'], ['Thu', 'Thur'], ['Fri', 'Friday'], ['Sat', 'Saturday'], ['Sun', 'Sunday']]
simple_days = [i[0] for i in short_days]

scraperwiki.metadata.save('data_columns', ['name', 'address', 'postcode', 'lat', 'lng', 'phone', 'email', 'url', 'facilities', 'services'] + simple_days)

#DO NOT READ - DANGER OF DEATH
#This converts a natural date and time range into
#  start_date, end_date, start_time, end_time
opening_time_re = re.compile('(%s) ?[-&/]? ?(%s)?\s?(\d{1,2}(?:\.\d\d)?(?:a|p)?m?) ?-? ?(\d{1,2}(?:\.\d\d)?(?:a|p)?m?)'%(days, days))


def split_facilities_list(fac):
    # remove the section title from the start of the record
    return fac[fac.find(':')+1:]
    

def opening_times(block):
    matched = opening_time_re.match(block.strip())
    if matched:
        first_date, last_date, opentime, close_time = matched.groups()
        flag = False
        for i in short_days:
            if first_date in i:
                 flag = True
            if flag:
                yield i[0], opentime, close_time
            if last_date in i or (flag and not last_date):
                break
        
    
def parse_leisure_center_page(url, record):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    core_soup = soup.find('div', {'id': 'content'})
    
    a_email = core_soup.find('a', {'class': 'email'})
    record['email'] = a_email.text if a_email else None
    
    
    div_facilities = core_soup.find('div', {'class': 'facilities'})
    if div_facilities:
        record['facilities'] = split_facilities_list(div_facilities.text)
    else:
        record['facilities'] = None
    
    div_Services = core_soup.find('div', {'class': 'services'})
    if div_Services:
        record['services'] = split_facilities_list(div_Services.text)
    else:
        record['services'] = None

    for i in simple_days:
        record[i] = 'closed'
    div_opening = core_soup.find('div', {'class': 'opening'})
    if div_opening:
        opening_text = div_opening.text
        for a_period in opening_text[opening_text.find(':')+1:].split(','):
            for day, open_time, close_time in opening_times(a_period):
                record[day] = '%s - %s'%(open_time, close_time)
    print ', '.join(record[day] for day in simple_days)
    

def parse_page(soup):
    trs = soup.findAll('tr')

    for tr in trs:
        tds = tr.findAll('td')
        if tds:
            record = {}
            record['name'] = tds[0].text
            link = tds[0].find('a')['href']
            record['url'] = base_url + link
            address =  tds[1].text
            record['address'] = address
            postcode = scraperwiki.geo.extract_gb_postcode(address)
            record['postcode'] = postcode
            if postcode:
                try:
                    record['lat'], record['lng'] = scraperwiki.geo.gb_postcode_to_latlng(postcode)
                except TypeError:
                    record['lat'], record['lng'] = None, None
            else:
                record['lat'], record['lng'] = None, None
            record['phone'] = tds[2].text
            parse_leisure_center_page(base_url + link, record)
            scraperwiki.datastore.save(["name"], record)

            
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    print url
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    parse_page(soup)
    all_links = soup.findAll("a")
    for i in all_links:
        if 'Next' in i.contents:
            next_link = i
            next_url = base_url + next_link['href']
            scrape_and_look_for_next_link(next_url)
        
base_url = 'http://birmingham.gov.uk'
starting_url = base_url + """/cs/Satellite?pagename=BCC/Common/Wrapper/Wrapper&childpagename=SystemAdmin/PageLayout&c=Page&cid=1186481130144&searchPageId=1223115664505&searchForm=1&pagination=1&entityname=&entitykeywords=&entitytype=Venue&entityarea=Any&entityfacilities=Leisure+Centre&entityservices=Any&search=Search"""
scrape_and_look_for_next_link(starting_url)
import scraperwiki
import re
from BeautifulSoup import BeautifulSoup


days = 'Mon|Tue|Wed|Thu|Fri|Sat|Sun|Tues|Monday|Friday|Saturday|Sunday|Thur'

short_days = [['Mon', 'Monday'], ['Tue', 'Tues'], ['Wed'], ['Thu', 'Thur'], ['Fri', 'Friday'], ['Sat', 'Saturday'], ['Sun', 'Sunday']]
simple_days = [i[0] for i in short_days]

scraperwiki.metadata.save('data_columns', ['name', 'address', 'postcode', 'lat', 'lng', 'phone', 'email', 'url', 'facilities', 'services'] + simple_days)

#DO NOT READ - DANGER OF DEATH
#This converts a natural date and time range into
#  start_date, end_date, start_time, end_time
opening_time_re = re.compile('(%s) ?[-&/]? ?(%s)?\s?(\d{1,2}(?:\.\d\d)?(?:a|p)?m?) ?-? ?(\d{1,2}(?:\.\d\d)?(?:a|p)?m?)'%(days, days))


def split_facilities_list(fac):
    # remove the section title from the start of the record
    return fac[fac.find(':')+1:]
    

def opening_times(block):
    matched = opening_time_re.match(block.strip())
    if matched:
        first_date, last_date, opentime, close_time = matched.groups()
        flag = False
        for i in short_days:
            if first_date in i:
                 flag = True
            if flag:
                yield i[0], opentime, close_time
            if last_date in i or (flag and not last_date):
                break
        
    
def parse_leisure_center_page(url, record):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    core_soup = soup.find('div', {'id': 'content'})
    
    a_email = core_soup.find('a', {'class': 'email'})
    record['email'] = a_email.text if a_email else None
    
    
    div_facilities = core_soup.find('div', {'class': 'facilities'})
    if div_facilities:
        record['facilities'] = split_facilities_list(div_facilities.text)
    else:
        record['facilities'] = None
    
    div_Services = core_soup.find('div', {'class': 'services'})
    if div_Services:
        record['services'] = split_facilities_list(div_Services.text)
    else:
        record['services'] = None

    for i in simple_days:
        record[i] = 'closed'
    div_opening = core_soup.find('div', {'class': 'opening'})
    if div_opening:
        opening_text = div_opening.text
        for a_period in opening_text[opening_text.find(':')+1:].split(','):
            for day, open_time, close_time in opening_times(a_period):
                record[day] = '%s - %s'%(open_time, close_time)
    print ', '.join(record[day] for day in simple_days)
    

def parse_page(soup):
    trs = soup.findAll('tr')

    for tr in trs:
        tds = tr.findAll('td')
        if tds:
            record = {}
            record['name'] = tds[0].text
            link = tds[0].find('a')['href']
            record['url'] = base_url + link
            address =  tds[1].text
            record['address'] = address
            postcode = scraperwiki.geo.extract_gb_postcode(address)
            record['postcode'] = postcode
            if postcode:
                try:
                    record['lat'], record['lng'] = scraperwiki.geo.gb_postcode_to_latlng(postcode)
                except TypeError:
                    record['lat'], record['lng'] = None, None
            else:
                record['lat'], record['lng'] = None, None
            record['phone'] = tds[2].text
            parse_leisure_center_page(base_url + link, record)
            scraperwiki.datastore.save(["name"], record)

            
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    print url
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    parse_page(soup)
    all_links = soup.findAll("a")
    for i in all_links:
        if 'Next' in i.contents:
            next_link = i
            next_url = base_url + next_link['href']
            scrape_and_look_for_next_link(next_url)
        
base_url = 'http://birmingham.gov.uk'
starting_url = base_url + """/cs/Satellite?pagename=BCC/Common/Wrapper/Wrapper&childpagename=SystemAdmin/PageLayout&c=Page&cid=1186481130144&searchPageId=1223115664505&searchForm=1&pagination=1&entityname=&entitykeywords=&entitytype=Venue&entityarea=Any&entityfacilities=Leisure+Centre&entityservices=Any&search=Search"""
scrape_and_look_for_next_link(starting_url)
