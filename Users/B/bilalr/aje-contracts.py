#Stolen Code

import scraperwiki
from bs4 import BeautifulSoup 

# Blank Python
scraperwiki.sqlite.attach("dod-contracts")
links = scraperwiki.sqlite.select("URL from `dod-contracts`.swdata")

for link in links:
    url=link["URL"] #to access the value of a dictionary
    #print url

#now run the URL
    html = scraperwiki.scrape(url)
    data = {"html": html, "url": url} #saving the HTML and URL data in a dictionary
    scraperwiki.sqlite.save(["url"], data)
    soup = BeautifulSoup(html)
    title = soup.find("div","inner maintext").get_text().strip().replace("\n", "").replace("\t", "").replace("\r","")
    print title
