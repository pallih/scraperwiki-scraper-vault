import scraperwiki
from bs4 import BeautifulSoup
import re

url = "http://www.fsa.usda.gov/FSA/dacoReports?area=home&subject=coop&topic=rpt-ps&reportType=Procurement-Bulk+Grain&subCategory=Contract+Awards+Bulk+Grain&summaryYear=%d&x=20&y=8"

stem = "http://www.fsa.usda.gov"

years = [2010, 2011]


for year in years:
    html = scraperwiki.scrape(url % year)
    soup = BeautifulSoup(html)
    
        

    list_of_links = soup.find_all("a", title="Link opens in new window")

    for a in list_of_links:
        link = stem + a['href']
        data = { "Year": year, "URL": link}
        scraperwiki.sqlite.save(["URL"], data)import scraperwiki
from bs4 import BeautifulSoup
import re

url = "http://www.fsa.usda.gov/FSA/dacoReports?area=home&subject=coop&topic=rpt-ps&reportType=Procurement-Bulk+Grain&subCategory=Contract+Awards+Bulk+Grain&summaryYear=%d&x=20&y=8"

stem = "http://www.fsa.usda.gov"

years = [2010, 2011]


for year in years:
    html = scraperwiki.scrape(url % year)
    soup = BeautifulSoup(html)
    
        

    list_of_links = soup.find_all("a", title="Link opens in new window")

    for a in list_of_links:
        link = stem + a['href']
        data = { "Year": year, "URL": link}
        scraperwiki.sqlite.save(["URL"], data)