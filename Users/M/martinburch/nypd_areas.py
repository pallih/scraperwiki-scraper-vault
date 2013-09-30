###############################################################################
# This scraper was written to collect the area data (precicts,...) for New York 
# City Police Dept.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re

# create the db table
scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS `Areas` (`area` text,`community_affairs` text,`meeting_schedule` text)")

def parse_item(html, pattern, left_delim, right_delim):
    l = html.find(pattern)
    if (l < 0):
        return ""
    while (html[l] != left_delim):
        l = l + 1
    begin = l
    while (html[l] != right_delim):
        l = l + 1
    end = l
    return html[begin:end]

def parse_item2(html, pattern, left_delim, right_string):
    l = html.find(pattern)
    if (l < 0):
        return ""
    while (html[l] != left_delim):
        l = l + 1
    begin = l
    sa = html[begin:].split(right_string)
    return sa[0]

# scrape_table function: gets passed to an individual page to scrape
def scrape_table(html,source):

    data = {}
    area = parse_item(html, '<span class="page_subtitle">', '|', '<')[2:]
    if (area == 'Midtown South Precinct'):
        area = '14th Precinct'
    if (area == 'Midtown North Precinct'):
        area = '18th Precinct'
    if (area == 'Central Park Precinct'):
        area = '22nd Precinct'
    data['area'] = area
    data['community_affairs'] = parse_item(html, 'Community Affairs:', '(', '<')
    schedule = parse_item2(html, 'Meetings:', '>', '</span>')[2:]
    if (schedule == ""):
        schedule = parse_item2(html, 'Location and Time', '>', '&#160;&#160;</span></p></span>')[1:]
    data['meeting_schedule'] = schedule

    data['source'] = source

    l = 0
    while area[l].isdigit():
        l = l + 1;
    data['precinct'] = int(area[0:l])

    #print data
    scraperwiki.sqlite.save(unique_keys=['area'],data=data,table_name="Areas")
        
# scrape_and_look_for_next_link function: calls the scrape_table
def scrape_area_links(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    find_link = soup.findAll(href=re.compile("/precincts/"))
    for i in range(len(find_link)):
        #print find_link[i]
        next_link = find_link[i]['href']
        #print next_link
        rep_link = next_link.replace('..','http://www.nyc.gov/html/nypd/html')
        print rep_link
        areahtml = scraperwiki.scrape(rep_link)
        #print areahtml
        scrape_table(areahtml,rep_link)
    
scrape_area_links('http://www.nyc.gov/html/nypd/html/home/precincts.shtml')

###############################################################################
# This scraper was written to collect the area data (precicts,...) for New York 
# City Police Dept.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re

# create the db table
scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS `Areas` (`area` text,`community_affairs` text,`meeting_schedule` text)")

def parse_item(html, pattern, left_delim, right_delim):
    l = html.find(pattern)
    if (l < 0):
        return ""
    while (html[l] != left_delim):
        l = l + 1
    begin = l
    while (html[l] != right_delim):
        l = l + 1
    end = l
    return html[begin:end]

def parse_item2(html, pattern, left_delim, right_string):
    l = html.find(pattern)
    if (l < 0):
        return ""
    while (html[l] != left_delim):
        l = l + 1
    begin = l
    sa = html[begin:].split(right_string)
    return sa[0]

# scrape_table function: gets passed to an individual page to scrape
def scrape_table(html,source):

    data = {}
    area = parse_item(html, '<span class="page_subtitle">', '|', '<')[2:]
    if (area == 'Midtown South Precinct'):
        area = '14th Precinct'
    if (area == 'Midtown North Precinct'):
        area = '18th Precinct'
    if (area == 'Central Park Precinct'):
        area = '22nd Precinct'
    data['area'] = area
    data['community_affairs'] = parse_item(html, 'Community Affairs:', '(', '<')
    schedule = parse_item2(html, 'Meetings:', '>', '</span>')[2:]
    if (schedule == ""):
        schedule = parse_item2(html, 'Location and Time', '>', '&#160;&#160;</span></p></span>')[1:]
    data['meeting_schedule'] = schedule

    data['source'] = source

    l = 0
    while area[l].isdigit():
        l = l + 1;
    data['precinct'] = int(area[0:l])

    #print data
    scraperwiki.sqlite.save(unique_keys=['area'],data=data,table_name="Areas")
        
# scrape_and_look_for_next_link function: calls the scrape_table
def scrape_area_links(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    find_link = soup.findAll(href=re.compile("/precincts/"))
    for i in range(len(find_link)):
        #print find_link[i]
        next_link = find_link[i]['href']
        #print next_link
        rep_link = next_link.replace('..','http://www.nyc.gov/html/nypd/html')
        print rep_link
        areahtml = scraperwiki.scrape(rep_link)
        #print areahtml
        scrape_table(areahtml,rep_link)
    
scrape_area_links('http://www.nyc.gov/html/nypd/html/home/precincts.shtml')

