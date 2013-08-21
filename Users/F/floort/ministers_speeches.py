###############################################################################
# Basic scraper
###############################################################################

import datetime
import scraperwiki
from BeautifulSoup import BeautifulSoup
from urlparse import urljoin

STARTING_PAGES = [
    "http://www.dwp.gov.uk/newsroom/ministers-speeches/",
    "http://www.dwp.gov.uk/previous-administration-news/ministers-speeches/"
]

def scrape_speech(url, date, author, title):
    page = BeautifulSoup(scraperwiki.scrape(url))
    content = page.find("div", {"id": "content"}).text
    where = page.find("div", {"id": "content"}).findAll("p")[2].text
    scraperwiki.sqlite.save(["permalink"],{
        "permalink": url,
        "given_on": date,
        "minister_name": author,
        "title": title,
        "body": content,
        "where": where,
        "department": "Department for Work and Pensions",
    })
    

def scrape_list(url):
    page = BeautifulSoup(scraperwiki.scrape(url))
    for row in page.find("table", {"class":"listTable"}).findAll("tr")[1:]:
        colls = row.findAll("td")
        date = [int(n) for n in colls[0].text.split("/")]
        date = datetime.date(date[2]+2000, date[1], date[0])
        author = colls[2].text
        speech_url = urljoin(url, colls[1].find("a")["href"])
        title = colls[1].find("a").text
        scrape_speech(speech_url, date, author, title)
        


for url in STARTING_PAGES:
    page = BeautifulSoup(scraperwiki.scrape(url))
    for y in page.find("ul", {"class":"year"}).findAll("li"):
        scrape_list(urljoin(url, y.find("a")["href"]))
    
