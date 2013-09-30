from scraperwiki import swimport
TABLE_NAME='nytm_sos'

swimport('meetup').scrape('http://www.meetup.com/ny-tech/events/47879702/',TABLE_NAME)
swimport('swversion').swversion(TABLE_NAME)

print """
How to get the current table:
SELECT * from (SELECT value_blob FROM `swvariables` WHERE name="nytm_sos_current");
"""from scraperwiki import swimport
TABLE_NAME='nytm_sos'

swimport('meetup').scrape('http://www.meetup.com/ny-tech/events/47879702/',TABLE_NAME)
swimport('swversion').swversion(TABLE_NAME)

print """
How to get the current table:
SELECT * from (SELECT value_blob FROM `swvariables` WHERE name="nytm_sos_current");
"""