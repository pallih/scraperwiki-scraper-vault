###############################################################################
# This scraper was written to collect the reported crime listed for New York City
# and all of the individual precincts from the NYPD's website contained in the 
# pdf files.
# This scraper is based on an earlier scraper by Andrew Wheeler.
###############################################################################

import scraperwiki

import re

# define the order our columns are displayed in the datastore
scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS `CrimeStatistics` (`edition` text ,`area` text,`start_date` text,`end_date` text,`murder` integer,`rape` integer,`robbery` integer,`felony_assault` integer,`burglary` integer,`grand_larceny` integer,`grand_larceny_auto` integer,`petit_larceny` integer,`misdemeanor_assault` integer,`misdemeanor_sex_crimes` integer,`shooting_victim` integer,`shooting_incident` integer)")

scraperwiki.sqlite.attach("current-week-reported-crime-city-wide-and-for-prec", "src")           
#scraperwiki.sqlite.table_info("src.swdata")

scraperwiki.sqlite.attach("nycrime", "dst")           
#scraperwiki.sqlite.table_info("dst.CrimeStatistics")

# Get one week of data for testing purposes (cmb)
results = scraperwiki.sqlite.select("`area`, `week`, `murder`, `rape`, `robbery`, `fa` as `felony_assault`, `burg` as `burglary`, `lar` as `grand_larceny`, `mvt` as `grand_larceny_auto`, `volume` as `edition` FROM src.swdata")

for result in results:
    dates = result['week'].split() #Report Covering the Week <start> Through <end>
    result['start_date'] = dates[4]
    result['end_date'] = dates[6]
    del result['week']
    print result

scraperwiki.sqlite.save(unique_keys=['area','end_date'],data=results,table_name="CrimeStatistics")
###############################################################################
# This scraper was written to collect the reported crime listed for New York City
# and all of the individual precincts from the NYPD's website contained in the 
# pdf files.
# This scraper is based on an earlier scraper by Andrew Wheeler.
###############################################################################

import scraperwiki

import re

# define the order our columns are displayed in the datastore
scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS `CrimeStatistics` (`edition` text ,`area` text,`start_date` text,`end_date` text,`murder` integer,`rape` integer,`robbery` integer,`felony_assault` integer,`burglary` integer,`grand_larceny` integer,`grand_larceny_auto` integer,`petit_larceny` integer,`misdemeanor_assault` integer,`misdemeanor_sex_crimes` integer,`shooting_victim` integer,`shooting_incident` integer)")

scraperwiki.sqlite.attach("current-week-reported-crime-city-wide-and-for-prec", "src")           
#scraperwiki.sqlite.table_info("src.swdata")

scraperwiki.sqlite.attach("nycrime", "dst")           
#scraperwiki.sqlite.table_info("dst.CrimeStatistics")

# Get one week of data for testing purposes (cmb)
results = scraperwiki.sqlite.select("`area`, `week`, `murder`, `rape`, `robbery`, `fa` as `felony_assault`, `burg` as `burglary`, `lar` as `grand_larceny`, `mvt` as `grand_larceny_auto`, `volume` as `edition` FROM src.swdata")

for result in results:
    dates = result['week'].split() #Report Covering the Week <start> Through <end>
    result['start_date'] = dates[4]
    result['end_date'] = dates[6]
    del result['week']
    print result

scraperwiki.sqlite.save(unique_keys=['area','end_date'],data=results,table_name="CrimeStatistics")
