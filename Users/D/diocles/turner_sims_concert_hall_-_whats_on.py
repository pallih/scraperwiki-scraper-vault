import scraperwiki
from BeautifulSoup import BeautifulSoup

import pytz
from datetime import datetime

# scrape_table function: gets passed an individual page to scrape
def scrape_page(soup, current):
    sectors = soup.findAll(attrs={'class':'sector'})
    
    for sector in sectors:
        event = {}
        parent = sector.parent
        
        event['title'] = parent.h3.text

        url = "http://www.turnersims.co.uk" + parent.h3.a['href']
        event['url'] = url

        html = scraperwiki.scrape(url)
        subsoup = BeautifulSoup(html)

        when = subsoup.find(attrs={'class':'date'}).text
        when = datetime.strptime(when, "%A %d %B, %I:%M %p")
        when = when.replace(year=current['year'])

        # We assume here they won't publish things more than 6 months
        # in the past or in the future.
        if when.month - current['month'] >= 6 :
            when = when.replace(year=current['year']-1)
        elif current['month'] - when.month >= 6:
            when = when.replace(year=current['year']+1)

        event['datetime'] = pytz.timezone('Europe/London').localize(when)
        
        scraperwiki.sqlite.save(["url"], event) # save the records one by one

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url, current):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_page(soup, current)
    next_link = soup.find("a", { "class" : "next" })

    if next_link:
        next_url = "http://www.turnersims.co.uk" + next_link['href']

        scrape_and_look_for_next_link(next_url, current)

london = pytz.timezone('Europe/London')

now_utc = datetime.now(pytz.timezone('UTC'))
now_tz = now_utc.astimezone(london)

current = {}
current['year'] = now_tz.year
current['month'] = now_tz.month

base_url = 'http://www.turnersims.co.uk/upcoming-events'
scrape_and_look_for_next_link(base_url, current)
import scraperwiki
from BeautifulSoup import BeautifulSoup

import pytz
from datetime import datetime

# scrape_table function: gets passed an individual page to scrape
def scrape_page(soup, current):
    sectors = soup.findAll(attrs={'class':'sector'})
    
    for sector in sectors:
        event = {}
        parent = sector.parent
        
        event['title'] = parent.h3.text

        url = "http://www.turnersims.co.uk" + parent.h3.a['href']
        event['url'] = url

        html = scraperwiki.scrape(url)
        subsoup = BeautifulSoup(html)

        when = subsoup.find(attrs={'class':'date'}).text
        when = datetime.strptime(when, "%A %d %B, %I:%M %p")
        when = when.replace(year=current['year'])

        # We assume here they won't publish things more than 6 months
        # in the past or in the future.
        if when.month - current['month'] >= 6 :
            when = when.replace(year=current['year']-1)
        elif current['month'] - when.month >= 6:
            when = when.replace(year=current['year']+1)

        event['datetime'] = pytz.timezone('Europe/London').localize(when)
        
        scraperwiki.sqlite.save(["url"], event) # save the records one by one

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url, current):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_page(soup, current)
    next_link = soup.find("a", { "class" : "next" })

    if next_link:
        next_url = "http://www.turnersims.co.uk" + next_link['href']

        scrape_and_look_for_next_link(next_url, current)

london = pytz.timezone('Europe/London')

now_utc = datetime.now(pytz.timezone('UTC'))
now_tz = now_utc.astimezone(london)

current = {}
current['year'] = now_tz.year
current['month'] = now_tz.month

base_url = 'http://www.turnersims.co.uk/upcoming-events'
scrape_and_look_for_next_link(base_url, current)
