import scraperwiki
import urllib
import urllib2
import urlparse
import lxml.etree, lxml.html
import re
import HTMLParser

timeHtml = scraperwiki.scrape("http://iswc2011.semanticweb.org/program/")
timeRoot = lxml.html.fromstring(timeHtml)

for div in timeRoot.cssselect(".floatbox .csc-default"):
    h2 = div.cssselect("tr h2")
    if len(h2) > 0:

        rows = div.cssselect('table tr')
        # Get the day and delete the row.
        day = rows[0].text_content()
        del rows[0]
        # Get the times and delete that row.
        timeRow = rows[0]
        del rows[0]

        startTimes = []
        endTimes = []
        del timeRow[0]
        for timeCell in timeRow:
            split = timeCell.text_content().split('-')
            startTimes.append(split[0].strip())
            endTimes.append(split[1].strip())

        for row in rows:
            sTimes = iter(startTimes)
            eTimes = iter(endTimes)
            td = row.cssselect("td")
            if td[0].get('colspan') > 0:
                track = td[0].text_content()
            else:
                room = td[0].text_content()
                del td[0]
                for slot in td:
                    startTime = sTimes.next()
                    endTime = eTimes.next()
                    title = slot.text_content().strip()
                    link = slot.cssselect('a')
                    # if the slot is linked, the id is the link
                    if len(link) > 0:
                        id = link[0].get('href')
                    # otherwise, it's the name and start time
                    else:
                        id = title + startTime

                    # Save time to the database.
                    if title:
                        data = {}
                        data['start_time'] = startTime
                        data['end_time'] = endTime
                        data['day'] = day
                        data['room'] = room
                        data['title'] = title
                        data['id'] = id
                        scraperwiki.sqlite.save(unique_keys=['id'], data=data)

# Research track.
html = scraperwiki.scrape("http://iswc2011.semanticweb.org/program/research-papers/")

root = lxml.html.fromstring(html)
num = 0;

