import scraperwiki

import lxml.html 


for year in range(2011, 2012):
    url = 'http://www.formula1.com/results/season/%s' % (year,)

    html = scraperwiki.scrape(url)
      
    root = lxml.html.fromstring(html)

    data = {
        'country' : None,
        'date' : None,
        'driver' : None,
        'team' : None,
        'laps' : None,
        'duration' : None,
    }
    print year
    for tr in root.find_class('raceResults')[0].xpath('tr'):
        if tr.xpath('td'):
            # check we have a driver, otherwise race has yet to take place!
            if len(tr.xpath('td')[2].xpath('a')) > 0:
                data['country'] = tr.xpath('td')[0].xpath('a')[0].text
                data['date'] = tr.xpath('td')[1].text
                data['driver'] = tr.xpath('td')[2].xpath('a')[0].text
                data['team'] = tr.xpath('td')[3].xpath('a')[0].text
                data['laps'] = tr.xpath('td')[4].text
                data['duration'] = tr.xpath('td')[5].text
                data['season'] = tr.xpath('td')[1].text.split('/')[2]
                scraperwiki.sqlite.save(unique_keys=['date'], data=data)
        import scraperwiki

import lxml.html 


for year in range(2011, 2012):
    url = 'http://www.formula1.com/results/season/%s' % (year,)

    html = scraperwiki.scrape(url)
      
    root = lxml.html.fromstring(html)

    data = {
        'country' : None,
        'date' : None,
        'driver' : None,
        'team' : None,
        'laps' : None,
        'duration' : None,
    }
    print year
    for tr in root.find_class('raceResults')[0].xpath('tr'):
        if tr.xpath('td'):
            # check we have a driver, otherwise race has yet to take place!
            if len(tr.xpath('td')[2].xpath('a')) > 0:
                data['country'] = tr.xpath('td')[0].xpath('a')[0].text
                data['date'] = tr.xpath('td')[1].text
                data['driver'] = tr.xpath('td')[2].xpath('a')[0].text
                data['team'] = tr.xpath('td')[3].xpath('a')[0].text
                data['laps'] = tr.xpath('td')[4].text
                data['duration'] = tr.xpath('td')[5].text
                data['season'] = tr.xpath('td')[1].text.split('/')[2]
                scraperwiki.sqlite.save(unique_keys=['date'], data=data)
        