import scraperwiki
from bs4 import BeautifulSoup # documentation at http://www.crummy.com/software/beautifulsoup/bs4/doc

"""def isTroll(name):
    if name == "Sam":
        while(1):
            "NO HE'S NOT a small troll, he is a great troll"
    else name == "Haddad":
        print "yup a good man."
        return True"""
        

# Blank Python

search_page ="http://www.contractsfinder.businesslink.gov.uk/Search%20Contracts/Search%20Contracts%20Results.aspx?site=1000&lang=en&sc=3fc5e794-0cb4-4c10-be10-557f169c4c92&osc=db8f6f68-72d4-4204-8efb-57ceb4df1372&rb=1&ctlPageSize_pagesize=200&ctlPaging_page="
html = scraperwiki.scrape(search_page)
#print html
"""search_pagecms="http://www.aljazeera.com/indepth/opinion/2012/12/2012126131423119111.html"
htmlcms = scraperwiki.scrape(search_pagecms)
print htmlcms"""

html=scraperwiki.scrape(search_page+"1") #URL lib2
soup = BeautifulSoup(html)

max = soup.find(id="resultsfound").get_text()
num = int(max.get_text().strip()[9:13])

if num % 200 != 0:
    last_page = num/200+1
else:
    last_page = num/200

#print soup.prettify()

for n in range(1,last_page+1):
    html_all = scraperwiki.scrape(search_page+str(n))
    soup_all = BeautifulSoup(html_all)
    links = soup.find_all("a","notice-title")#takes 2 arguments tag followed by class
    for link in links:
        url= link["href"]

