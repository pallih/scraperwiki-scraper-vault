import scraperwiki

import lxml.html 

try:
    #scraperwiki.sqlite.execute("drop table drivers")
    scraperwiki.sqlite.execute("create table drivers (position int, driver string, nationality string, team string, points int, season int)")
except:
    pass

for year in range(1950, 2012):
    url = 'http://www.formula1.com/results/driver/%s/' % (year,)

    html = scraperwiki.scrape(url)
      
    root = lxml.html.fromstring(html)

    data = {
        'position' : None,
        'driver' : None,
        'nationality' : None,
        'team' : None,
        'points' : None,
        'season' : str(year),
    }
    print year
    for tr in root.find_class('raceResults')[0].xpath('tr'):
        if tr.xpath('td'):
            # check we have a driver, otherwise race has yet to take place!
            if len(tr.xpath('td')[1].xpath('a')) > 0:
                scraperwiki.sqlite.execute('insert into drivers values (?, ?, ?, ?, ?, ?)', (
                        tr.xpath('td')[0].text,
                        tr.xpath('td')[1].xpath('a')[0].text,
                        tr.xpath('td')[2].text,
                        tr.xpath('td')[3].xpath('a')[0].text,
                        tr.xpath('td')[4].text,
                        str(year)))
                scraperwiki.sqlite.commit()
                
        import scraperwiki

import lxml.html 

try:
    #scraperwiki.sqlite.execute("drop table drivers")
    scraperwiki.sqlite.execute("create table drivers (position int, driver string, nationality string, team string, points int, season int)")
except:
    pass

for year in range(1950, 2012):
    url = 'http://www.formula1.com/results/driver/%s/' % (year,)

    html = scraperwiki.scrape(url)
      
    root = lxml.html.fromstring(html)

    data = {
        'position' : None,
        'driver' : None,
        'nationality' : None,
        'team' : None,
        'points' : None,
        'season' : str(year),
    }
    print year
    for tr in root.find_class('raceResults')[0].xpath('tr'):
        if tr.xpath('td'):
            # check we have a driver, otherwise race has yet to take place!
            if len(tr.xpath('td')[1].xpath('a')) > 0:
                scraperwiki.sqlite.execute('insert into drivers values (?, ?, ?, ?, ?, ?)', (
                        tr.xpath('td')[0].text,
                        tr.xpath('td')[1].xpath('a')[0].text,
                        tr.xpath('td')[2].text,
                        tr.xpath('td')[3].xpath('a')[0].text,
                        tr.xpath('td')[4].text,
                        str(year)))
                scraperwiki.sqlite.commit()
                
        