import scraperwiki
import urllib
import re
import json
import time

maxindex = scraperwiki.sqlite.select("max(id) from swdata")[0]["max(id)"]

places_raw = scraperwiki.scrape('http://www.census.gov/tiger/tms/gazetteer/places2k.txt')

places = []
for line in places_raw.splitlines():
    state= line[:2]
    name = line[9:72].strip().decode('utf8',errors='ignore')

    name = ' '.join(name.split()[:-1])

    lat = float(line[143:153].strip())
    lon = float(line[153:163].strip())

    places.append({
        "name": name,
        "state": state,
        "lat": lat,
        "lon": lon,
    })

class MyOpener(urllib.FancyURLopener):
    version = 'https://scraperwiki.com/scrapers/us_settlement_dates/'

opener = MyOpener()

endpoint = "http://en.wikipedia.org/w/api.php"

def get(params):
    try:
        url = endpoint + "?" + urllib.urlencode(params)
    except UnicodeEncodeError:
        print "some ugly unicode error"
        return None
    try:
        response = opener.open(url)
    except IOError:
        print "hit IO Error. Sleeping for 10 seconds"
        time.sleep(10)
        return get(params)

    response = json.loads(response.read())
    try:
        pages = response['query']['pages']
    except KeyError:
        print response
        return None
    first_key = pages.keys()[0]
    if first_key == "-1":
        return None
    content = pages[first_key]['revisions'][0]['*']

    if '#REDIRECT' in content:
        name = content.split('[[')[1].split(']]')[0].strip()
        params['titles'] = name
        return get(params)
    else:
        return content

def extract_settled(content):
    dates = []
    for line in content.splitlines():
        if "|established_date" in line:
            try:
                dateline = line.split('=')[1].strip()
            except IndexError:
                return None
            if dateline:
                date = map(int, re.findall('([1-2][0-9][0-9][0-9])',dateline))
                try:
                    dates.append(min(date))
                except ValueError:
                    print "failed to parse"
                    print dateline
                    return None
    if len(dates) == 0:
        return None
    else:
        return min(dates)

try:
        for i,place in enumerate(places):
            if i < maxindex:
                continue
            print i, place
            params = {
                "format":"json",
                "action":"query",
                "prop":"revisions",
                "rvprop":"content",
                "maxlag":5,
                "titles":"%s, %s"%(place['name'], place['state'])
            }
            content = get(params)
            if not content:
                print place['name'], "has no content"
                continue
            dates = extract_settled(content)
            if dates:
                place['dates'] = dates
                place['id'] = i
                scraperwiki.sqlite.save(unique_keys=['id'], data=place)
except scraperwiki.CPUTimeExceededError:
    print "reached my CPU time for today!"