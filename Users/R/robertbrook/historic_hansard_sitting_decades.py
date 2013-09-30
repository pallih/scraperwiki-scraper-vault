import scraperwiki
import lxml.html
import urllib

sitting_centuries_fragments = ['19', '20', '21']

sitting_decades_fragments = []

for sitting_centuries_fragment in sitting_centuries_fragments:
    html = scraperwiki.scrape('http://hansard.millbanksystems.com/sittings/C' + sitting_centuries_fragment)
    root = lxml.html.fromstring(html)
    
    for timeline_date in root.cssselect("td.timeline_date a"):
        sitting_decades_fragments.append(timeline_date.attrib['href'])

for sitting_decades_fragment in sitting_decades_fragments:
        data = {
            'url' : 'http://hansard.millbanksystems.com' + sitting_decades_fragment
        }
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)






import scraperwiki
import lxml.html
import urllib

sitting_centuries_fragments = ['19', '20', '21']

sitting_decades_fragments = []

for sitting_centuries_fragment in sitting_centuries_fragments:
    html = scraperwiki.scrape('http://hansard.millbanksystems.com/sittings/C' + sitting_centuries_fragment)
    root = lxml.html.fromstring(html)
    
    for timeline_date in root.cssselect("td.timeline_date a"):
        sitting_decades_fragments.append(timeline_date.attrib['href'])

for sitting_decades_fragment in sitting_decades_fragments:
        data = {
            'url' : 'http://hansard.millbanksystems.com' + sitting_decades_fragment
        }
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)






