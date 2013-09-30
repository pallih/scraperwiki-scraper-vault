import scraperwiki
from lxml import etree
import StringIO


# Im using yahoos YQL here just because I already had this query
# In the Yahoo YQL console this query looks like:
# SELECT td.p, td.div.p.strong FROM html WHERE url="http://news.bbc.co.uk/weather/forecast/5?state=fo:B#fo:B" AND xpath='//table[@class="twelve-hour-forecast forecast"]/tbody/tr'
# The interesting parts are the '/forectast/5' which sets the forecast to be for Edinburgh (5) and the 'state=fo:B#fo:B' which has a similar effect to clicking on the '24 hours' tab and changes the weather display to be the 24 hours one

html = scraperwiki.scrape ("http://query.yahooapis.com/v1/public/yql?q=SELECT%20*%20FROM%20html%20WHERE%20url%3D%22http%3A%2F%2Fnews.bbc.co.uk%2Fweather%2Fforecast%2F5%3Fstate%3Dfo%3AB%23fo%3AB%22%20AND%20xpath%3D'%2F%2Ftable%5B%40class%3D%22twelve-hour-forecast%20forecast%22%5D%2Ftbody%2Ftr'")

# Turn page into XML etree
xmlTree = etree.parse(StringIO.StringIO(html))

# Extract each row from the table
rows = xmlTree.xpath('/query/results/tr')

uniqueRecordId = 0

# Iterate over each row in the XML representation of the HTML table
# Each row is a time and bunch of weather information
for row in rows:
    record = {
        'id' : None,
        'time': None,
        'summary': None,
        'temp_max_c': None,
        'winddir': None,
        'windspeed': None,
    }  

    # Each col is a column in the XML representation of the HTML table
    cols = row.xpath('td')

    # Populate the record by extracting the parts of the XML representation of the HTML column we are interested in
    # The XPath paths are relative to the column 
    record['id'] = uniqueRecordId
    record['time'] = cols[0].xpath('p')[0].text # time
    record['summary'] = cols[1].xpath('div/p/strong')[0].text # summary weather
    record['temp_max_c'] = cols[2].xpath('span/span')[0].text # temp in C
    record['winddir'] =  cols[3].xpath('span/span')[0].text # Wind Dir
    record['windspeed'] = cols[3].xpath('span/span')[1].text # Wind Speed

    # Save the record to the DB
    scraperwiki.sqlite.save(unique_keys=["id"], data=record)

    # Increment the unique record id, sqlite requires every record in the table has a unique id
    uniqueRecordId = uniqueRecordId + 1
import scraperwiki
from lxml import etree
import StringIO


# Im using yahoos YQL here just because I already had this query
# In the Yahoo YQL console this query looks like:
# SELECT td.p, td.div.p.strong FROM html WHERE url="http://news.bbc.co.uk/weather/forecast/5?state=fo:B#fo:B" AND xpath='//table[@class="twelve-hour-forecast forecast"]/tbody/tr'
# The interesting parts are the '/forectast/5' which sets the forecast to be for Edinburgh (5) and the 'state=fo:B#fo:B' which has a similar effect to clicking on the '24 hours' tab and changes the weather display to be the 24 hours one

html = scraperwiki.scrape ("http://query.yahooapis.com/v1/public/yql?q=SELECT%20*%20FROM%20html%20WHERE%20url%3D%22http%3A%2F%2Fnews.bbc.co.uk%2Fweather%2Fforecast%2F5%3Fstate%3Dfo%3AB%23fo%3AB%22%20AND%20xpath%3D'%2F%2Ftable%5B%40class%3D%22twelve-hour-forecast%20forecast%22%5D%2Ftbody%2Ftr'")

# Turn page into XML etree
xmlTree = etree.parse(StringIO.StringIO(html))

# Extract each row from the table
rows = xmlTree.xpath('/query/results/tr')

uniqueRecordId = 0

# Iterate over each row in the XML representation of the HTML table
# Each row is a time and bunch of weather information
for row in rows:
    record = {
        'id' : None,
        'time': None,
        'summary': None,
        'temp_max_c': None,
        'winddir': None,
        'windspeed': None,
    }  

    # Each col is a column in the XML representation of the HTML table
    cols = row.xpath('td')

    # Populate the record by extracting the parts of the XML representation of the HTML column we are interested in
    # The XPath paths are relative to the column 
    record['id'] = uniqueRecordId
    record['time'] = cols[0].xpath('p')[0].text # time
    record['summary'] = cols[1].xpath('div/p/strong')[0].text # summary weather
    record['temp_max_c'] = cols[2].xpath('span/span')[0].text # temp in C
    record['winddir'] =  cols[3].xpath('span/span')[0].text # Wind Dir
    record['windspeed'] = cols[3].xpath('span/span')[1].text # Wind Speed

    # Save the record to the DB
    scraperwiki.sqlite.save(unique_keys=["id"], data=record)

    # Increment the unique record id, sqlite requires every record in the table has a unique id
    uniqueRecordId = uniqueRecordId + 1
