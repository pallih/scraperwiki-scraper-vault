import scraperwiki
from bs4 import BeautifulSoup

search_page = "http://www.theyworkforyou.com/peers/"
html = scraperwiki.scrape(search_page)
soup = BeautifulSoup(html)

all_on_page = soup.find_all("td", "row", "a")

for each in all_on_page:
    link = "http://www.theyworkforyou.com" + each.find("a")["href"]
    from lxml import html
    from urllib import urlopen
    fh = urlopen(link)
    document = html.parse(fh).getroot()
    name = document.cssselect("h1")[0].text
    date = document.cssselect("div.main li strong")[0].text
    list_check_1 = ["2010", "2011", "2012", "2013"]
    if any(word in date for word in list_check_1):
        data = { "Name": name, "Date": date, "URL": link }
        scraperwiki.sqlite.save(["Name"], data)

import scraperwiki
from bs4 import BeautifulSoup

search_page = "http://www.theyworkforyou.com/peers/"
html = scraperwiki.scrape(search_page)
soup = BeautifulSoup(html)

all_on_page = soup.find_all("td", "row", "a")

for each in all_on_page:
    link = "http://www.theyworkforyou.com" + each.find("a")["href"]
    from lxml import html
    from urllib import urlopen
    fh = urlopen(link)
    document = html.parse(fh).getroot()
    name = document.cssselect("h1")[0].text
    date = document.cssselect("div.main li strong")[0].text
    list_check_1 = ["2010", "2011", "2012", "2013"]
    if any(word in date for word in list_check_1):
        data = { "Name": name, "Date": date, "URL": link }
        scraperwiki.sqlite.save(["Name"], data)

