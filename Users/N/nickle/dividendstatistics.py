sourcescraper = 'dividends'

import scraperwiki


scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select(           
    '''
        ticker 'Ticker', 
        count (ticker) 'Count'
        from dividends.swdata 
        group by ticker
        order by ticker
        '''
)
print "<table>"           
print "<tr><th>Ticker</th><th>Count</th>"
for d in data:
    print "<tr>"
    print "<td>", d["Ticker"], "</td>"
    print "<td>", d["Count"], "</td>"
    print "</tr>"
print "</table>"sourcescraper = 'dividends'

import scraperwiki


scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select(           
    '''
        ticker 'Ticker', 
        count (ticker) 'Count'
        from dividends.swdata 
        group by ticker
        order by ticker
        '''
)
print "<table>"           
print "<tr><th>Ticker</th><th>Count</th>"
for d in data:
    print "<tr>"
    print "<td>", d["Ticker"], "</td>"
    print "<td>", d["Count"], "</td>"
    print "</tr>"
print "</table>"