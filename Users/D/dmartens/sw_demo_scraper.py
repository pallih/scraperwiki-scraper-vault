print "Hello, coding in the cloud!" # prints to the console

# Import needed libraries
import scraperwiki
import lxml.html # SW says that lxml is the best library for parsing HTML

# Identify webpage
html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")

# Print the webpage to the console
print html

# Parse the webpage
root = lxml.html.fromstring(html)

for tr in root.cssselect("div[align='left'] tr"):
  tds = tr.cssselect("td")
  if len(tds)==12:
    data = {
      'country' : tds[0].text_content(),
      'years_in_school' : int(tds[4].text_content())
    }
    print data

    # To store data in the datastore, replace the "print data" line with the following line
    #scraperwiki.sqlite.save(unique_keys=['country'], data=data)

# To acquire data from the datastore, use this line
#select * from swdata order by years_in_school desc limit 10