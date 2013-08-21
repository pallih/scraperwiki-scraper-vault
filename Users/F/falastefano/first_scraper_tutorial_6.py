import scraperwiki
import lxml.html

#
# Documentation / First scraper tutorial
#

# Test Python
print "Hello, coding in the cloud!"


# Download HTML from the web
html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html


# Parsing the HTML to get content and  Saving to the ScraperWiki datastore
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        # Save data to the ScraperWiki datastore
        # The unique keys (just country in this case) identify each piece of data. 
        # When the scraper runs again, existing data with the same values for the unique keys is replaced.
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)
        # Stampa il dato a video
        print data


# Getting the data out again.
# Example: gives you the records for the ten countries where children spend the most years at school
# select * from swdata order by years_in_school desc limit 10



