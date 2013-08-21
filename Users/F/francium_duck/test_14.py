import scraperwiki
import csv
#import sqlite3 as lite

"""
The latitude/longitude data herein is randomly assigned from coordinates
within the same postcode district as the individual concerned.

No identities should be inferred from these locations. 
"""

scraperwiki.sqlite.execute("DROP TABLE IF EXISTS rhok_map_data")

scraperwiki.sqlite.execute("""CREATE TABLE rhok_map_data (
                    person_id integer unique,
                    groupprojectid integer,
                    groupmemberid integer, 
                    groupprojectmemberskillwheelid integer,
                    facilitator_type string,
                    approxtime int,
                    ismale int, 
                    dob string,
                    ethnicityref int,
                    disabilityref int,
                    approx_age int,
                    latitude real, 
                    longitude real 
)""")


# download data from dropbox
data = scraperwiki.scrape("http://dl.dropbox.com/u/2062132/rhok_scraper_data.csv")
reader = csv.reader(data.splitlines())

for row in reader:
    scraperwiki.sqlite.execute("""
        INSERT INTO rhok_map_data VALUES (?,?,?,?,?,
                                          ?,?,?,?,?,
                                          ?,?,?)""",row)

scraperwiki.sqlite.commit()


#
# Blank Python

