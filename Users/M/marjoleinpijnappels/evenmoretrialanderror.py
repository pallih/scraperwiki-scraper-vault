import scraperwiki
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach('moretrialanderror')

scrapings = scraperwiki.sqlite.select("* from 'moretrialanderror'.swdata")

for scraping in scrapings:
    url = scraping["URL"]
    #print url

    soup = BeautifulSoup(scraping["HTML"])

    title = soup.find("div","fieldset-title corners-top").get_text().replace("English", "").strip()
    #print title

info = soup.find_all("p", "clearfix")

for p in info:
    span = p.find("span")
    if span:
        span_text = span.get_text().strip()
        print span_text
        span.clear()
    if span_text != "":
        info = p.get_text().strip() #the rest of the text in the ps have the column values
    print infoimport scraperwiki
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach('moretrialanderror')

scrapings = scraperwiki.sqlite.select("* from 'moretrialanderror'.swdata")

for scraping in scrapings:
    url = scraping["URL"]
    #print url

    soup = BeautifulSoup(scraping["HTML"])

    title = soup.find("div","fieldset-title corners-top").get_text().replace("English", "").strip()
    #print title

info = soup.find_all("p", "clearfix")

for p in info:
    span = p.find("span")
    if span:
        span_text = span.get_text().strip()
        print span_text
        span.clear()
    if span_text != "":
        info = p.get_text().strip() #the rest of the text in the ps have the column values
    print info