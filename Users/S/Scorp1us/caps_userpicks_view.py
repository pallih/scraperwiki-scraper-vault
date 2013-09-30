# Blank Python
sourcescraper = 'caps_userpicks'

import scraperwiki 
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select( '''ticker||' '||sum(points) title, ticker||' Points:'||sum(points)||' $:'||price||' Up:'||stock_gain_pct||'% Index:'||index_gain_pct||'%' description, max(start_date) pubDate, max(start_date) date, ticker link from (
        select ticker, count(ticker)    points, max(start_price) price, stock_gain_pct , index_gain_pct, max(start_date) start_date from swdata where call='Outperform' group by ticker
        union
        select ticker, count(ticker)*-1 points, max(start_price) price, stock_gain_pct, index_gain_pct, max(start_date) start_date  from swdata where call='Underperform' group by ticker
    )
where points > 5 and stock_gain_pct > index_gain_pct and stock_gain_pct > 0
group by ticker order by date desc, points''')

#data = scraperwiki.sqlite.select( '''ticker||' '||count(ticker) title, '' link,  ticker||' '||count(ticker)||' '||start_price description, datetime('now') date from swdata where call='Outperform' and stock_gain_pct > index_gain_pct group by ticker having count(ticker) > 3 order by count(ticker) desc''' ) 

print "<table>" 
print "<tr><th>Ticker</th><th>Description</th><th>Date</th>" 
for d in data: 
    print "<tr>" 
    print "<td>", d["title"], "</td>" 
    print "<td>", d["description"], "</td>" 
    print "<td>", d["date"], "</td>" 
    print "</tr>"   
print "</table>"
# Blank Python
sourcescraper = 'caps_userpicks'

import scraperwiki 
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select( '''ticker||' '||sum(points) title, ticker||' Points:'||sum(points)||' $:'||price||' Up:'||stock_gain_pct||'% Index:'||index_gain_pct||'%' description, max(start_date) pubDate, max(start_date) date, ticker link from (
        select ticker, count(ticker)    points, max(start_price) price, stock_gain_pct , index_gain_pct, max(start_date) start_date from swdata where call='Outperform' group by ticker
        union
        select ticker, count(ticker)*-1 points, max(start_price) price, stock_gain_pct, index_gain_pct, max(start_date) start_date  from swdata where call='Underperform' group by ticker
    )
where points > 5 and stock_gain_pct > index_gain_pct and stock_gain_pct > 0
group by ticker order by date desc, points''')

#data = scraperwiki.sqlite.select( '''ticker||' '||count(ticker) title, '' link,  ticker||' '||count(ticker)||' '||start_price description, datetime('now') date from swdata where call='Outperform' and stock_gain_pct > index_gain_pct group by ticker having count(ticker) > 3 order by count(ticker) desc''' ) 

print "<table>" 
print "<tr><th>Ticker</th><th>Description</th><th>Date</th>" 
for d in data: 
    print "<tr>" 
    print "<td>", d["title"], "</td>" 
    print "<td>", d["description"], "</td>" 
    print "<td>", d["date"], "</td>" 
    print "</tr>"   
print "</table>"
