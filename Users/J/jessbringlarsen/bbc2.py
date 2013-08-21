import scraperwiki
import lxml.html
import re

# Regex matcher to split date/time string into date and time strings
timePattern = re.compile('(\d+-\d+-\d+)\s(\d+:\d+)')

html = scraperwiki.scrape('http://www.bordtennisportalen.dk/DBTU/HoldTurnering/UdskrivStilling/?page=3&season=42012&region=4004&agegroup=4006&group=1909&team=13705&match=&club=&player=')
root = lxml.html.fromstring(html)
rows = root.cssselect("table.matchlist tr")

# Remove header row
rows.remove(rows[0])
for row in rows:
    timeMatcher = timePattern.search(row[0].text_content())
    
    data = {
      'date' : timeMatcher.group(1),
      'time' : timeMatcher.group(2),
      'matchno' : row[1].text_content(),
      'home_team' : row[2].text_content(),
      'away_team' : row[3].text_content()
    }
    scraperwiki.sqlite.save(unique_keys=['matchno'], data=data)