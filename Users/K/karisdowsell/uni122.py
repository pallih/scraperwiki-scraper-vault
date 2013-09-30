import scraperwiki, sys
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("uni12")

links = scraperwiki.sqlite.select("URL from `uni12`.swdata")

for link in links:
    url = link["URL"]
    print url

    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    #print soup
    
    title = soup.find("h2","legend-edit").get_text().replace("English", "").strip()
    print title

    ps = soup.find_all ("p", "clearfix")
    for p in ps: 
        span_text = ""
        span= p.find("span")
        if span:
            span_text = span.get_text().strip() 
            span.clear()
        if span_text != "":
            info = p.get_text().strip()
            print span_text
            print info
                
                if ref ==("reference number:")
                ref = info
                print info
        



            import scraperwiki, sys
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("uni12")

links = scraperwiki.sqlite.select("URL from `uni12`.swdata")

for link in links:
    url = link["URL"]
    print url

    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    #print soup
    
    title = soup.find("h2","legend-edit").get_text().replace("English", "").strip()
    print title

    ps = soup.find_all ("p", "clearfix")
    for p in ps: 
        span_text = ""
        span= p.find("span")
        if span:
            span_text = span.get_text().strip() 
            span.clear()
        if span_text != "":
            info = p.get_text().strip()
            print span_text
            print info
                
                if ref ==("reference number:")
                ref = info
                print info
        



            