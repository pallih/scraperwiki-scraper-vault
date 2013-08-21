import scraperwiki
import lxml.html

import pytz
from datetime import datetime

# Take date and time strings and return a corresponding datetime object
def processtime(date, time, current_year, current_month):
    when = datetime.strptime(date + " " + time, "%d %B %I.%M %p")
    when = when.replace(year=current_year)

    when = london.localize(when)

    # We assume here they won't publish things more than 6 months
    # in the past or in the future.
    if when.month - current_month >= 6 :
        when = when.replace(year=current_year-1)
    elif current_month - when.month >= 6:
        when = when.replace(year=current_year+1)

    return when

london = pytz.timezone('Europe/London')

now_utc = datetime.now(pytz.timezone('UTC'))
now_tz = now_utc.astimezone(london)

current_year = now_tz.year
current_month = now_tz.month

html = scraperwiki.scrape("http://www.southampton.gov.uk/s-leisure/parksgreenspaces/events.aspx")

root = lxml.html.fromstring(html)

for tr in root.cssselect("div.blog tr"):
    tds = tr.cssselect("td")

    #FIXME: This sometimes eats the first event, the parser needs tweaking
    if len(tds) == 0:
        continue

    when = processtime(tds[0].text_content().strip(),
                       tds[2].text_content().strip(),
                       current_year, current_month)

    data = {
      'datetime' : when,
      'venue' : tds[3].text_content().strip(),
      'event' : tds[1].text_content().strip(),
    }

    scraperwiki.sqlite.save(unique_keys=['datetime','venue','event'], data=data)



