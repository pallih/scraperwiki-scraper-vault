import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.southampton.gov.uk/s-leisure/parksgreenspaces/ParksLocaltoYou/")
root = lxml.html.fromstring(html)

for faqblock in root.cssselect(".faqBlock"):
    for link in faqblock.cssselect("h2 a"):
        park = {
            'name': link.text_content().strip(), 
        }

        scraperwiki.sqlite.save(["name"], park)import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.southampton.gov.uk/s-leisure/parksgreenspaces/ParksLocaltoYou/")
root = lxml.html.fromstring(html)

for faqblock in root.cssselect(".faqBlock"):
    for link in faqblock.cssselect("h2 a"):
        park = {
            'name': link.text_content().strip(), 
        }

        scraperwiki.sqlite.save(["name"], park)