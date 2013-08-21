import scraperwiki
import lxml.html
import urllib

scraperwiki.sqlite.attach( 'historic_hansard_sitting_years' )
historic_hansard_sitting_years = scraperwiki.sqlite.select("* from historic_hansard_sitting_years.swdata")

sitting_months_fragments = []

for historic_hansard_sitting_year in historic_hansard_sitting_years:
    html = scraperwiki.scrape(historic_hansard_sitting_year['url'])
    root = lxml.html.fromstring(html)
    
    for timeline_date in root.cssselect("td.timeline_date a"):
        sitting_months_fragments.append(timeline_date.attrib['href'])


count = 1
for sitting_months_fragment in sitting_months_fragments:
        data = {
            'url' : 'http://hansard.millbanksystems.com' + sitting_months_fragment, 'count' : count
        }
        count = count + 1
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)






