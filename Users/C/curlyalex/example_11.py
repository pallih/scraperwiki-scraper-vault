import scraperwiki, sys
from bs4 import BeautifulSoup 

scraperwiki.sqlite.attach("test_scraper_36")

links = scraperwiki.sqlite.select
 
print "Processing %d links" % len(links)

for link in links: 
    url = link["URL"]
    print  url

    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    print soup
    position = position + 1  
    scraperwiki.sqlite.save_var('position', link["id"])

    title = soup.find("h2", "legend-edit").get_text().replace("English", "").strip()
    
    ps = soup.find_all ("p", "clearfix")
    for p in ps:
        span_text = ""
        span = p.find("span")
        if span:
            span_text = span.get_text().strip()
            span.clear()
        if span_text != "":
            info = p.get_text().strip()
            
            print span_text
            print p.get_text().strip()
            print
import scraperwiki, sys
from bs4 import BeautifulSoup 

scraperwiki.sqlite.attach("test_scraper_36")

links = scraperwiki.sqlite.select
 
print "Processing %d links" % len(links)

for link in links: 
    url = link["URL"]
    print  url

    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    print soup
    position = position + 1  
    scraperwiki.sqlite.save_var('position', link["id"])

    title = soup.find("h2", "legend-edit").get_text().replace("English", "").strip()
    
    ps = soup.find_all ("p", "clearfix")
    for p in ps:
        span_text = ""
        span = p.find("span")
        if span:
            span_text = span.get_text().strip()
            span.clear()
        if span_text != "":
            info = p.get_text().strip()
            
            print span_text
            print p.get_text().strip()
            print
