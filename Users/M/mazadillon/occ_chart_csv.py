import scraperwiki
scraperwiki.sqlite.attach("occ_charts")

get = scraperwiki.utils.GET()

try: chart = get['chart']
except KeyError: chart = False

try: date = get['date']
except KeyError: date = False

if date == False:
    data = scraperwiki.sqlite.select("date FROM occ_charts.swdata order by date DESC LIMIT 1")
    date = data[0]['date']

if chart:
    data = scraperwiki.sqlite.select("* FROM occ_charts.swdata where chart='"+chart+"' and date='"+date+"' order by date DESC,position asc limit 100")
    scraperwiki.utils.httpresponseheader('Content-Type','text/html')
    print 'Loading chart '+chart+' for '+date+'<br />'
    for row in data:
        print row['artist'] + ',' + row['title'] + '<br />'

else:
    data = scraperwiki.sqlite.select("* FROM occ_charts.swdata group by date order by date DESC")
    for row in data:
        print row['date']
        print ' <a href="https://views.scraperwiki.com/run/occ_chart_csv/?chart=singles&date=' + row['date'] + '">Singles</a>'
        print ' <a href="https://views.scraperwiki.com/run/occ_chart_csv/?chart=albums&date=' + row['date'] + '">Albums</a>'
        print '<br />'

    

import scraperwiki
scraperwiki.sqlite.attach("occ_charts")

get = scraperwiki.utils.GET()

try: chart = get['chart']
except KeyError: chart = False

try: date = get['date']
except KeyError: date = False

if date == False:
    data = scraperwiki.sqlite.select("date FROM occ_charts.swdata order by date DESC LIMIT 1")
    date = data[0]['date']

if chart:
    data = scraperwiki.sqlite.select("* FROM occ_charts.swdata where chart='"+chart+"' and date='"+date+"' order by date DESC,position asc limit 100")
    scraperwiki.utils.httpresponseheader('Content-Type','text/html')
    print 'Loading chart '+chart+' for '+date+'<br />'
    for row in data:
        print row['artist'] + ',' + row['title'] + '<br />'

else:
    data = scraperwiki.sqlite.select("* FROM occ_charts.swdata group by date order by date DESC")
    for row in data:
        print row['date']
        print ' <a href="https://views.scraperwiki.com/run/occ_chart_csv/?chart=singles&date=' + row['date'] + '">Singles</a>'
        print ' <a href="https://views.scraperwiki.com/run/occ_chart_csv/?chart=albums&date=' + row['date'] + '">Albums</a>'
        print '<br />'

    

