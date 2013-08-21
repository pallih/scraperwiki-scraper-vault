import dateutil.parser
import urllib
import urllib2
import lxml
import lxml.html

import scraperwiki


parkrun_url = "http://www.parkrun.org.uk/south-manchester/results/weeklyresults?runSeqNumber=%i"

def get_results(race):
    req = urllib2.Request(parkrun_url%(race))

    req.add_header("User-Agent", "Mozilla")
    req.add_header("Host", "www.parkrun.org.uk")
    req.add_header("Accept", "*/*")

    r = urllib2.urlopen(req)
    text = r.read()

    html = lxml.html.document_fromstring(text)
    # Hurts my eyes to do this, fragile as hell way
    # to get the race ID and date
    d = html.get_element_by_id("dnn_ctr4953_ModuleContent")
    racename = list(d.find_class("normal")[0])[1].text_content()
    raceid = racename.split('\n')[1].strip().replace("-","").strip()
    racedate = dateutil.parser.parse(racename.split('\n')[2].strip(),
                                     dayfirst=True)
    assert(int(raceid) == race)

    results_rows = list(html.get_element_by_id("results"))[1]

    racers = []

    for row in results_rows:
        vals = [td.text_content() for td in row]
        racer = dict()
        # Some racers have no times, skip them
        if not vals[2]:
            continue

        racer['position'] = int(vals[0])
        racer['name'] = vals[1]
        min,sec = [int(d) for d in vals[2].split(":")]
        racer['time'] = min*60 + sec
        racer['agegroup'] = vals[3]
        racer['gender'] = vals[5]
        racer['genderpos'] = int(vals[6])
        racer['race'] = int(race)
        racer['racedate'] = racedate

        racers.append(racer)

    print race, len(racers)
    return racers


# Limit to first 50 races, could easily extend it to more
# and keep it up to date but for that we should find out
# scraping policy of parkrun.org
for race in range(1, 51):
    res = get_results(race)

    keys = ["race", "racedate", "name"]
    
    scraperwiki.sqlite.save(keys, res)



