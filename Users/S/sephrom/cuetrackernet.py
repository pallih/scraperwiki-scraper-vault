import scraperwiki
import lxml.html

# Create table scheme to determine alignment of table columns
scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS cuetracker (id integer, player text, country text, matchesPlayed integer, matchesWon integer, matchesWonInPercent real, framesPlayed integer, framesWon integer, framesWonInPercent real)") 

html = scraperwiki.scrape("http://www.cuetracker.net/pages/matchesFrames.php?season=2012/2013")
root = lxml.html.fromstring(html)

data = []

for tr in root.cssselect('div.text table table tr'):
    # Skip table header
    if tr.cssselect("td")[1].text_content() == 'Player':
        continue

    # Split fields with integer and percent value
    matchesArray = tr.cssselect("td")[3].text_content().translate(None, "()%").split(' ')
    framesArray = tr.cssselect("td")[5].text_content().translate(None, "()%").split(' ')

    data = {
        'id': int(tr.cssselect("td")[0].text_content()),
        'country': tr.cssselect("td img.flag")[0].attrib['title'],
        'player': tr.cssselect("td")[1].text_content(),
        'matchesPlayed': int(tr.cssselect("td")[2].text_content()),
        'matchesWon': int(matchesArray[0]),
        'matchesWonInPercent': float(matchesArray[1]),
        'framesPlayed': int(tr.cssselect("td")[4].text_content()),
        'framesWon': int(framesArray[0]),
        'framesWonInPercent': float(framesArray[0]),
    }

    # Store fetched data
    scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="cuetracker", verbose=2)
