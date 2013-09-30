import scraperwiki
from bs4 import BeautifulSoup

url ="http://www.fsa.usda.gov/FSA/dacoReports?area=home&subject=coop&topic=rpt-ps&reportType=Procurement-International&subCategory=Contract+Awards+Intl&summaryYear=%d&x=17&y=10"

stem = "http://www.fsa.usda.gov/"

years = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]


for year in years:
    html = scraperwiki.scrape(url % year)
    soup = BeautifulSoup(html)
    
    print soup.prettify()
    
    # Result is a list of links
    list_of_links = soup.find_all("a", title="Link opens in new window")
    
    for a in list_of_links:
        link = stem + a['href']
        data = { "Year": year, "URL": link}
        #scraperwiki.sqlite.save(["URL"], data)import scraperwiki
from bs4 import BeautifulSoup

url ="http://www.fsa.usda.gov/FSA/dacoReports?area=home&subject=coop&topic=rpt-ps&reportType=Procurement-International&subCategory=Contract+Awards+Intl&summaryYear=%d&x=17&y=10"

stem = "http://www.fsa.usda.gov/"

years = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]


for year in years:
    html = scraperwiki.scrape(url % year)
    soup = BeautifulSoup(html)
    
    print soup.prettify()
    
    # Result is a list of links
    list_of_links = soup.find_all("a", title="Link opens in new window")
    
    for a in list_of_links:
        link = stem + a['href']
        data = { "Year": year, "URL": link}
        #scraperwiki.sqlite.save(["URL"], data)