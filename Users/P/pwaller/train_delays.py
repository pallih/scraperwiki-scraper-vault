from cPickle import dumps
from datetime import datetime, timedelta, time

from scraperwiki import scrape, sqlite
from lxml import html


def maketime(s):
    if s == "On time": 
        return None
    hour, minute = s.strip().rstrip("a").split(":")
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    try:
        return today.replace(hour=int(hour), minute=int(minute))
    except ValueError:
        return None

def maketimes(times):
    times = [maketime(t) for t in times.itertext()]
    sched, actual = times[:2]
    if actual is None: 
        actual = sched
    minutes_late = (actual - sched).seconds // 60
    return sched, actual, minutes_late
    
    
def main():
    print "Scraping"
    content = scrape("http://traintimes.org.uk/live/liv")

    rows = html.fromstring(content).cssselect("#liveboard tr")
    
    for row in rows:
        cols = row.cssselect("td")
        if not cols: continue
            
        times, stations, platforms = cols[:3]
        
        sched, actual, minutes_late = maketimes(times)
        
        sqlite.save(
            unique_keys=["scrapetime", "schedtime", "stations"], 
            data={"scrapetime": dumps(datetime.now()), 
                  "schedtime": dumps(sched), 
                  "stations": stations.text, 
                  "minutes_late": minutes_late})

if __name__ in ("__main__", "scraper"):
    main()from cPickle import dumps
from datetime import datetime, timedelta, time

from scraperwiki import scrape, sqlite
from lxml import html


def maketime(s):
    if s == "On time": 
        return None
    hour, minute = s.strip().rstrip("a").split(":")
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    try:
        return today.replace(hour=int(hour), minute=int(minute))
    except ValueError:
        return None

def maketimes(times):
    times = [maketime(t) for t in times.itertext()]
    sched, actual = times[:2]
    if actual is None: 
        actual = sched
    minutes_late = (actual - sched).seconds // 60
    return sched, actual, minutes_late
    
    
def main():
    print "Scraping"
    content = scrape("http://traintimes.org.uk/live/liv")

    rows = html.fromstring(content).cssselect("#liveboard tr")
    
    for row in rows:
        cols = row.cssselect("td")
        if not cols: continue
            
        times, stations, platforms = cols[:3]
        
        sched, actual, minutes_late = maketimes(times)
        
        sqlite.save(
            unique_keys=["scrapetime", "schedtime", "stations"], 
            data={"scrapetime": dumps(datetime.now()), 
                  "schedtime": dumps(sched), 
                  "stations": stations.text, 
                  "minutes_late": minutes_late})

if __name__ in ("__main__", "scraper"):
    main()