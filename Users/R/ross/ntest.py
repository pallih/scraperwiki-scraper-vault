import lxml.html
import urllib2
import re
import scraperwiki

# want 'http://en.wikipedia.org/wiki/List_of_Formula_One_fatal_accidents' really....
url = "http://webcache.googleusercontent.com/search?q=cache:EseRA70hZ3wJ:en.wikipedia.org/wiki/List_of_Formula_One_fatal_accidents+formula+one+accidents+wikipedia&cd=1&hl=en&ct=clnk&gl=uk"

data = scraperwiki.scrape(url )

# Load the html into lxml
page = lxml.html.fromstring( data )

# data is in first table
table = page.cssselect('table.wikitable')[0]
header_row = table[0] # ignore the header row

driver_re = re.compile(".*\((\w+)\)")

# For each row after the first row
for row in table[1:]:
    data = {}

    data['driver_name'] = row[0].cssselect('span.vcard span.fn')[0].text_content()

    data['driver_country'] = ""
    m = driver_re.match(row[0].text_content())
    if m:
        data['driver_country'] = m.groups(0)[0]

    data['date'] = row[1].text_content()
    data['race'] = row[2].text_content()
    data['circuit'] = row[3].text_content()
    data['car'] = row[4].text_content()
    data['during'] = row[5].text_content()

    scraperwiki.sqlite.save(['driver_name', 'race'], data)
