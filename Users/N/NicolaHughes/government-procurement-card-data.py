import scraperwiki
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("government-procurement-card")

links = scraperwiki.sqlite.select("* from `government-procurement-card`.swdata")

for link in links:
    page_url = link["URL"]
    print page_url
    description = link["Description"]
    publisher = link["Publisher"]
    title = link["Title"]
    latest = link["Latest"]
    html = scraperwiki.scrape(page_url)
    soup = BeautifulSoup(html)

    attributes = soup.find_all("a", "btn btn-primary")
    for a in attributes:
        url = a["href"]
        #print url
        data = { "Page URL": page_url, "Data URL": url, "Description": description, "Publisher": publisher, "Title": title, "Latest": latest }
        scraperwiki.sqlite.save(["Page URL" , "Data URL"], data )
import scraperwiki
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("government-procurement-card")

links = scraperwiki.sqlite.select("* from `government-procurement-card`.swdata")

for link in links:
    page_url = link["URL"]
    print page_url
    description = link["Description"]
    publisher = link["Publisher"]
    title = link["Title"]
    latest = link["Latest"]
    html = scraperwiki.scrape(page_url)
    soup = BeautifulSoup(html)

    attributes = soup.find_all("a", "btn btn-primary")
    for a in attributes:
        url = a["href"]
        #print url
        data = { "Page URL": page_url, "Data URL": url, "Description": description, "Publisher": publisher, "Title": title, "Latest": latest }
        scraperwiki.sqlite.save(["Page URL" , "Data URL"], data )
