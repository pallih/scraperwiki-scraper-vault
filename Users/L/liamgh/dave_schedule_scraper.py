import scraperwiki
import lxml.html
import re
from datetime import datetime, time, timedelta, tzinfo

class TZLondon(tzinfo):
     def utcoffset(self, dt):
         return timedelta(0)
     def dst(self, dt):
         return timedelta(hours=1)
     def tzname(self,dt):
         return "Europe/London"

brands = {}

def convertTimeString(timeStr):
    t = re.search("(?P<hour>\d+)\.(?P<minute>\d{2})(?P<noon>[A|P]M)",timeStr)
    hour = int(t.group("hour"))
    min = int(t.group("minute"))
    if t.group("noon") == "PM"and hour != 12:
        hour = hour+12
    elif t.group("noon") == "AM" and hour == 12:
        hour = 0
    return time(hour, min)

def deriveTimes(startTimeStr, endTimeStr, startTime):
    # if clock larger then next day
    progStart = convertTimeString(startTimeStr)
    progEnd = convertTimeString(endTimeStr)
    duration = 0
    start = startTime.replace(hour=progStart.hour, minute=progStart.minute)
    end = startTime.replace(hour=progEnd.hour, minute=progEnd.minute)
    
    # After midnight (handle starting and finishing after midnight)
    if startTime.hour >= 21 and progStart.hour < 12:
        start = start + timedelta(days=1)
    if startTime.hour >= 21 and progEnd.hour < 12:
        end = end + timedelta(days=1)
    # Before midnight (handle starts before midnight)
    if startTime.hour <= 4 and progStart.hour > 21:
        start = start - timedelta(days=1)

    duration = end - start
    return {
        "start": start.isoformat(), 
        "end": end.isoformat(),
        "duration": int(duration.total_seconds())
    }
         

def parseProgInfoTime(infoLine, startTime):
     infoLine =  re.sub("\r|\n|\t"," ", infoLine)
     results = re.search("(?P<title>.*) (?P<start>\d+\.\d\d[AP]M) \- (?P<end>\d+\.\d\d[AP]M) on (?P<channel>.*)", infoLine)
     t = deriveTimes(results.group("start"), results.group("end"), startTime)
     return {
         "title": results.group("title").strip(),
         "start": t["start"],
         "end": t["end"],
         "duration": t["duration"],
         "channel": results.group("channel").strip()
     }

def scrapeContainer(brandLink):
    print "Looking for brand"
    html = scraperwiki.scrape(brandLink)
    root = lxml.html.fromstring(html)
    container = root.cssselect("base")[0].attrib.get('href').strip()
    title = root.cssselect("h1.main")[0].text_content()
    description = ""
    if len(root.cssselect("div#main-copy")) > 0:
        description =root.cssselect("div#main-copy")[0].text_content()
    image = ""
    if len(root.cssselect("div.showpage-body img")):
        image = root.cssselect("div.showpage-body img")[0].attrib.get('src').strip()

    scriptsEle = root.cssselect("script")
    brandSlug = None
    for scriptEle in scriptsEle:
        keywordSearch = re.search("srv_Keywords\' \: \'dave,dave-shows,(.*)\',", scriptEle.text_content())
        if keywordSearch is not None:
            parts = keywordSearch.group(1).split(",")
            if (len(parts) == 2):
                brandSlug =  parts[1]

    data = {
        "type": 'brand',
        "brand-slug": brandSlug,
        "title": title,
        "description": description,
        "image": image,
        "uri": container,
    }
    scraperwiki.sqlite.save(unique_keys=['uri'], data=data)
    return container

def getContainer(brandLink):
    if brandLink not in brands:
        brands[brandLink] = scrapeContainer(brandLink)
    return brands[brandLink]

def getEpgSegment(startTime):
    startUrl = "http://uktv.co.uk/dave/tv/currentDate/%s/startTime/%d" % (startTime.strftime("%Y-%m-%d"), startTime.hour)
    print startUrl
    html = scraperwiki.scrape(startUrl)
    root = lxml.html.fromstring(html)

    progEntryEles = root.cssselect("div.series")

    for progEntryEle in progEntryEles:
        if len(progEntryEle.cssselect("div.progDetails")) > 0:
            container = ""
            progDetailsEle = progEntryEle.cssselect("div.progDetails")[0]
            progDetailsElePs = progDetailsEle.cssselect("p")
            description = ""
            subtitled = False
            audioDescribed = False
            for index, progDetailsEleP in enumerate(progDetailsElePs):
                 text = progDetailsEleP.text_content()
                 if index == 0:
                     timeDetails = parseProgInfoTime(text, startTime)
                 else:
                     if text.find("Subtitled") == 0 or text.find("Audio Described") ==0:
                         subtitled = text.find("Subtitled") != -1
                         audioDescribed = text.find("Audio Described") != -1
                     elif description == "":
                         description = text
        
            uri = progEntryEle.cssselect("div.innerSeries a")[0].attrib.get('href').strip()
            if (timeDetails["channel"] != "Dave") or uri.find("javascript") != -1:
               continue
            container = getContainer(uri)
            data = {
               "start": timeDetails["start"],
               "end": timeDetails["end"],
               "duration": timeDetails["duration"],
               "title": timeDetails["title"],
               "description": description,
               "subtitled" : subtitled,
               "audioDescribed": audioDescribed,
               "channel": timeDetails["channel"],
               "container": container,
               "uri": uri,
               "type": "broadcast"
            }
            scraperwiki.sqlite.save(unique_keys=['uri'], data=data)

howmuch = timedelta(days=2)
startTime = datetime.now(TZLondon()).replace(hour=0,minute=0,second=0,microsecond=0)
endTime = startTime + howmuch

while startTime < endTime:
    getEpgSegment(startTime)
    startTime = startTime + timedelta(hours=3)