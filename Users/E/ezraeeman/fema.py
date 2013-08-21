import scraperwiki

from bs4 import BeautifulSoup

html = scraperwiki.scrape("http://www.fema.gov/policy-claim-statistics-flood-insurance/policy-claim-statistics-flood-insurance/policy-claim-13-9")
soup = BeautifulSoup(html)

print soup.prettify()


