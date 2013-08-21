# sorry, a very dirty quick hack to get an ical schedule
# imported to google spreadsheet + small python script from there to ical
import scraperwiki
import urllib
import urllib2
import urlparse
import lxml.etree, lxml.html
import re
import HTMLParser

base = "http://iswc2011.semanticweb.org/program/"
timeHtml = scraperwiki.scrape(base)
timeRoot = lxml.html.fromstring(timeHtml)

days = {'Sunday': '23.10.2011', 'Monday': '24.10.2011',
        'Tuesday': '25.10.2011','Wednesday':'26.10.2011',
        'Thursday':'27.10.2011'}
tracks ={'tb-005': 'Keynote',
         'tb-002': 'Research',
         'tb-008': 'In-Use',
         'tb-009': 'Industry',
         'tb-003': 'Other Event',
         'tb-004': 'Semantic Web Challenge',
         'tb-001': 'Posters and Demos',}
pauses = {'COFFEEBREAK': "CoffeeBreak",
          'LUNCH': "Lunch",
          'BREAK': "Break",
          'CBORFEFAEKE': "CoffeeBreak"}
for div in timeRoot.cssselect(".floatbox .csc-default"):
    h2 = div.cssselect("tr h2")
    track = None
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
        pauseTimes = []
        del timeRow[0]
        for timeCell in timeRow:
            split = timeCell.text_content().split('-')
            startTimes.append(split[0].strip())
            eTime = split[1].strip()
            endTimes.append(eTime if eTime else '23:59') #open ended (e.g., conf dinner)
            pauseTimes.append(0)

        for row in rows:
            td = row.cssselect("td")
            if td[0].get('colspan') > 0:
                track = td[0].text_content()[:-1]
            else:
                room = td[0].text_content()
                del td[0]
                i = 0
                for slot in td:
                    # find the right column for times (rowspans aren't added again)
                    while pauseTimes[i] > 0:
                        pauseTimes[i] -= 1
                        i += 1

                    # if the slot spans multiple lines it's a pause event (coffee or lunch)
                    rs = slot.get('rowspan')
                    if (int(rs) if rs else None) > 1:
                        rtitle = ''.join(slot.text_content().strip().split())
                        title = pauses[rtitle]
                        pauseTimes[i] += int(rs) - 1
                    else:
                        title = slot.text_content().strip()
                    
                    startTime = startTimes[i]
                    cols = slot.get('colspan')
                    if cols: cols = int(cols)
                    i += cols - 1 if cols and cols > 1 else 0
                    try:
                        endTime = endTimes[i]
                    except IndexError:
                        endTime = endTimes[-1]
                        print 'warning, time out of bound:', title
                    
                    date=days[day]
                    
                    link = slot.cssselect('a')
                    # if the slot is linked, the id is the link
                    if len(link) > 0:
                        id = link[0].get('href')
                        if not id.startswith('http://'):
                            if id.startswith('../'):
                                id = "/".join(base.split('/')[:-2]) + "/" + id[3:]
                            else:
                                id = base + id
                            
                    # otherwise, it's the name and start time
                    else:
                        id = base + "#" + urllib.quote_plus(title + date + startTime) #fasten your seat belt!
                    #id = urlparse.urljoin(base, id) # abs urls are preserved by urljoin (lucky)
                    
                    cl = slot.get('class')
                    if cl in tracks:
                        track = tracks[cl]
                    
                    i += 1
                    # Save time to the database.
                    if title:
                        data = {}
                        data['start_time'] = " ".join([date, startTime])
                        data['end_time'] = " ".join([date, endTime])
                        data['room'] = "Haydn" if room == "Hayden" else room
                        data['title'] = title
                        data['id'] = id
                        data['track'] = track if not title in pauses.values() else 'Pause'
                        scraperwiki.sqlite.save(unique_keys=['id'], data=data)



