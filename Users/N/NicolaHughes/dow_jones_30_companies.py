import scraperwiki
from bs4 import BeautifulSoup

url = "http://www.stockmarketsreview.com/companies_dowjones30/"
html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)

tds = soup.find_all("td", "first")
for td in tds:
    company = td.get_text()
    print td.nextSibling
    #data = {"Company": company}
    #scraperwiki.sqlite.save(["Company"], data)
