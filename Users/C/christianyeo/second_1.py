import scraperwiki, sys
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("scrapes")

links = scraperwiki.sqlite.select('URL from `scrapes`.swdata')

for link in links:
    url = link["URL"]
    #print url

    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    #print soup

    title = soup.find("h2", "legend-edit").get_text().replace("English",'').strip()
    print title

    ps = soup.find_all("p", "clearfix")
    
    for p in ps:
        span_text = ''
        span = p.find("span")
        if span:
            span_text = span.get_text().strip()
            span.clear()
        if span_text !="":
            info = p.get_text().strip()
#            print span
#            print info
            if span_text == "Reference number:":
                print info
            elif span_text == "Estimated length of contract:":
                print info
            elif span_text == "Awarded value:":
                print info