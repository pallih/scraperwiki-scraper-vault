import scraperwiki

import lxml.html 

try:
    scraperwiki.sqlite.execute("drop table constructors")
    scraperwiki.sqlite.execute("create table constructors (position int, team string, points int, season int)")   
except:
    pass

for year in range(2011, 2012):
    url = 'http://www.formula1.com/results/team/%s/' % (year,)

    html = scraperwiki.scrape(url)
      
    root = lxml.html.fromstring(html)

    data = {
        'position' : None,
        'team' : None,
        'points' : None,
        'season' : str(year),
    }
    print year
    for tr in root.find_class('raceResults')[0].xpath('tr'):
        if tr.xpath('td'):
            # check we have a driver, otherwise race has yet to take place!
            if len(tr.xpath('td')[1].xpath('a')) > 0:
                scraperwiki.sqlite.execute('insert into constructors values (?, ?, ?, ?)', (
                        tr.xpath('td')[0].text,
                        tr.xpath('td')[1].xpath('a')[0].text,
                        tr.xpath('td')[2].text,
                        str(year)))
                scraperwiki.sqlite.commit()
        