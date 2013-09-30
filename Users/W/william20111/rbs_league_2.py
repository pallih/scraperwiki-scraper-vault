import scraperwiki
import BeautifulSoup

from scraperwiki import sqlite

html = scraperwiki.scrape('http://www.bbc.co.uk/sport/rugby-union/scottish-championship-league-b/table')
page = BeautifulSoup.BeautifulSoup(html)

for table in page.findAll('table'):
    for col in table.findAll('td')[1:]:
        if col.get('class','') in ['rank', 'col_text','pld', 'w', 'd', 'l', 'f', 'a', 'pts']:
            rank = col.contents[0]
            col_text = col.contents[0]
            pld = col.contents[0]
            w = col.contents[0]
            d = col.contents[0]
            f = col.contents[0]
            a = col.contents[0]
            l = col.contents[0]
            team = col.contents[0]
            w = col.contents[0]
            pts = col.contents[0]
            print rank
            data = {'rank':rank,
                    'team':col_text,
                    'played':pld,
                    'win':w,
                    'draw':d,
                    'lose':l,
                    'fo':f,
                    'against':a,
                    'pts':pts,
}
            sqlite.save(unique_keys=['rank'], data=data)
import scraperwiki
import BeautifulSoup

from scraperwiki import sqlite

html = scraperwiki.scrape('http://www.bbc.co.uk/sport/rugby-union/scottish-championship-league-b/table')
page = BeautifulSoup.BeautifulSoup(html)

for table in page.findAll('table'):
    for col in table.findAll('td')[1:]:
        if col.get('class','') in ['rank', 'col_text','pld', 'w', 'd', 'l', 'f', 'a', 'pts']:
            rank = col.contents[0]
            col_text = col.contents[0]
            pld = col.contents[0]
            w = col.contents[0]
            d = col.contents[0]
            f = col.contents[0]
            a = col.contents[0]
            l = col.contents[0]
            team = col.contents[0]
            w = col.contents[0]
            pts = col.contents[0]
            print rank
            data = {'rank':rank,
                    'team':col_text,
                    'played':pld,
                    'win':w,
                    'draw':d,
                    'lose':l,
                    'fo':f,
                    'against':a,
                    'pts':pts,
}
            sqlite.save(unique_keys=['rank'], data=data)
