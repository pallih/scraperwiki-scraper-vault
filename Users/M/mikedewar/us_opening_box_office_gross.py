import scraperwiki
import lxml.html
import time

# Blank Python

html = scraperwiki.scrape(
    "http://boxofficemojo.com/weekend/chart/?view=main&p=.htm"
)
root = lxml.html.fromstring(html)
for table in root.cssselect('table'):
    rows = table.cssselect('tr')
    if len(rows[0].cssselect('td')) == 11:
        for row in rows[1:]:
            cells = row.cssselect('td')
            try:
                week = int(cells[-1].text_content())
            except ValueError:
                continue
            if week == 1:
                data = {
                    'title': cells[2].text_content(),
                    'take': int(cells[4].text_content().strip('$').replace(',','')),
                    'scrape_time': time.time()
                }
                scraperwiki.sqlite.save(unique_keys=['title'], data=data)


#TW    LW    Title (click to view)    Studio    Weekend Gross    % Change    Theater Count / Change    Average    Total Gross    Budget*    Week #

#print root