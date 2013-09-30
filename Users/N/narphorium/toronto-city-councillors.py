###############################################################################
# Toronto City Councillors Scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

def parse_ward(ward_name):
    ward = {}
    matches = re.search("^Ward (\d+) (.+)$", ward_name, re.MULTILINE)
    ward["Number"] = matches.group(1).strip()
    ward["Name"] = matches.group(2).strip()
    return ward 

def scrape_councillor(url, record):
    record["URL"] = url
    soup = BeautifulSoup(scraperwiki.scrape(url))
    main_content = soup.find("div",{"id":"content"}).find("div",{"class":"main"})

    ward_data = parse_ward(main_content.find("a").text.strip())
    record["Ward Number"] = ward_data["Number"]
    record["Ward Name"] = ward_data["Name"]

    record["Name"] = main_content.find("h3").text.replace("Councillor","").strip()
    record["Image"] = "http://www.toronto.ca" + main_content.find("img")["src"].strip() 
    record["Email"] = ""
    record["Website"] = ""
    for link in main_content.find("div",{"class":"two_column"}).findAll("a"):
        if link["href"].find('mailto:') > -1:
            record["Email"] = link["href"].replace("mailto:","").strip()
        elif link["target"] == "_blank" and link["href"].find('http:') > -1:
            record["Website"] = link["href"].strip()

        
# retrieve a page
starting_url = 'http://app.toronto.ca/im/council/councillors.jsp'
soup = BeautifulSoup(scraperwiki.scrape(starting_url))

# use BeautifulSoup to get all <td> tags
table = soup.find('td', { "width" : "600" }).find("table")
for link in table.findAll("a"):
    if link['href'].find("councillors") > -1 and len(link.text.strip()) > 0:
        record = {}
        scrape_councillor(link['href'], record)
        print record
        # save records to the datastore
        scraperwiki.sqlite.save(["Name"], record) 
    ###############################################################################
# Toronto City Councillors Scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

def parse_ward(ward_name):
    ward = {}
    matches = re.search("^Ward (\d+) (.+)$", ward_name, re.MULTILINE)
    ward["Number"] = matches.group(1).strip()
    ward["Name"] = matches.group(2).strip()
    return ward 

def scrape_councillor(url, record):
    record["URL"] = url
    soup = BeautifulSoup(scraperwiki.scrape(url))
    main_content = soup.find("div",{"id":"content"}).find("div",{"class":"main"})

    ward_data = parse_ward(main_content.find("a").text.strip())
    record["Ward Number"] = ward_data["Number"]
    record["Ward Name"] = ward_data["Name"]

    record["Name"] = main_content.find("h3").text.replace("Councillor","").strip()
    record["Image"] = "http://www.toronto.ca" + main_content.find("img")["src"].strip() 
    record["Email"] = ""
    record["Website"] = ""
    for link in main_content.find("div",{"class":"two_column"}).findAll("a"):
        if link["href"].find('mailto:') > -1:
            record["Email"] = link["href"].replace("mailto:","").strip()
        elif link["target"] == "_blank" and link["href"].find('http:') > -1:
            record["Website"] = link["href"].strip()

        
# retrieve a page
starting_url = 'http://app.toronto.ca/im/council/councillors.jsp'
soup = BeautifulSoup(scraperwiki.scrape(starting_url))

# use BeautifulSoup to get all <td> tags
table = soup.find('td', { "width" : "600" }).find("table")
for link in table.findAll("a"):
    if link['href'].find("councillors") > -1 and len(link.text.strip()) > 0:
        record = {}
        scrape_councillor(link['href'], record)
        print record
        # save records to the datastore
        scraperwiki.sqlite.save(["Name"], record) 
    