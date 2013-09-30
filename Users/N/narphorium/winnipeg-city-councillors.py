###############################################################################
# Winnipeg City Councillors Scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup, Comment
 
VALID_KEYS = ["Ward", "Address", "Phone", "Fax"]

def add_record_value(record, key, value):
    if key in VALID_KEYS:
        value = value.replace('&nbsp;', ' ')
        record[key] = value.strip()

def scrape_councillor(url, record):
    record["URL"] = "http://www.winnipeg.ca/council/" + url
    soup = BeautifulSoup(scraperwiki.scrape(record["URL"]))

    # strip all HTML comments from the page.
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]

    tables = soup.find("div", {"id" : "content"}).findAll("table")
    img = soup.find("img", {"class" : "bio_pic"})
    if img:
        record["Image"] = "http://www.winnipeg.ca" + img["src"]

    name = soup.find("span", {"class" : "bg90B"})
    record["Name"] = name.text.replace('Councillor','').strip()


    # table = soup.find(text="Ward Information").findParent('table').find("table", { "width" : "100%" })
    table = tables[0]
    key = ''
    value = ''
    # Could be improved to add spaces within the addresses.
    for row in table.findAll("tr"):
        cols = row.findAll("td")
        k = cols[0].text.strip().replace(':','')
        if len(k) > 0:
            add_record_value(record, key, value)
            key = k
            value = ''
        if len(cols) > 1:
            value += cols[1].text.strip() + '\n'
    add_record_value(record, key, value)
        
        
# retrieve a page
starting_url = 'http://www.winnipeg.ca/council/'
soup = BeautifulSoup(scraperwiki.scrape(starting_url))

# use BeautifulSoup to get all <td> tags
table = soup.find('div', { "id" : "content" }).findAll("table")[1]
for td in table.findAll("td"):
    if td.find('font', { "class" : "k80B" }) != None:
        record = {}
        link = td.find('a')
        scrape_councillor(link['href'], record)
        print record
        # save records to the datastore
        scraperwiki.sqlite.save(["Name"], record) 
    
###############################################################################
# Winnipeg City Councillors Scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup, Comment
 
VALID_KEYS = ["Ward", "Address", "Phone", "Fax"]

def add_record_value(record, key, value):
    if key in VALID_KEYS:
        value = value.replace('&nbsp;', ' ')
        record[key] = value.strip()

def scrape_councillor(url, record):
    record["URL"] = "http://www.winnipeg.ca/council/" + url
    soup = BeautifulSoup(scraperwiki.scrape(record["URL"]))

    # strip all HTML comments from the page.
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]

    tables = soup.find("div", {"id" : "content"}).findAll("table")
    img = soup.find("img", {"class" : "bio_pic"})
    if img:
        record["Image"] = "http://www.winnipeg.ca" + img["src"]

    name = soup.find("span", {"class" : "bg90B"})
    record["Name"] = name.text.replace('Councillor','').strip()


    # table = soup.find(text="Ward Information").findParent('table').find("table", { "width" : "100%" })
    table = tables[0]
    key = ''
    value = ''
    # Could be improved to add spaces within the addresses.
    for row in table.findAll("tr"):
        cols = row.findAll("td")
        k = cols[0].text.strip().replace(':','')
        if len(k) > 0:
            add_record_value(record, key, value)
            key = k
            value = ''
        if len(cols) > 1:
            value += cols[1].text.strip() + '\n'
    add_record_value(record, key, value)
        
        
# retrieve a page
starting_url = 'http://www.winnipeg.ca/council/'
soup = BeautifulSoup(scraperwiki.scrape(starting_url))

# use BeautifulSoup to get all <td> tags
table = soup.find('div', { "id" : "content" }).findAll("table")[1]
for td in table.findAll("td"):
    if td.find('font', { "class" : "k80B" }) != None:
        record = {}
        link = td.find('a')
        scrape_councillor(link['href'], record)
        print record
        # save records to the datastore
        scraperwiki.sqlite.save(["Name"], record) 
    
