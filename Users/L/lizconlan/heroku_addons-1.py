import scraperwiki
import logging
from BeautifulSoup import BeautifulSoup


# retrieve a page
starting_url = 'http://addons.heroku.com/'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

#set the order of the columns
if scraperwiki.sqlite.table_info(name="swdata") == []:
    scraperwiki.sqlite.execute("create table swdata (`name` string, `summary` string, `link` string)")

# use BeautifulSoup to get all relevant <div> tags
divs = soup.findAll('div', {"class" : "addon-wrapper"})

for div in divs:
    link = div.find('a')

    name = link.text
    href = starting_url + link['href']
    summary = div.find("p", {"class" : "summary"}).text

    record = {"name" : name, "summary" : summary, "link" : href}

    # save records to the datastore
    scraperwiki.sqlite.save(["name"], record)

import scraperwiki
import logging
from BeautifulSoup import BeautifulSoup


# retrieve a page
starting_url = 'http://addons.heroku.com/'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

#set the order of the columns
if scraperwiki.sqlite.table_info(name="swdata") == []:
    scraperwiki.sqlite.execute("create table swdata (`name` string, `summary` string, `link` string)")

# use BeautifulSoup to get all relevant <div> tags
divs = soup.findAll('div', {"class" : "addon-wrapper"})

for div in divs:
    link = div.find('a')

    name = link.text
    href = starting_url + link['href']
    summary = div.find("p", {"class" : "summary"}).text

    record = {"name" : name, "summary" : summary, "link" : href}

    # save records to the datastore
    scraperwiki.sqlite.save(["name"], record)

