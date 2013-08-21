# EDSA View for MMDA Tweets

import datetime
import scraperwiki

def friendly_diff(diff):
    second_diff = diff.seconds
    day_diff = diff.days
    if day_diff < 0:
        return ''
    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"


scraperwiki.utils.httpresponseheader('Content-Type', 'text/plain')

sourcescraper = 'mmda_tweets'
scraperwiki.sqlite.attach(sourcescraper)
now = datetime.datetime.utcnow()
query = scraperwiki.utils.GET()
roads = query.get('roads', 'edsa|c5|slex').split('|')

if query.get('update', False):
    scraper = scraperwiki.utils.swimport(sourcescraper)
    for road in roads:
        data = scraper.scrape_road(road)
print now

for road in roads:
    data = scraperwiki.sqlite.select('* from %s.swdata where road="%s" order by updated_at desc limit 10' % (sourcescraper, road))
    print '*', road
    for datum in data:
        try:
            updated_at = datetime.datetime.strptime(datum['updated_at'], "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            updated_at = datetime.datetime.strptime(datum['updated_at'], "%Y-%m-%dT%H:%M:%S")
        delta = (now - updated_at)
        print '-', friendly_diff(delta), (delta.days, delta.seconds)


