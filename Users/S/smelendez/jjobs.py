import scraperwiki
from bs4 import BeautifulSoup
import requests
import dateutil.parser


def main():
    jjobsurl = 'http://journalismjobs.com/Search_Jobs_all.cfm'
    jjobspage = requests.get(jjobsurl).text # Quick and dirty

    soup = BeautifulSoup(jjobspage)
    
    for row in soup.findAll("tr", "plainRow"):
        title = row.find("b").get_text()
        
        company = row.find("div", "company").get_text().strip()
        location = row.find("td", "location").get_text().strip()
        postdate = row.find("td", "postdate").get_text().strip()
       
        
        print title,company,location,postdate

        data = {
            'title' : title,
            'company' : company,
            'location' : location,
            'date' : postdate
        }
        print data
        scraperwiki.sqlite.save(unique_keys = data.keys(), data = data)
        
     
main()
        
# Blank Python

