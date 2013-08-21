import lxml.html
import scraperwiki
from BeautifulSoup import BeautifulSoup


starting_url = 'http://www.canstar.com.au/interest-rate-comparison/compare-credit-card-rates.html'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)


table = soup.find("table",{"id" : "credit-cards"})
body = table.find("tbody")
rows = body.findAll("tr")
for row in rows:
    cells = row.findAll("td")
    if cells:
        c = row.find("td", {"class" : "company"})
        if c:
            company = cells[0].find("a").string
            cardName = cells[1].string
            interestRate = cells[2].string
        else:
            cardName = cells[0].string
            interestRate = cells[1].string
        dataAll = {"company": company, "cardName": cardName, "interestRate": interestRate}
        scraperwiki.sqlite.save(unique_keys=["company", "cardName"], data=dataAll, table_name= "canStarCreditCards")




