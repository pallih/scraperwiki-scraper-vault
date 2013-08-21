import scraperwiki
import urllib
import lxml.html

# Grabs individual stats about the AFL players from the stats center.
# Note these stats are from the stats view! Uses finalsiren.com as the
# data source.
#
# Written by Kah Goh, 2013.

def getContent(season, page):
    """Extracts a page of HTML content.

        season is the year to extract the data for

        page is the page number to extract from
    """
    encodedReq = urllib.urlencode({'SeasonID' : season, 'Page': page, 'Sort': 'Rating Desc'})
    url = "http://finalsiren.com/AFLPlayerStats.asp?%s" % encodedReq
    content = scraperwiki.scrape(url)
    return content

def extractEntries(content):
    """Extracts the player stats from the HTML content.

        content is the HTML content containing the stats to be extracted.
    """
    parsed = lxml.html.fromstring(content)

    # There should be only one table on the page with content.
    table = parsed.cssselect('table.playerstatssmall')[0]
    readRows(table.cssselect('tr.ar1'))
    readRows(table.cssselect('tr.ar2'))

def readRows(rows):
    """Reads the data from the given rows and insert them into the database.

        rows are in the table containing the stats to be extracted.
    """
    for row in rows:
        parseRow(row)

def parseRow(row):
    """Reads the entry contained in a single row and stores it in the database.

        row is the row containing the content.
    """
    cells = row.cssselect('td')

    name = cells[2].text_content
    data = {'name': cells[2].text_content(),
        'team': cells[4].text_content(),
        'number': int(cells[1].text_content()),
        'matches_played': int(cells[3].text_content()),
        'kicks': int(cells[5].text_content()),
        'handballs': int(cells[7].text_content()),
        'marks': int(cells[11].text_content()),
        'hit_outs': int(cells[13].text_content()),
        'tackles': int(cells[15].text_content()),
        'frees_for': int(cells[17].text_content()),
        'frees_against': int(cells[18].text_content()),
        'goals': int(cells[19].text_content()),
        'behinds': int(cells[21].text_content()),
        'rating': int(cells[23].text_content()) }
    scraperwiki.sqlite.save(unique_keys=['name'], data=data, table_name='statistics')

# Reads pages 1 to 15 for the 2012 season stats.
for i in range(1, 15):
    extractEntries(getContent(2012, i))

