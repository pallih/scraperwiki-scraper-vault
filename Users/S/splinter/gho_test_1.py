import scraperwiki
import csv


data = scraperwiki.scrape("http://apps.who.int/gho/athena/data/GHO/WHOSIS_000001?format=csv&profile=text&filter=COUNTRY:*;REGION:AFR;REGION:AMR;REGION:SEAR;REGION:EUR;REGION:EMR;REGION:WPR;SEX:-;LOCATION:-");
reader = csv.DictReader(data.splitlines())

for row in reader:
  print "Processing row %s" % row
  scraperwiki.sqlite.save(unique_keys=['Indicator', 'Country', 'Year', 'WHO region', 'World Bank income group'],data=row)
 
