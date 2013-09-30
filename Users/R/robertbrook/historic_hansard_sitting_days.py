import scraperwiki
import lxml.html
import urllib

# scraperwiki.sqlite.execute('''
#    CREATE INDEX IF NOT EXISTS count_manual_index 
#    ON swdata (count)''')

start_count = scraperwiki.sqlite.get_var("last_saved", 1) - 1
count = scraperwiki.sqlite.get_var("last_counter", 0) + 1

scraperwiki.sqlite.attach( 'historic_hansard_sitting_months' )
historic_hansard_sitting_months = scraperwiki.sqlite.select("* from historic_hansard_sitting_months.swdata where count > " + str(start_count) + " ORDER BY count")

for historic_hansard_sitting_month in historic_hansard_sitting_months:
    html = scraperwiki.scrape(historic_hansard_sitting_month['url'])
    root = lxml.html.fromstring(html)
    
    for timeline_date in root.cssselect("td.timeline_date a"):
        sitting_days_fragment = timeline_date.attrib['href']
        data = {
            'url' : 'http://hansard.millbanksystems.com' + sitting_days_fragment, 'count' : count
        }
        count = count + 1
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)
        scraperwiki.sqlite.save_var("last_saved", historic_hansard_sitting_month['count'])
        scraperwiki.sqlite.save_var("last_counter", count)






import scraperwiki
import lxml.html
import urllib

# scraperwiki.sqlite.execute('''
#    CREATE INDEX IF NOT EXISTS count_manual_index 
#    ON swdata (count)''')

start_count = scraperwiki.sqlite.get_var("last_saved", 1) - 1
count = scraperwiki.sqlite.get_var("last_counter", 0) + 1

scraperwiki.sqlite.attach( 'historic_hansard_sitting_months' )
historic_hansard_sitting_months = scraperwiki.sqlite.select("* from historic_hansard_sitting_months.swdata where count > " + str(start_count) + " ORDER BY count")

for historic_hansard_sitting_month in historic_hansard_sitting_months:
    html = scraperwiki.scrape(historic_hansard_sitting_month['url'])
    root = lxml.html.fromstring(html)
    
    for timeline_date in root.cssselect("td.timeline_date a"):
        sitting_days_fragment = timeline_date.attrib['href']
        data = {
            'url' : 'http://hansard.millbanksystems.com' + sitting_days_fragment, 'count' : count
        }
        count = count + 1
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)
        scraperwiki.sqlite.save_var("last_saved", historic_hansard_sitting_month['count'])
        scraperwiki.sqlite.save_var("last_counter", count)






