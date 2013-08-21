import scraperwiki

import lxml.html 

cols = ['position','driver','nationality','team','points','season']

for year in range(1950, 2012):
    url = 'http://www.formula1.com/results/driver/%s/' % (year,)

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    lst = [] # We can save a list of dicts
    for tr in root.find_class('raceResults')[0].xpath('tr'):
        if tr.xpath('td') and len(tr.xpath('td')[1].xpath('a')) > 0:
            row = [tr.xpath('td')[0].text,
                    tr.xpath('td')[1].xpath('a')[0].text,
                    tr.xpath('td')[2].text,
                    tr.xpath('td')[3].xpath('a')[0].text,
                    tr.xpath('td')[4].text,
                    str(year)]
            lst.append( dict(zip(cols,row)) )

    # Save the list of dictionaries to the main table and the table for this season
    scraperwiki.sqlite.save(['position', 'season'], lst, table_name='Drivers')
    scraperwiki.sqlite.save(['position', 'season'], lst, table_name='Season %s' % str(year))
                
        import scraperwiki

import lxml.html 

cols = ['position','driver','nationality','team','points','season']

for year in range(1950, 2012):
    url = 'http://www.formula1.com/results/driver/%s/' % (year,)

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    lst = [] # We can save a list of dicts
    for tr in root.find_class('raceResults')[0].xpath('tr'):
        if tr.xpath('td') and len(tr.xpath('td')[1].xpath('a')) > 0:
            row = [tr.xpath('td')[0].text,
                    tr.xpath('td')[1].xpath('a')[0].text,
                    tr.xpath('td')[2].text,
                    tr.xpath('td')[3].xpath('a')[0].text,
                    tr.xpath('td')[4].text,
                    str(year)]
            lst.append( dict(zip(cols,row)) )

    # Save the list of dictionaries to the main table and the table for this season
    scraperwiki.sqlite.save(['position', 'season'], lst, table_name='Drivers')
    scraperwiki.sqlite.save(['position', 'season'], lst, table_name='Season %s' % str(year))
                
        