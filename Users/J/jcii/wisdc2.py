# Blank Python
import scraperwiki
import logging
from BeautifulSoup import BeautifulSoup


# retrieve a page
starting_url = 'http://wisdc.org/index.php?filter=+Search+&from=2004-01-01&to=--&module=wisdc.websiteforms&cmd=searchadvanced&qty=10000'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

#store the order of the columns
scraperwiki.sqlite.save_var("data_columns", ["date", "candidateName", "candidateLink", "contributorName", "citystatezip", "employer", "interest_category", "amount" ])

tables = soup.findAll('table', {"class" : "searchTable"})
rows = tables[1].tbody.findAll('tr')
print "There are %d rows" % len(rows)
for row in rows:
    print "row: ", row
    cells = row.findAll('td')

    date = cells[0].text
    candidateName = cells[1].text
    candidateLink = cells[1].href
    contributorName = cells[2].text
    citystatezip = cells[3].text
    employer = cells[4].text
    interest_category = cells[5].text
    amount = cells[6].text

    record = { "date" : date, "candidateName" : candidateName, "candidateLink" : candidateLink, "contributorName" : contributorName , "citystatezip" : citystatezip , "employer" : employer, "interest_category" : interest_category, "amount": amount }

    scraperwiki.sqlite.save(unique_keys=["date", "candidateName", "contributorName", "citystatezip", "amount"], data=record)
#    for cell in cells:
#        print "the cell:", cell

