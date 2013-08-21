import scraperwiki
sourcescraper = 'irish_president_engagements'
scraperwiki.sqlite.attach(sourcescraper)

try:
    year = scraperwiki.utils.GET()['year']
    data = scraperwiki.sqlite.select("*,strftime('%Y',DATE) as year FROM swdata WHERE year = '"+year+"' ORDER BY date ASC, time ASC")
    print '<ul>'
    for engagement in data:
        print '<li>{!r} @ {}: {} @ {}</li>'.format(engagement['date'],engagement['time'], engagement['info'], engagement['place'])
    print '</ul>'
except KeyError:    
    data = scraperwiki.sqlite.select("*,strftime('%Y',DATE) as year,count(*) as count FROM swdata group by year order by year desc")
    print '<table><tr><th>Year</th><th>Engagements</th></tr>'
    for year in data:
        print '<tr><td><a href="?year='+year['year']+ '">'+year['year']+ '</td><td>'+str(year['count'])+'</td></tr>'
    print '</table>'
