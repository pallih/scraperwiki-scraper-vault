import scraperwiki
import lxml.html
import csvkit

schools_csv = scraperwiki.scrape('http://projects.propublica.org/schools/tables/districts/1100030.csv')

print schools_csv