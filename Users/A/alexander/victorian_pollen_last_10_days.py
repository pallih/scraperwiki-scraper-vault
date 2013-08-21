# Blank Python
sourcescraper = 'victorian_pollen_rating_all_days'
#import scraperwiki.sqlite

# connect to the source database giving it the name src
#scraperwiki.sqlite.attach(sourcescraper, "src")

#SELECT * FROM swdata

#####################################
import scraperwiki
scraperwiki.sqlite.attach("victorian_pollen_rating_all_days")


data = scraperwiki.sqlite.select(
    '''* from `swdata` 
    order by Date desc limit 10'''
)


print "<h1>Victorian Pollen Ratings</h1>"
print "This Scraper scrapes daily pollen ratings from http://www.asthma.org.au/PollenAlert.aspx."
print "Updated once a day.</br>"
print "Created by Alexander M on scraperwiki.com</p>"
print "</br>"

print "<table>"           
print "<tr><th>Date</th><th>Rating</th><th>Grass Pollen Count</th><th>Total Pollen Count</th>"
for d in data:
    print "<tr>"
    print "<td>", d["Date"], "</td>"
    print "<td>", d["Rating"], "</td>"
    print "<td>", d["GrassCount"], "</td>"
    print "<td>", d["TotalCount"], "</td>"


