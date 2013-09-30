import scraperwiki           
import lxml.html
import re

import pytz
from datetime import datetime

london = pytz.timezone('Europe/London')

html = scraperwiki.scrape("http://www.platformtavern.com/music.html")
root = lxml.html.fromstring(html)

month = ""
year = 0

for tr in root.cssselect("table[align='center'] tr"):
    month_td = tr.cssselect(".style53,.style69")

    # Catch the rows which contain the month and year.
    if len(month_td) != 0:
        month_str = month_td[0].text_content().strip()

        m = re.match(r"(\w+) (\d+)", month_str)
        if m == None:
            print "Skipping"
            continue

        month = m.group(1)
        year = m.group(2)
        continue

    # Ignore everything before the first month row.
    if month == "":
        continue

    cols = tr.cssselect("td")

    # Ignore rows where the middle column is not a single hyphen.
    if (len(cols) > 1) and (cols[1].text_content() != "-"):
        continue

    date_str = cols[0].text_content().strip()

    m = re.search(r"day (\d+)(?:st|nd|rd|th)\s*(?:from|-)\s*(\d+)\.?(\d+)?pm", date_str)

    # Carry on if there was no match.
    if m == None:
        print "No match!"
        continue

    day = m.group(1)
    hour = m.group(2)
    minute = m.group(3) or 0

    when = london.localize(
        datetime.strptime(
            "%s,%s,%s,%s,%s,PM" % (year, month, day, hour, minute),
            "%Y,%B,%d,%I,%M,%p"
        )
    )

    data = {
        'datetime': when,
        'act': cols[2].text_content().strip(),
    }

    scraperwiki.sqlite.save(unique_keys=['datetime'], data=data)import scraperwiki           
import lxml.html
import re

import pytz
from datetime import datetime

london = pytz.timezone('Europe/London')

html = scraperwiki.scrape("http://www.platformtavern.com/music.html")
root = lxml.html.fromstring(html)

month = ""
year = 0

for tr in root.cssselect("table[align='center'] tr"):
    month_td = tr.cssselect(".style53,.style69")

    # Catch the rows which contain the month and year.
    if len(month_td) != 0:
        month_str = month_td[0].text_content().strip()

        m = re.match(r"(\w+) (\d+)", month_str)
        if m == None:
            print "Skipping"
            continue

        month = m.group(1)
        year = m.group(2)
        continue

    # Ignore everything before the first month row.
    if month == "":
        continue

    cols = tr.cssselect("td")

    # Ignore rows where the middle column is not a single hyphen.
    if (len(cols) > 1) and (cols[1].text_content() != "-"):
        continue

    date_str = cols[0].text_content().strip()

    m = re.search(r"day (\d+)(?:st|nd|rd|th)\s*(?:from|-)\s*(\d+)\.?(\d+)?pm", date_str)

    # Carry on if there was no match.
    if m == None:
        print "No match!"
        continue

    day = m.group(1)
    hour = m.group(2)
    minute = m.group(3) or 0

    when = london.localize(
        datetime.strptime(
            "%s,%s,%s,%s,%s,PM" % (year, month, day, hour, minute),
            "%Y,%B,%d,%I,%M,%p"
        )
    )

    data = {
        'datetime': when,
        'act': cols[2].text_content().strip(),
    }

    scraperwiki.sqlite.save(unique_keys=['datetime'], data=data)