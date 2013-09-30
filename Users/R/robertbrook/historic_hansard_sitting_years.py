import scraperwiki
import lxml.html
import urllib

scraperwiki.sqlite.attach( 'historic_hansard_sitting_decades' )
historic_hansard_sitting_decades = scraperwiki.sqlite.select("* from historic_hansard_sitting_decades.swdata")

sitting_years_fragments = []

for historic_hansard_sitting_decade in historic_hansard_sitting_decades:
    html = scraperwiki.scrape(historic_hansard_sitting_decade['url'])
    root = lxml.html.fromstring(html)
    
    for timeline_date in root.cssselect("td.timeline_date a"):
        sitting_years_fragments.append(timeline_date.attrib['href'])

for sitting_years_fragment in sitting_years_fragments:
        data = {
            'url' : 'http://hansard.millbanksystems.com' + sitting_years_fragment
        }
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)







import scraperwiki
import lxml.html
import urllib

scraperwiki.sqlite.attach( 'historic_hansard_sitting_decades' )
historic_hansard_sitting_decades = scraperwiki.sqlite.select("* from historic_hansard_sitting_decades.swdata")

sitting_years_fragments = []

for historic_hansard_sitting_decade in historic_hansard_sitting_decades:
    html = scraperwiki.scrape(historic_hansard_sitting_decade['url'])
    root = lxml.html.fromstring(html)
    
    for timeline_date in root.cssselect("td.timeline_date a"):
        sitting_years_fragments.append(timeline_date.attrib['href'])

for sitting_years_fragment in sitting_years_fragments:
        data = {
            'url' : 'http://hansard.millbanksystems.com' + sitting_years_fragment
        }
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)







