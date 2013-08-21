import scraperwiki, sys
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("contracts_finder_mod")

links = scraperwiki.sqlite.select("URL from `contracts_finder_mod`.swdata")

for link in links:
    url = link["URL"]
    print url

    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    #print soup

    title = soup.find("h2", "legend-edit").get_text().replace("English", "").strip()
    print title

    ps = soup.find_all("p","clearfix")
    
    for p in ps:
        span_text = ""
        span = p.find("span")
        if span:
            span_text = span.get_text().strip()
            span.clear()
        if span_text !="":
            info = p.get_text().strip()
            # print span_text
            # print info

            if span_text == "Reference number:":
                ref = info
                print info

            elif span_text == "Estimated length of contract:":
                # change date data   
                est = info
                print info

            #issue with this block
            elif span_text == "Awarded value:":
                award = info                
                #sort this bit out!!!!
                value = int(info.encode("utf8").replace(",", "").replace(",","")
                #print info
                print value
            #end problem block

            elif span_text == "Location where the contract is to be carried out:":
                location = info
                print info

            elif span_text == "Name of the buying organisation:":
                name_buy = info
                #need to remove English
                info = info.replace("English", "")
                print info       