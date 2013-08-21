import scraperwiki
import urllib2
import urllib
import BeautifulSoup as bs
import lxml.html

scraperwiki.sqlite.attach("regions", "reg")


rows = scraperwiki.sqlite.select("* from reg.swdata where district_id=26")
count = 0
for row in rows:
    if count > 180 and count < 240:
        val = row['vdc_name']+ " " +row["region_name"]+ " ward:" + str(row['wards'])
        print val
    count += 1
