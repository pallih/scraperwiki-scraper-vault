import scraperwiki
import lxml.html
import calendar

cal = calendar.Calendar()

# print maximum daily temperature in London for everyday of January 2010
for m in range(1,13):
    # days in month .... 
    for d in cal.itermonthdays(2010, m):
        print 'Processing %s/%s' % (d, m,)
        #timestamp = '2010' + str(m) + str(d)
        timestamp_pretty = '%s/%s/%s' % ('2010', str(m), str(d) )
        url = "http://www.wunderground.com/history/airport/EGLL/2010/" + str(m) + "/" + str(d) + "/DailyHistory.html"
        
        # Needed to workaround the bad entry in the scraperwiki cache.
        url += '?avoidcache=hack'

        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)

        DailyMeanTemp = root.cssselect("span.nobr span.b")[0]
        DailyMaxTemp = root.cssselect("span.nobr span.b")[1]
        DailyMinTemp = root.cssselect("span.nobr span.b")[4]
        
        #print timestamp_pretty + "," + DailyMaxTemp.text
        #scraperwiki.sqlite.save(['date'], {'date':timestamp_pretty, 'max temperature': DailyMaxTemp.text})
        scraperwiki.sqlite.save(['date'], {
            'date':timestamp_pretty, 
            'max temperature': DailyMaxTemp.text, 
            'min temperature': DailyMinTemp.text,
            'mean temperature': DailyMeanTemp.text})

